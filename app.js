let leagueData = null;
let currentSelectedTeam = null;
let currentStandingsSubTab = 'division';

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
                <p>Could not load <b>usbl_league_data.json</b>. Make sure you ran <b>export_league_data_v24.py</b> and uploaded the output JSON file to GitHub Pages.</p>
            </div>`;
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

function switchStandingsSubTab(sub) {
    currentStandingsSubTab = sub;
    renderStandings();
}

function switchTxSubTab(subKey) {
    document.querySelectorAll('.tx-sub-content').forEach(el => el.classList.remove('active'));
    const target = document.getElementById('tx-sub-' + subKey);
    if (target) target.classList.add('active');
}

function initDashboard() {
    populatePlayerSelectOptions();
    renderStandings();
    renderBattingLeaders();
    renderPitchingLeaders();
    renderStatcast();
    renderTransactions();
    renderFreeAgents();
    renderHistoryAwards();
    renderProspects();
}

function populatePlayerSelectOptions() {
    const select = document.getElementById('playerTrendSelect');
    if (!select) return;

    select.innerHTML = '<option value="">-- Select Player --</option>';
    let batList = (leagueData && leagueData.batting_leaders) ? leagueData.batting_leaders : [];

    batList.forEach(p => {
        const pName = p.Player || p.Name;
        if (pName) {
            const opt = document.createElement('option');
            opt.value = pName;
            opt.textContent = `${pName} (${p.Team || 'Team'})`;
            select.appendChild(opt);
        }
    });
}

function renderStandings() {
    const container = document.getElementById('standingsContainer');
    if (!container) return;

    let standingsList = (currentStandingsSubTab === 'wildcard') 
        ? ((leagueData && leagueData.wildcard_standings) ? leagueData.wildcard_standings : [])
        : ((leagueData && leagueData.standings) ? leagueData.standings : []);

    if (!standingsList || standingsList.length === 0) {
        container.innerHTML = `<div class="card"><p class="no-data">No standings data found in usbl_league_data.json for USBL Major League.</p></div>`;
        return;
    }

    let rowsHtml = standingsList.map(row => {
        const teamName = row.Team || row.TEAM || row.Tm || "Team";
        const w = row.W || row.w || "0";
        const l = row.L || row.l || "0";
        const pct = row.PCT || row.pct || ".000";
        const gb = row.GB || row.gb || "-";
        const wcgb = row.WCGB || "-";
        const home = row.HOME || "0-0";
        const away = row.AWAY || "0-0";
        const l10 = row.L10 || "0-0";
        const streak = row.STREAK || "W1";
        const logo = row.logo_url || `images/team_logos/${teamName.toLowerCase().replace(/[^a-z0-9]/g, '_')}.png`;

        return `
            <tr>
                <td class="team-cell">
                    <img src="${logo}" class="team-logo-small" onerror="this.style.display='none'">
                    <a class="team-link" onclick="openTeamSummary('${teamName.replace(/'/g, "\\'")}')">${teamName}</a>
                </td>
                <td>${w}</td>
                <td>${l}</td>
                <td><b>${pct}</b></td>
                <td>${gb}</td>
                <td>${wcgb}</td>
                <td>${home}</td>
                <td>${away}</td>
                <td>${l10}</td>
                <td>${streak}</td>
            </tr>
        `;
    }).join('');

    container.innerHTML = `
        <div class="card">
            <h3>USBL Major League ${currentStandingsSubTab === 'wildcard' ? 'Wild Card Race' : 'Division Standings'}</h3>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Team</th>
                            <th>W</th>
                            <th>L</th>
                            <th>PCT</th>
                            <th>GB</th>
                            <th>WCGB</th>
                            <th>Home</th>
                            <th>Away</th>
                            <th>L10</th>
                            <th>Streak</th>
                        </tr>
                    </thead>
                    <tbody>${rowsHtml}</tbody>
                </table>
            </div>
        </div>`;
}

function renderBattingLeaders() {
    const container = document.getElementById('battingLeadersContainer');
    if (!container) return;

    let batList = (leagueData && leagueData.batting_leaders) ? leagueData.batting_leaders : [];

    if (!batList || batList.length === 0) {
        container.innerHTML = `<div class="card"><p class="no-data">No batting statistics extracted for Major League.</p></div>`;
        return;
    }

    const sortedBatters = [...batList].sort((a, b) => parseFloat(b.AVG || 0) - parseFloat(a.AVG || 0));

    let rowsHtml = sortedBatters.map((p, idx) => `
        <tr>
            <td>${idx + 1}</td>
            <td class="player-cell">
                <img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                <a class="player-link" onclick="openPlayerProfile('${(p.Player || 'Player').replace(/'/g, "\\'")}')">${p.Player || "Player"}</a>
            </td>
            <td>${p.Team || "-"}</td>
            <td>${p.AB || "0"}</td>
            <td>${p.H || "0"}</td>
            <td>${p.HR || "0"}</td>
            <td>${p.RBI || "0"}</td>
            <td><b>${p.AVG || ".000"}</b></td>
            <td>${p.OBP || ".000"}</td>
            <td>${p.SLG || ".000"}</td>
        </tr>
    `).join('');

    container.innerHTML = `
        <div class="card">
            <h3>Major League Batting Leaders</h3>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Player</th>
                            <th>Team</th>
                            <th>AB</th>
                            <th>H</th>
                            <th>HR</th>
                            <th>RBI</th>
                            <th>AVG</th>
                            <th>OBP</th>
                            <th>SLG</th>
                        </tr>
                    </thead>
                    <tbody>${rowsHtml}</tbody>
                </table>
            </div>
        </div>`;
}

function renderPitchingLeaders() {
    const container = document.getElementById('pitchingLeadersContainer');
    if (!container) return;

    let pitchList = (leagueData && leagueData.pitching_leaders) ? leagueData.pitching_leaders : [];

    if (!pitchList || pitchList.length === 0) {
        container.innerHTML = `<div class="card"><p class="no-data">No pitching statistics extracted for Major League.</p></div>`;
        return;
    }

    const sortedPitchers = [...pitchList].sort((a, b) => parseFloat(a.ERA || 99) - parseFloat(b.ERA || 99));

    let rowsHtml = sortedPitchers.map((p, idx) => `
        <tr>
            <td>${idx + 1}</td>
            <td class="player-cell">
                <img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                <a class="player-link" onclick="openPlayerProfile('${(p.Player || 'Pitcher').replace(/'/g, "\\'")}')">${p.Player || "Pitcher"}</a>
            </td>
            <td>${p.Team || "-"}</td>
            <td>${p.W || "0"}-${p.L || "0"}</td>
            <td><b>${p.ERA || "0.00"}</b></td>
            <td>${p.IP || "0.0"}</td>
            <td>${p.WHIP || "0.00"}</td>
            <td>${p.K9 || "0.0"}</td>
            <td>${p.SV || "0"}</td>
        </tr>
    `).join('');

    container.innerHTML = `
        <div class="card">
            <h3>Major League Pitching Leaders</h3>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Pitcher</th>
                            <th>Team</th>
                            <th>W-L</th>
                            <th>ERA</th>
                            <th>IP</th>
                            <th>WHIP</th>
                            <th>K/9</th>
                            <th>SV</th>
                        </tr>
                    </thead>
                    <tbody>${rowsHtml}</tbody>
                </table>
            </div>
        </div>`;
}

function renderStatcast() {
    const cards = document.getElementById('statcastCards');
    const tbody = document.getElementById('statcastTableBody');

    let scData = (leagueData && leagueData.statcast_data) ? leagueData.statcast_data : null;

    if (cards) {
        if (scData && scData.summary && scData.summary.max_ev !== null) {
            cards.innerHTML = `
                <div class="card"><h3>Max Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#ef4444;font-weight:bold;">${scData.summary.max_ev} MPH</p><p>${scData.summary.max_ev_player || "-"}</p></div>
                <div class="card"><h3>Hard-Hit % (95+ MPH)</h3><p class="subtitle" style="font-size:1.5rem;color:#f59e0b;font-weight:bold;">${scData.summary.hard_hit_pct}%</p><p>League Batted Balls</p></div>
                <div class="card"><h3>Avg Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#10b981;font-weight:bold;">${scData.summary.avg_ev} MPH</p><p>All Field Events</p></div>
                <div class="card"><h3>Batted Balls Tracked</h3><p class="subtitle" style="font-size:1.5rem;color:#38bdf8;font-weight:bold;">${scData.summary.total_batted_balls}</p><p>Play-by-Play Logs</p></div>`;
        } else {
            cards.innerHTML = `<div class="card" style="grid-column: 1 / -1;"><p class="no-data">No Statcast play-by-play exit velocity logs found in OOTP Almanac files.</p></div>`;
        }
    }

    if (tbody) {
        if (scData && scData.leaderboard && scData.leaderboard.length > 0) {
            tbody.innerHTML = scData.leaderboard.slice(0, 25).map(b => `
                <tr>
                    <td><img src="${b.headshot_url}" class="player-headshot" onerror="this.src='images/players/default.png'"><a class="player-link" onclick="openPlayerProfile('${b.player.replace(/'/g, "\\'")}')">${b.player}</a></td>
                    <td><b>${b.ev} MPH</b></td>
                    <td>${b.trajectory}</td>
                    <td>${b.distance ? b.distance + ' FT' : '-'}</td>
                    <td>${b.is_hard_hit ? '<span class="badge" style="background:#ef4444;">🔥 Hard-Hit</span>' : '<span class="badge" style="background:#64748b;">Standard</span>'}</td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = `<tr><td colspan="5" class="no-data">No Statcast Exit Velocity records parsed from OOTP game logs.</td></tr>`;
        }
    }
}

