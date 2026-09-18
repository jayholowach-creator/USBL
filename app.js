let leagueData = null;
let currentLeague = "USBL (Major League)";
let currentSelectedTeam = null;
let currentLineupPlatoon = "vsLHP";

document.addEventListener('DOMContentLoaded', () => {
    fetch('usbl_league_data.json')
        .then(res => res.json())
        .then(data => {
            leagueData = data;
            initDashboard();
        })
        .catch(err => {
            console.log("Could not load usbl_league_data.json:", err);
            showDataError();
        });
});

function showDataError() {
    const container = document.getElementById('standingsContainer');
    if (container) {
        container.innerHTML = `<div class="card" style="border-color:#ef4444;"><h3 style="color:#ef4444;">⚠️ Dataset Not Found</h3><p>Could not load <b>usbl_league_data.json</b>. Make sure you ran <b>export_league_data_v12.py</b> and placed the output JSON file in your web root directory.</p></div>`;
    }
}

function handleLeagueChange() {
    const select = document.getElementById('leagueSelect');
    if (select) {
        currentLeague = select.value;
        document.getElementById('standingsTitle').innerText = `League Standings — ${currentLeague}`;
        document.getElementById('battingTitle').innerText = `Batting Leaders — ${currentLeague}`;
        document.getElementById('pitchingTitle').innerText = `Pitching Leaders — ${currentLeague}`;
        renderStandings();
        renderBattingLeaders();
        renderPitchingLeaders();
    }
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    
    document.getElementById('tab-' + tabName).classList.add('active');
    if (event && event.target) event.target.classList.add('active');

    if (tabName === 'visualizations') {
        renderAllCharts();
    }
}

function initDashboard() {
    renderStandings();
    renderBattingLeaders();
    renderPitchingLeaders();
    renderStatcast();
}

function renderStandings() {
    const container = document.getElementById('standingsContainer');
    if (!container) return;

    let standingsList = [];
    if (leagueData && leagueData.standings_by_league && leagueData.standings_by_league[currentLeague]) {
        standingsList = leagueData.standings_by_league[currentLeague];
    } else if (leagueData && leagueData.standings && leagueData.standings.mlb) {
        standingsList = leagueData.standings.mlb;
    }

    if (!standingsList || standingsList.length === 0) {
        container.innerHTML = `<div class="card"><p>No standings data available for ${currentLeague}.</p></div>`;
        return;
    }

    let rowsHtml = standingsList.map(row => {
        const teamName = row.Team || row.TEAM || row.Tm || "Team";
        const w = row.W || row.w || "0";
        const l = row.L || row.l || "0";
        const pct = row.PCT || row.pct || ".000";
        const gb = row.GB || row.gb || "-";
        const logo = row.logo_url || `images/team_logos/${teamName.toLowerCase().replace(/[^a-z0-9]/g, '_')}.png`;

        return `
            <tr>
                <td class="team-cell">
                    <img src="${logo}" class="team-logo-small" onerror="this.style.display='none'">
                    <a class="team-link" onclick="openTeamSummary('${teamName.replace(/'/g, "\'")}')">${teamName}</a>
                </td>
                <td>${w}</td>
                <td>${l}</td>
                <td>${pct}</td>
                <td>${gb}</td>
            </tr>
        `;
    }).join('');

    container.innerHTML = `
        <div class="card">
            <h3>${currentLeague} Standings</h3>
            <div class="table-wrapper">
                <table>
                    <thead><tr><th>Team</th><th>W</th><th>L</th><th>PCT</th><th>GB</th></tr></thead>
                    <tbody>${rowsHtml}</tbody>
                </table>
            </div>
        </div>`;
}

function openTeamSummary(teamName) {
    currentSelectedTeam = teamName;
    const modal = document.getElementById('teamSummaryModal');
    const titleEl = document.getElementById('modalTeamName');
    const logoEl = document.getElementById('modalTeamLogo');

    titleEl.innerText = teamName;
    const teamSlug = teamName.toLowerCase().replace(/[^a-z0-9]/g, '_');
    logoEl.src = `images/team_logos/${teamSlug}.png`;
    logoEl.style.display = 'block';

    renderTeamLineup();
    renderTeamPitching();
    renderTeamDefense();

    modal.style.display = 'flex';
}

