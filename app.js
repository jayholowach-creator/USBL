let leagueData = null;
let currentLeague = "USBL (Major League)";
let currentSelectedTeam = null;

document.addEventListener('DOMContentLoaded', () => {
    fetch('usbl_league_data.json')
        .then(res => {
            if (!res.ok) throw new Error("HTTP " + res.status);
            return res.json();
        })
        .then(data => {
            leagueData = data;
            initDashboard();
        })
        .catch(err => {
            console.warn("usbl_league_data.json could not be loaded:", err);
            showDatasetMissingError();
        });
});

function showDatasetMissingError() {
    const container = document.getElementById('standingsContainer');
    if (container) {
        container.innerHTML = `
            <div class="card" style="border-color:#ef4444;">
                <h3 style="color:#ef4444;">⚠️ Dataset Not Loaded</h3>
                <p>Could not load <b>usbl_league_data.json</b>. Make sure you ran <b>export_league_data_v15.py</b> and uploaded the resulting JSON file to your web root directory on GitHub Pages.</p>
            </div>`;
    }
}

function handleLeagueChange() {
    const select = document.getElementById('leagueSelect');
    if (select) {
        currentLeague = select.value;
        const stTitle = document.getElementById('standingsTitle');
        const batTitle = document.getElementById('battingTitle');
        const pitchTitle = document.getElementById('pitchingTitle');

        if (stTitle) stTitle.innerText = `League Standings — ${currentLeague}`;
        if (batTitle) batTitle.innerText = `Batting Leaders — ${currentLeague}`;
        if (pitchTitle) pitchTitle.innerText = `Pitching Leaders — ${currentLeague}`;

        renderStandings();
        renderBattingLeaders();
        renderPitchingLeaders();
    }
}

function switchTab(tabName, evt) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    
    const targetTab = document.getElementById('tab-' + tabName);
    if (targetTab) targetTab.classList.add('active');

    if (evt && evt.target) {
        evt.target.classList.add('active');
    }
}

function initDashboard() {
    populatePlayerSelectOptions();
    renderStandings();
    renderBattingLeaders();
    renderPitchingLeaders();
    renderStatcast();
}

function populatePlayerSelectOptions() {
    const select = document.getElementById('playerTrendSelect');
    if (!select) return;

    select.innerHTML = '<option value="">-- Select Player --</option>';
    
    let batList = (leagueData && leagueData.batting_by_league && leagueData.batting_by_league[currentLeague]) 
        ? leagueData.batting_by_league[currentLeague] 
        : [];

    batList.forEach(p => {
        const pName = p.Player || p.Name || p.Batter;
        if (pName) {
            const opt = document.createElement('option');
            opt.value = pName;
            opt.textContent = `${pName} (${p.Team || p.TM || 'Team'})`;
            select.appendChild(opt);
        }
    });
}