function renderTransactions() {
    const container = document.getElementById('transactionsContainer');
    if (!container) return;

    let txList = (leagueData && leagueData.transactions) ? leagueData.transactions : [];

    if (!txList || txList.length === 0) {
        container.innerHTML = `<p class="no-data">No recent transactions or trades extracted from OOTP Almanac files.</p>`;
        return;
    }

    container.innerHTML = txList.slice(0, 25).map(tx => `
        <div style="border-bottom: 1px solid #334155; padding: 8px 0;">
            <span class="badge" style="background:#0284c7;">${tx.date || '2017'}</span> ${tx.details}
        </div>
    `).join('');
}

function renderFreeAgents() {
    const tbody = document.getElementById('freeAgentsTableBody');
    if (!tbody) return;

    let faList = (leagueData && leagueData.free_agents) ? leagueData.free_agents : [];

    if (!faList || faList.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="no-data">No available free agents parsed from OOTP Almanac.</td></tr>`;
        return;
    }

    tbody.innerHTML = faList.slice(0, 30).map(fa => `
        <tr>
            <td class="player-cell">
                <img src="${fa.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                <a class="player-link" onclick="openPlayerProfile('${(fa.Player || fa.Name || 'Player').replace(/'/g, "\\'")}')">${fa.Player || fa.Name || "Player"}</a>
            </td>
            <td>${fa.POS || fa.Pos || "UT"}</td>
            <td>${fa.Age || "28"}</td>
            <td>${fa.PrevTeam || fa.Team || "Free Agent"}</td>
            <td><b>${fa.Salary || "$1,500,000"}</b></td>
            <td>${fa.Notes || "Available"}</td>
        </tr>
    `).join('');
}

function renderHistoryAwards() {
    const champs = document.getElementById('championsContainer');
    const mvps = document.getElementById('mvpContainer');

    if (champs) champs.innerHTML = `<p class="no-data">No historical World Series champions extracted from OOTP Almanac.</p>`;
    if (mvps) mvps.innerHTML = `<p class="no-data">No historical award winner records parsed from OOTP Almanac.</p>`;
}

function renderProspects() {
    const container = document.getElementById('prospectsContainer');
    if (!container) return;

    container.innerHTML = `<div class="card"><p class="no-data">No top prospects data extracted from OOTP Almanac files.</p></div>`;
}

function openPlayerProfile(playerName) {
    const modal = document.getElementById('playerProfileModal');
    const nameEl = document.getElementById('playerName');
    const teamPosEl = document.getElementById('playerTeamPos');
    const headshotEl = document.getElementById('playerHeadshot');
    const highlightGrid = document.getElementById('playerCardHighlightGrid');
    const headerEl = document.getElementById('playerStatsHeader');
    const bodyEl = document.getElementById('playerStatsBody');

    if (nameEl) nameEl.innerText = playerName;

    let pData = null;
    let isPitcher = false;

    if (leagueData && leagueData.batting_leaders) {
        pData = leagueData.batting_leaders.find(p => (p.Player || "").toLowerCase() === playerName.toLowerCase());
    }
    if (!pData && leagueData && leagueData.pitching_leaders) {
        pData = leagueData.pitching_leaders.find(p => (p.Player || "").toLowerCase() === playerName.toLowerCase());
        if (pData) isPitcher = true;
    }

    if (headshotEl) {
        headshotEl.src = (pData && pData.headshot_url) ? pData.headshot_url : 'images/players/default.png';
    }

    if (teamPosEl) {
        teamPosEl.innerText = pData ? `${pData.Team || 'Free Agent'} • ${isPitcher ? 'Pitcher' : 'Position Player'}` : 'USBL Major League Player';
    }

    if (highlightGrid && pData) {
        if (!isPitcher) {
            highlightGrid.innerHTML = `
                <div class="stat-box"><div class="stat-box-title">Batting Avg (AVG)</div><div class="stat-box-val">${pData.AVG || '.000'}</div></div>
                <div class="stat-box"><div class="stat-box-title">Home Runs (HR)</div><div class="stat-box-val" style="color:#ef4444;">${pData.HR || '0'}</div></div>
                <div class="stat-box"><div class="stat-box-title">Runs Batted In (RBI)</div><div class="stat-box-val" style="color:#f59e0b;">${pData.RBI || '0'}</div></div>
                <div class="stat-box"><div class="stat-box-title">On-Base + Slg (OPS)</div><div class="stat-box-val" style="color:#10b981;">${pData.OPS || '.000'}</div></div>`;
        } else {
            highlightGrid.innerHTML = `
                <div class="stat-box"><div class="stat-box-title">Earned Run Avg (ERA)</div><div class="stat-box-val">${pData.ERA || '0.00'}</div></div>
                <div class="stat-box"><div class="stat-box-title">Win-Loss Record</div><div class="stat-box-val" style="color:#38bdf8;">${pData.W || '0'}-${pData.L || '0'}</div></div>
                <div class="stat-box"><div class="stat-box-title">Innings Pitched (IP)</div><div class="stat-box-val" style="color:#f59e0b;">${pData.IP || '0.0'}</div></div>
                <div class="stat-box"><div class="stat-box-title">WHIP</div><div class="stat-box-val" style="color:#10b981;">${pData.WHIP || '0.00'}</div></div>`;
        }
    }

    if (headerEl && bodyEl && pData) {
        if (!isPitcher) {
            headerEl.innerHTML = `<tr><th>G</th><th>AB</th><th>R</th><th>H</th><th>2B</th><th>3B</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th><th>SB</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th></tr>`;
            bodyEl.innerHTML = `<tr><td>${pData.G||"150"}</td><td>${pData.AB||"0"}</td><td>${pData.R||"0"}</td><td>${pData.H||"0"}</td><td>${pData['2B']||"0"}</td><td>${pData['3B']||"0"}</td><td><b>${pData.HR||"0"}</b></td><td><b>${pData.RBI||"0"}</b></td><td>${pData.BB||"0"}</td><td>${pData.SO||"0"}</td><td>${pData.SB||"0"}</td><td><b>${pData.AVG||".000"}</b></td><td>${pData.OBP||".000"}</td><td>${pData.SLG||".000"}</td><td><b>${pData.OPS||".000"}</b></td></tr>`;
        } else {
            headerEl.innerHTML = `<tr><th>W</th><th>L</th><th>ERA</th><th>G</th><th>GS</th><th>SV</th><th>IP</th><th>H</th><th>R</th><th>ER</th><th>HR</th><th>BB</th><th>SO</th><th>WHIP</th><th>K/9</th></tr>`;
            bodyEl.innerHTML = `<tr><td>${pData.W||"0"}</td><td>${pData.L||"0"}</td><td><b>${pData.ERA||"0.00"}</b></td><td>${pData.G||"30"}</td><td>${pData.GS||"30"}</td><td>${pData.SV||"0"}</td><td>${pData.IP||"0.0"}</td><td>${pData.H||"0"}</td><td>${pData.R||"0"}</td><td>${pData.ER||"0"}</td><td>${pData.HR||"0"}</td><td>${pData.BB||"0"}</td><td>${pData.SO||"0"}</td><td>${pData.WHIP||"0.00"}</td><td>${pData.K9||"0.0"}</td></tr>`;
        }
    }

    if (modal) modal.style.display = 'flex';
}

function closePlayerProfile() {
    const modal = document.getElementById('playerProfileModal');
    if (modal) modal.style.display = 'none';
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
    if (leagueData && leagueData.batting_leaders) {
        teamHitters = leagueData.batting_leaders.filter(p => {
            const tm = (p.Team || "").toLowerCase();
            return tm && currentSelectedTeam.toLowerCase().includes(tm);
        });
    }

    if (!teamHitters || teamHitters.length === 0) {
        tbody.innerHTML = `<tr><td colspan="10" class="no-data">No roster or batting stats extracted for ${currentSelectedTeam}.</td></tr>`;
        return;
    }

    tbody.innerHTML = teamHitters.map((p, idx) => `
        <tr>
            <td>${idx + 1}</td>
            <td class="player-cell">
                <img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                <a class="player-link" onclick="openPlayerProfile('${(p.Player || 'Player').replace(/'/g, "\\'")}')">${p.Player || "Player"}</a>
            </td>
            <td>${p.AB || "0"}</td>
            <td>${p.H || "0"}</td>
            <td>${p.HR || "0"}</td>
            <td>${p.RBI || "0"}</td>
            <td><b>${p.AVG || ".000"}</b></td>
            <td>${p.OBP || ".000"}</td>
            <td>${p.SLG || ".000"}</td>
            <td>${p.OPS || ".000"}</td>
        </tr>
    `).join('');
}

function renderTeamPitching() {
    const tbody = document.getElementById('pitchingStaffTableBody');
    if (!tbody) return;

    let teamPitchers = [];
    if (leagueData && leagueData.pitching_leaders) {
        teamPitchers = leagueData.pitching_leaders.filter(p => {
            const tm = (p.Team || "").toLowerCase();
            return tm && currentSelectedTeam.toLowerCase().includes(tm);
        });
    }

    if (!teamPitchers || teamPitchers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="no-data">No pitching staff statistics extracted for ${currentSelectedTeam}.</td></tr>`;
        return;
    }

    tbody.innerHTML = teamPitchers.map((p, idx) => `
        <tr>
            <td>${idx < 5 ? 'SP' + (idx + 1) : 'RP'}</td>
            <td class="player-cell">
                <img src="${p.headshot_url || 'images/players/default.png'}" class="player-headshot" onerror="this.src='images/players/default.png'">
                <a class="player-link" onclick="openPlayerProfile('${(p.Player || 'Pitcher').replace(/'/g, "\\'")}')">${p.Player || "Pitcher"}</a>
            </td>
            <td>${p.W || "0"}-${p.L || "0"}</td>
            <td><b>${p.ERA || "0.00"}</b></td>
            <td>${p.IP || "0.0"}</td>
            <td>${p.WHIP || "0.00"}</td>
            <td>${p.K9 || "0.0"}</td>
            <td>${p.SV || "0"}</td>
        </tr>
    `).join('');
}

function renderTeamDefense() {
    let teamHitters = [];
    if (leagueData && leagueData.batting_leaders) {
        teamHitters = leagueData.batting_leaders.filter(p => {
            const tm = (p.Team || "").toLowerCase();
            return tm && currentSelectedTeam.toLowerCase().includes(tm);
        });
    }

    const posMap = { 'c': 'def-c-name', '1b': 'def-1b-name', '2b': 'def-2b-name', '3b': 'def-3b-name', 'ss': 'def-ss-name', 'lf': 'def-lf-name', 'cf': 'def-cf-name', 'rf': 'def-rf-name' };
    
    if (teamHitters && teamHitters.length >= 8) {
        const positions = ['Catcher', '1st Base', '2nd Base', '3rd Base', 'Shortstop', 'Left Field', 'Center Field', 'Right Field'];
        const keys = ['c', '1b', '2b', '3b', 'ss', 'lf', 'cf', 'rf'];
        keys.forEach((k, idx) => {
            const el = document.getElementById(posMap[k]);
            if (el && teamHitters[idx]) {
                el.innerText = teamHitters[idx].Player || positions[idx];
            }
        });
    }
}

function filterTables() {
    const val = document.getElementById('globalSearch').value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(val) ? '' : 'none';
    });
}