function closeTeamSummary() {
    document.getElementById('teamSummaryModal').style.display = 'none';
}

function switchModalTab(tabKey) {
    document.querySelectorAll('.modal-sub-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.modal-tab-btn').forEach(el => el.classList.remove('active'));

    document.getElementById('modal-sub-' + tabKey).classList.add('active');
    if (event && event.target) event.target.classList.add('active');
}

function toggleLineupPlatoon(platoon) {
    currentLineupPlatoon = platoon;
    document.getElementById('btnLineupLHP').classList.toggle('active', platoon === 'vsLHP');
    document.getElementById('btnLineupRHP').classList.toggle('active', platoon === 'vsRHP');
    renderTeamLineup();
}

function renderTeamLineup() {
    const tbody = document.getElementById('lineupTableBody');
    if (!tbody) return;

    const sampleLineup = [
        { order: 1, pos: 'CF', name: 'Nate Mahoney', avg: '.365', obp: '.420', slg: '.610', ops: '1.030', hr: 28, rbi: 85 },
        { order: 2, pos: 'SS', name: 'Jesse Wilson', avg: '.342', obp: '.395', slg: '.580', ops: '.975', hr: 22, rbi: 78 },
        { order: 3, pos: 'LF', name: 'Dave Gordon', avg: '.328', obp: '.388', slg: '.550', ops: '.938', hr: 25, rbi: 92 },
        { order: 4, pos: '1B', name: 'Elmer Aguilera', avg: '.310', obp: '.375', slg: '.540', ops: '.915', hr: 31, rbi: 104 },
        { order: 5, pos: '3B', name: 'Carlos Gomez', avg: '.295', obp: '.350', slg: '.490', ops: '.840', hr: 18, rbi: 68 },
        { order: 6, pos: 'RF', name: 'Tyler Reed', avg: '.282', obp: '.340', slg: '.470', ops: '.810', hr: 16, rbi: 60 },
        { order: 7, pos: 'DH', name: 'Marcus Vance', avg: '.275', obp: '.335', slg: '.460', ops: '.795', hr: 19, rbi: 64 },
        { order: 8, pos: 'C',  name: 'Brian Martinez', avg: '.260', obp: '.320', slg: '.410', ops: '.730', hr: 11, rbi: 45 },
        { order: 9, pos: '2B', name: 'Kevin O'Connor', avg: '.252', obp: '.315', slg: '.390', ops: '.705', hr: 8, rbi: 38 }
    ];

    tbody.innerHTML = sampleLineup.map(p => `
        <tr>
            <td><b>${p.order}</b></td>
            <td><span class="badge" style="background:#0284c7;">${p.pos}</span></td>
            <td>
                <img src="images/players/${p.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}.png" class="player-headshot" onerror="this.src='images/players/default.png'">
                ${p.name}
            </td>
            <td>${p.avg}</td>
            <td>${p.obp}</td>
            <td>${p.slg}</td>
            <td><b>${p.ops}</b></td>
            <td>${p.hr}</td>
            <td>${p.rbi}</td>
        </tr>
    `).join('');
}

function renderTeamPitching() {
    const rotBody = document.getElementById('rotationTableBody');
    const bullBody = document.getElementById('bullpenTableBody');

    const sampleRotation = [
        { role: 'SP1', name: 'Mike Pearsall', wl: '18-5', era: '2.84', ip: '210.0', whip: '1.05', k9: '9.8', bb9: '2.1' },
        { role: 'SP2', name: 'Chris Vance', wl: '15-7', era: '3.12', ip: '192.1', whip: '1.12', k9: '9.2', bb9: '2.4' },
        { role: 'SP3', name: 'David Miller', wl: '12-8', era: '3.65', ip: '175.0', whip: '1.20', k9: '8.5', bb9: '2.8' },
        { role: 'SP4', name: 'Jason Thorne', wl: '11-9', era: '4.02', ip: '160.0', whip: '1.28', k9: '8.1', bb9: '3.1' },
        { role: 'SP5', name: 'Alex Rivera', wl: '9-10', era: '4.35', ip: '148.2', whip: '1.34', k9: '7.8', bb9: '3.4' }
    ];

    const sampleBullpen = [
        { role: 'CL', name: 'Mark Chapman', wl: '4-2', era: '1.95', sv: 38, ip: '64.2', whip: '0.92', k9: '12.4' },
        { role: 'SU', name: 'Derek Shaw', wl: '6-3', era: '2.45', sv: 5, ip: '72.0', whip: '1.04', k9: '10.8' },
        { role: 'MR', name: 'Greg Watson', wl: '5-4', era: '3.20', sv: 2, ip: '68.0', whip: '1.18', k9: '9.1' },
        { role: 'LR', name: 'Scott Bennett', wl: '3-2', era: '3.85', sv: 0, ip: '55.0', whip: '1.25', k9: '8.0' }
    ];

    if (rotBody) {
        rotBody.innerHTML = sampleRotation.map(p => `
            <tr>
                <td><b>${p.role}</b></td>
                <td><img src="images/players/${p.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}.png" class="player-headshot" onerror="this.src='images/players/default.png'">${p.name}</td>
                <td>${p.wl}</td>
                <td><b>${p.era}</b></td>
                <td>${p.ip}</td>
                <td>${p.whip}</td>
                <td>${p.k9}</td>
                <td>${p.bb9}</td>
            </tr>
        `).join('');
    }

    if (bullBody) {
        bullBody.innerHTML = sampleBullpen.map(p => `
            <tr>
                <td><b>${p.role}</b></td>
                <td><img src="images/players/${p.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}.png" class="player-headshot" onerror="this.src='images/players/default.png'">${p.name}</td>
                <td>${p.wl}</td>
                <td><b>${p.era}</b></td>
                <td><b>${p.sv}</b></td>
                <td>${p.ip}</td>
                <td>${p.whip}</td>
                <td>${p.k9}</td>
            </tr>
        `).join('');
    }
}

function renderTeamDefense() {
    const defenseMap = {
        'C':  { name: 'Brian Martinez', zr: '+4.2', fld: '.992', err: 3 },
        '1B': { name: 'Elmer Aguilera', zr: '+1.5', fld: '.995', err: 4 },
        '2B': { name: 'Kevin O'Connor', zr: '+6.8', fld: '.988', err: 6 },
        '3B': { name: 'Carlos Gomez', zr: '-1.2', fld: '.965', err: 11 },
        'SS': { name: 'Jesse Wilson', zr: '+12.4', fld: '.982', err: 8 },
        'LF': { name: 'Dave Gordon', zr: '+2.1', fld: '.985', err: 3 },
        'CF': { name: 'Nate Mahoney', zr: '+14.8', fld: '.994', err: 1 },
        'RF': { name: 'Tyler Reed', zr: '+0.5', fld: '.978', err: 4 }
    };

    Object.keys(defenseMap).forEach(pos => {
        const el = document.getElementById('def-' + pos);
        if (el) {
            const data = defenseMap[pos];
            el.innerHTML = `
                <div style="font-weight:700;">${data.name}</div>
                <div style="font-size:0.75rem;color:#38bdf8;">ZR: <b>${data.zr}</b> | FLD%: <b>${data.fld}</b></div>
            `;
        }
    });
}

function renderBattingLeaders() {
    const container = document.getElementById('battingLeadersContainer');
    if (!container) return;

    let batList = [];
    if (leagueData && leagueData.batting_by_league && leagueData.batting_by_league[currentLeague]) {
        batList = leagueData.batting_by_league[currentLeague];
    } else if (leagueData && leagueData.batting_leaders && leagueData.batting_leaders.mlb) {
        batList = leagueData.batting_leaders.mlb;
    }

    if (!batList || batList.length === 0) {
        container.innerHTML = `<div class="card"><p>No batting statistics available for ${currentLeague}.</p></div>`;
        return;
    }

    const topAvg = batList.slice(0, 5);
    let avgRows = topAvg.map((p, idx) => `
        <tr>
            <td>${idx + 1}</td>
            <td><img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">${p.Player || p.Name || "Player"}</td>
            <td>${p.Team || p.TM || "-"}</td>
            <td><b>${p.AVG || p.Avg || ".000"}</b></td>
        </tr>
    `).join('');

    container.innerHTML = `
        <div class="card">
            <h3>Batting Average (AVG)</h3>
            <div class="table-wrapper">
                <table>
                    <thead><tr><th>#</th><th>Player</th><th>Team</th><th>AVG</th></tr></thead>
                    <tbody>${avgRows}</tbody>
                </table>
            </div>
        </div>`;
}

function renderPitchingLeaders() {
    const container = document.getElementById('pitchingLeadersContainer');
    if (!container) return;

    let pitchList = [];
    if (leagueData && leagueData.pitching_by_league && leagueData.pitching_by_league[currentLeague]) {
        pitchList = leagueData.pitching_by_league[currentLeague];
    } else if (leagueData && leagueData.pitching_leaders && leagueData.pitching_leaders.mlb) {
        pitchList = leagueData.pitching_leaders.mlb;
    }

    if (!pitchList || pitchList.length === 0) {
        container.innerHTML = `<div class="card"><p>No pitching statistics available for ${currentLeague}.</p></div>`;
        return;
    }

    const topEra = pitchList.slice(0, 5);
    let eraRows = topEra.map((p, idx) => `
        <tr>
            <td>${idx + 1}</td>
            <td><img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">${p.Player || p.Name || "Pitcher"}</td>
            <td>${p.Team || p.TM || "-"}</td>
            <td><b>${p.ERA || p.Era || "0.00"}</b></td>
        </tr>
    `).join('');

    container.innerHTML = `
        <div class="card">
            <h3>Earned Run Average (ERA)</h3>
            <div class="table-wrapper">
                <table>
                    <thead><tr><th>#</th><th>Pitcher</th><th>Team</th><th>ERA</th></tr></thead>
                    <tbody>${eraRows}</tbody>
                </table>
            </div>
        </div>`;
}

function renderStatcast() {
    const cards = document.getElementById('statcastCards');
    const tbody = document.getElementById('statcastTableBody');

    let scData = (leagueData && leagueData.statcast_data) ? leagueData.statcast_data : null;

    if (cards && scData && scData.summary) {
        cards.innerHTML = `
            <div class="card"><h3>Max Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#ef4444;font-weight:bold;">${scData.summary.max_ev || "111.3"} MPH</p><p>${scData.summary.max_ev_player || "Jesse Wilson"}</p></div>
            <div class="card"><h3>Hard-Hit % (95+ MPH)</h3><p class="subtitle" style="font-size:1.5rem;color:#f59e0b;font-weight:bold;">${scData.summary.hard_hit_pct || "48.2"}%</p><p>League Batted Balls</p></div>
            <div class="card"><h3>Avg Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#10b981;font-weight:bold;">${scData.summary.avg_ev || "91.4"} MPH</p><p>All Field Events</p></div>
            <div class="card"><h3>Batted Balls Tracked</h3><p class="subtitle" style="font-size:1.5rem;color:#38bdf8;font-weight:bold;">${scData.summary.total_batted_balls || "1,240"}</p><p>Play-by-Play Logs</p></div>`;
    }

    if (tbody && scData && scData.leaderboard && scData.leaderboard.length > 0) {
        tbody.innerHTML = scData.leaderboard.slice(0, 15).map(b => `
            <tr>
                <td><img src="${b.headshot_url}" class="player-headshot" onerror="this.src='images/players/default.png'">${b.player}</td>
                <td><b>${b.ev} MPH</b></td>
                <td>${b.trajectory}</td>
                <td>${b.distance ? b.distance + ' FT' : '-'}</td>
                <td>${b.is_hard_hit ? '<span class="badge" style="background:#ef4444;">🔥 Hard-Hit</span>' : '<span class="badge" style="background:#64748b;">Standard</span>'}</td>
            </tr>
        `).join('');
    } else if (tbody) {
        tbody.innerHTML = `
            <tr><td>Jesse Wilson</td><td><b>111.3 MPH</b></td><td>Line Drive</td><td>380 FT</td><td><span class="badge" style="background:#ef4444;">🔥 Hard-Hit</span></td></tr>
            <tr><td>Nate Mahoney</td><td><b>110.0 MPH</b></td><td>Flyball</td><td>420 FT</td><td><span class="badge" style="background:#ef4444;">🔥 Hard-Hit</span></td></tr>
            <tr><td>Dave Gordon</td><td><b>108.8 MPH</b></td><td>Line Drive</td><td>365 FT</td><td><span class="badge" style="background:#ef4444;">🔥 Hard-Hit</span></td></tr>`;
    }
}

function renderAllCharts() {
    // Chart.js rendering
}

function filterTables() {
    const val = document.getElementById('globalSearch').value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(val) ? '' : 'none';
    });
}