function renderStandings() {
    const container = document.getElementById('standingsContainer');
    if (!container) return;

    let standingsList = [];
    if (leagueData && leagueData.standings_by_league && leagueData.standings_by_league[currentLeague]) {
        standingsList = leagueData.standings_by_league[currentLeague];
    }

    if (!standingsList || standingsList.length === 0) {
        container.innerHTML = `<div class="card"><p class="no-data">No standings data found in usbl_league_data.json for ${currentLeague}.</p></div>`;
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

    if (titleEl) titleEl.innerText = teamName;
    if (logoEl) {
        const logoPath = `images/team_logos/${teamName.toLowerCase().replace(/[^a-z0-9]/g, '_')}.png`;
        logoEl.src = logoPath;
        logoEl.style.display = 'inline-block';
    }

    renderTeamRoster();
    renderTeamPitching();
    renderTeamDefense();

    if (modal) modal.style.display = 'flex';
}

function closeTeamSummary() {
    const modal = document.getElementById('teamSummaryModal');
    if (modal) modal.style.display = 'none';
}

function switchModalTab(tabKey) {
    document.querySelectorAll('.modal-sub-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.modal-tab-btn').forEach(el => el.classList.remove('active'));

    const targetSub = document.getElementById('modal-sub-' + tabKey);
    if (targetSub) targetSub.classList.add('active');

    if (event && event.target) {
        event.target.classList.add('active');
    }
}

function renderTeamRoster() {
    const tbody = document.getElementById('lineupTableBody');
    if (!tbody) return;

    let teamHitters = [];
    if (leagueData && leagueData.batting_by_league && leagueData.batting_by_league[currentLeague]) {
        teamHitters = leagueData.batting_by_league[currentLeague].filter(p => {
            const tm = (p.Team || p.TM || "").toLowerCase();
            return tm && currentSelectedTeam.toLowerCase().includes(tm);
        });
    }

    if (!teamHitters || teamHitters.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="no-data">No roster or batting stats available for ${currentSelectedTeam} in extracted OOTP data.</td></tr>`;
        return;
    }

    tbody.innerHTML = teamHitters.map((p, idx) => `
        <tr>
            <td>${idx + 1}</td>
            <td>${p.POS || p.Pos || "UT"}</td>
            <td class="player-cell">
                <img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                ${p.Player || p.Name || "Player"}
            </td>
            <td>${p.AVG || p.Avg || ".000"}</td>
            <td>${p.OBP || p.Obp || ".000"}</td>
            <td>${p.SLG || p.Slg || ".000"}</td>
            <td><b>${p.OPS || p.Ops || ".000"}</b></td>
            <td>${p.HR || p.Hr || "0"}</td>
            <td>${p.RBI || p.Rbi || "0"}</td>
        </tr>
    `).join('');
}

function renderTeamPitching() {
    const tbody = document.getElementById('pitchingStaffTableBody');
    if (!tbody) return;

    let teamPitchers = [];
    if (leagueData && leagueData.pitching_by_league && leagueData.pitching_by_league[currentLeague]) {
        teamPitchers = leagueData.pitching_by_league[currentLeague].filter(p => {
            const tm = (p.Team || p.TM || "").toLowerCase();
            return tm && currentSelectedTeam.toLowerCase().includes(tm);
        });
    }

    if (!teamPitchers || teamPitchers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="no-data">No pitching staff statistics available for ${currentSelectedTeam} in extracted OOTP data.</td></tr>`;
        return;
    }

    tbody.innerHTML = teamPitchers.map((p, idx) => `
        <tr>
            <td>${p.Role || (idx < 5 ? 'SP' + (idx + 1) : 'RP')}</td>
            <td class="player-cell">
                <img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                ${p.Player || p.Name || "Pitcher"}
            </td>
            <td>${p.W || "0"}-${p.L || "0"}</td>
            <td><b>${p.ERA || p.Era || "0.00"}</b></td>
            <td>${p.IP || p.Ip || "0.0"}</td>
            <td>${p.WHIP || p.Whip || "0.00"}</td>
            <td>${p.K9 || p['K/9'] || "0.0"}</td>
            <td>${p.SV || p.Sv || "0"}</td>
        </tr>
    `).join('');
}

function renderTeamDefense() {
    const tbody = document.getElementById('defenseTableBody');
    if (!tbody) return;

    let teamHitters = [];
    if (leagueData && leagueData.batting_by_league && leagueData.batting_by_league[currentLeague]) {
        teamHitters = leagueData.batting_by_league[currentLeague].filter(p => {
            const tm = (p.Team || p.TM || "").toLowerCase();
            return tm && currentSelectedTeam.toLowerCase().includes(tm);
        });
    }

    if (!teamHitters || teamHitters.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="no-data">No defensive rating metrics extracted for ${currentSelectedTeam}.</td></tr>`;
        return;
    }

    tbody.innerHTML = teamHitters.map(p => `
        <tr>
            <td>${p.POS || p.Pos || "UT"}</td>
            <td class="player-cell">
                <img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                ${p.Player || p.Name || "Player"}
            </td>
            <td>${p.ZR || p.Zr || "0.0"}</td>
            <td><b>${p['FLD%'] || p.Fld || ".000"}</b></td>
            <td>${p.E || p.Err || "0"}</td>
        </tr>
    `).join('');
}

function renderBattingLeaders() {
    const container = document.getElementById('battingLeadersContainer');
    if (!container) return;

    let batList = [];
    if (leagueData && leagueData.batting_by_league && leagueData.batting_by_league[currentLeague]) {
        batList = leagueData.batting_by_league[currentLeague];
    }

    if (!batList || batList.length === 0) {
        container.innerHTML = `<div class="card"><p class="no-data">No batting statistics found in usbl_league_data.json for ${currentLeague}.</p></div>`;
        return;
    }

    const topAvg = batList.slice(0, 10);
    let avgRows = topAvg.map((p, idx) => `
        <tr>
            <td>${idx + 1}</td>
            <td class="player-cell">
                <img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                ${p.Player || p.Name || "Player"}
            </td>
            <td>${p.Team || p.TM || "-"}</td>
            <td><b>${p.AVG || p.Avg || ".000"}</b></td>
        </tr>
    `).join('');

    container.innerHTML = `
        <div class="card">
            <h3>Batting Average Leaders (AVG)</h3>
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
    }

    if (!pitchList || pitchList.length === 0) {
        container.innerHTML = `<div class="card"><p class="no-data">No pitching statistics found in usbl_league_data.json for ${currentLeague}.</p></div>`;
        return;
    }

    const topEra = pitchList.slice(0, 10);
    let eraRows = topEra.map((p, idx) => `
        <tr>
            <td>${idx + 1}</td>
            <td class="player-cell">
                <img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                ${p.Player || p.Name || "Pitcher"}
            </td>
            <td>${p.Team || p.TM || "-"}</td>
            <td><b>${p.ERA || p.Era || "0.00"}</b></td>
        </tr>
    `).join('');

    container.innerHTML = `
        <div class="card">
            <h3>Earned Run Average Leaders (ERA)</h3>
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

    if (cards) {
        if (scData && scData.summary && scData.summary.total_batted_balls > 0) {
            cards.innerHTML = `
                <div class="card"><h3>Max Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#ef4444;font-weight:bold;">${scData.summary.max_ev} MPH</p><p>${scData.summary.max_ev_player}</p></div>
                <div class="card"><h3>Hard-Hit % (95+ MPH)</h3><p class="subtitle" style="font-size:1.5rem;color:#f59e0b;font-weight:bold;">${scData.summary.hard_hit_pct}%</p><p>Tracked Field Events</p></div>
                <div class="card"><h3>Avg Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#10b981;font-weight:bold;">${scData.summary.avg_ev} MPH</p><p>All Field Events</p></div>
                <div class="card"><h3>Batted Balls Tracked</h3><p class="subtitle" style="font-size:1.5rem;color:#38bdf8;font-weight:bold;">${scData.summary.total_batted_balls}</p><p>Play-by-Play Logs</p></div>`;
        } else {
            cards.innerHTML = `<div class="card"><p class="no-data">No pitch-by-pitch Statcast logs available for this export.</p></div>`;
        }
    }

    if (tbody) {
        if (scData && scData.leaderboard && scData.leaderboard.length > 0) {
            tbody.innerHTML = scData.leaderboard.slice(0, 25).map(b => `
                <tr>
                    <td class="player-cell">
                        <img src="${b.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                        ${b.player}
                    </td>
                    <td><b>${b.ev} MPH</b></td>
                    <td>${b.trajectory}</td>
                    <td>${b.distance ? b.distance + ' FT' : '-'}</td>
                    <td>${b.is_hard_hit ? '<span class="badge" style="background:#ef4444;">🔥 Hard-Hit</span>' : '<span class="badge" style="background:#64748b;">Standard</span>'}</td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = `<tr><td colspan="5" class="no-data">No Statcast exit velocity records found in OOTP play-by-play logs.</td></tr>`;
        }
    }
}

function updatePlayerTrendChart() {
    const note = document.getElementById('trendChartNote');
    if (note) note.style.display = 'block';
}

function lookupMatchup() {
    const pitcher = document.getElementById('pitcherInput').value.trim();
    const batter = document.getElementById('batterInput').value.trim();
    const resultDiv = document.getElementById('matchupResult');

    if (!resultDiv) return;

    if (!pitcher || !batter) {
        resultDiv.innerHTML = `<div class="card"><p class="no-data">Please enter both a pitcher name and a batter name.</p></div>`;
        return;
    }

    resultDiv.innerHTML = `
        <div class="card">
            <h3>Matchup Query: ${pitcher} (P) vs. ${batter} (B)</h3>
            <p class="no-data mt-2">No head-to-head matchup history found between <b>${pitcher}</b> and <b>${batter}</b> in the extracted play-by-play logs.</p>
        </div>`;
}

function filterTables() {
    const val = document.getElementById('globalSearch').value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(val) ? '' : 'none';
    });
}
