import os

def generate_v8_web_files():
    print("Generating updated dashboard website files (v8 with 100% Strict Real Data — No Fallbacks)...")
    
    # 1. INDEX.HTML
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>USBL Major League & Statcast Analytics</title>
    <link rel="stylesheet" href="styles.css">
    <!-- Chart.js for Interactive Baseball Visualizations -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <header class="navbar">
        <div class="logo-group">
            <div class="logo">
                <span class="badge">USBL</span> Analytics Dashboard
            </div>
            <!-- HEADER LEAGUE SELECTOR DROPDOWN -->
            <div class="league-selector-wrapper">
                <label for="leagueSelect">ACTIVE LEAGUE:</label>
                <select id="leagueSelect" onchange="handleLeagueChange()">
                    <option value="USBL (Major League)" selected>USBL (Major League)</option>
                    <option value="Triple-A (AAA)">Triple-A (AAA)</option>
                    <option value="Double-A (AA)">Double-A (AA)</option>
                    <option value="Class-A (A)">Class-A (A)</option>
                    <option value="Rookie League">Rookie League</option>
                </select>
            </div>
        </div>

        <nav class="nav-links">
            <button class="nav-btn active" onclick="switchTab('standings', event)">Standings</button>
            <button class="nav-btn" onclick="switchTab('batting', event)">Batting Leaders</button>
            <button class="nav-btn" onclick="switchTab('pitching', event)">Pitching Leaders</button>
            <button class="nav-btn" onclick="switchTab('statcast', event)">🔥 Statcast & EV</button>
            <button class="nav-btn" onclick="switchTab('visualizations', event)">📊 Graphs & Charts</button>
            <button class="nav-btn" onclick="switchTab('matchups', event)">⚔️ Batter vs Pitcher</button>
        </nav>
    </header>

    <main class="container">
        <!-- GLOBAL SEARCH BAR -->
        <div class="search-section">
            <input type="text" id="globalSearch" placeholder="🔍 Search player, team, or stat..." onkeyup="filterTables()">
        </div>

        <!-- TAB 1: STANDINGS -->
        <section id="tab-standings" class="tab-content active">
            <h2 id="standingsTitle">League Standings — USBL (Major League)</h2>
            <div id="standingsContainer"></div>
        </section>

        <!-- TAB 2: BATTING LEADERS -->
        <section id="tab-batting" class="tab-content">
            <div class="section-header">
                <h2 id="battingTitle">Batting Leaders — USBL (Major League)</h2>
            </div>
            <div id="battingLeadersContainer" class="grid-3"></div>
        </section>

        <!-- TAB 3: PITCHING LEADERS -->
        <section id="tab-pitching" class="tab-content">
            <div class="section-header">
                <h2 id="pitchingTitle">Pitching Leaders — USBL (Major League)</h2>
            </div>
            <div id="pitchingLeadersContainer" class="grid-3"></div>
        </section>

        <!-- TAB 4: STATCAST EXIT VELOCITY -->
        <section id="tab-statcast" class="tab-content">
            <h2>🔥 Statcast Exit Velocity & Batted Ball Leaderboard</h2>
            <p class="subtitle">Parsed directly from play-by-play game log exit velocity (MPH) tracking.</p>
            <div class="statcast-summary-cards grid-4" id="statcastCards"></div>
            <div class="card mt-4">
                <h3>Top Exit Velocity Batted Balls</h3>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>Exit Velocity</th>
                                <th>Batted Ball Type</th>
                                <th>Distance</th>
                                <th>Classification</th>
                            </tr>
                        </thead>
                        <tbody id="statcastTableBody"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 5: VISUALIZATIONS -->
        <section id="tab-visualizations" class="tab-content">
            <h2>📊 Interactive Player & Game Visualizations</h2>
            
            <div class="grid-2 mt-4">
                <!-- CHART 1: SEASON TREND -->
                <div class="card">
                    <h3>📈 Player Season Trajectory</h3>
                    <p class="card-subtitle">Track player performance trends over the course of the season.</p>
                    <div class="filter-group mb-2">
                        <select id="playerTrendSelect" onchange="updatePlayerTrendChart()">
                            <option value="">-- Select Player --</option>
                        </select>
                    </div>
                    <canvas id="trendChart"></canvas>
                    <div id="trendChartNote" class="no-data mt-2" style="display:none;">No game-by-game trend logs found for this player in the extracted dataset.</div>
                </div>

                <!-- CHART 2: SPRAY CHART -->
                <div class="card">
                    <h3>🎯 Batted Ball Field Spray Chart</h3>
                    <p class="card-subtitle">Location and contact quality for hits on the diamond.</p>
                    <canvas id="sprayChart"></canvas>
                    <div id="sprayChartNote" class="no-data mt-2" style="display:none;">No spray chart distance coordinates available in the current dataset.</div>
                </div>
            </div>

            <div class="grid-2 mt-4">
                <!-- CHART 3: WIN PROBABILITY ADDED -->
                <div class="card">
                    <h3>⚾ In-Game Win Expectancy (WPA) Graph</h3>
                    <p class="card-subtitle">Inning-by-inning win probability wave from play-by-play game logs.</p>
                    <canvas id="wpaChart"></canvas>
                    <div id="wpaChartNote" class="no-data mt-2" style="display:none;">No in-game WPA win probability logs found in the current dataset.</div>
                </div>

                <!-- CHART 4: EXIT VELOCITY HISTOGRAM -->
                <div class="card">
                    <h3>🚀 Exit Velocity Distribution</h3>
                    <p class="card-subtitle">Batted ball breakdown by hit speed category.</p>
                    <canvas id="evDistChart"></canvas>
                    <div id="evDistChartNote" class="no-data mt-2" style="display:none;">No exit velocity distribution data available in the current dataset.</div>
                </div>
            </div>
        </section>

        <!-- TAB 6: PITCHER VS HITTER MATCHUP ANALYZER -->
        <section id="tab-matchups" class="tab-content">
            <h2>⚔️ Pitcher vs. Hitter Head-to-Head Matchup Search</h2>
            <p class="subtitle">Look up head-to-head stats for any pitcher against any batter in the extracted dataset.</p>
            
            <div class="card matchup-box">
                <div class="matchup-inputs">
                    <div class="input-group">
                        <label>Pitcher Name:</label>
                        <input type="text" id="pitcherInput" placeholder="Enter pitcher name...">
                    </div>
                    <div class="vs-badge">VS</div>
                    <div class="input-group">
                        <label>Batter Name:</label>
                        <input type="text" id="batterInput" placeholder="Enter batter name...">
                    </div>
                    <button class="btn-primary" onclick="lookupMatchup()">Analyze Matchup</button>
                </div>

                <div id="matchupResult" class="matchup-results mt-4"></div>
            </div>
        </section>
    </main>

    <!-- TEAM SUMMARY MODAL WINDOW -->
    <div id="teamSummaryModal" class="modal-overlay" style="display: none;">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title-group">
                    <img id="modalTeamLogo" src="" class="team-logo-medium" onerror="this.style.display='none';">
                    <h2 id="modalTeamName">Team Summary</h2>
                </div>
                <button class="close-btn" onclick="closeTeamSummary()">✕</button>
            </div>

            <!-- MODAL SUB-TABS -->
            <div class="modal-nav">
                <button class="modal-tab-btn active" onclick="switchModalTab('lineups')">📋 Roster & Lineups</button>
                <button class="modal-tab-btn" onclick="switchModalTab('pitching')">⚾ Pitching Staff</button>
                <button class="modal-tab-btn" onclick="switchModalTab('defense')">🛡️ Defensive Ratings</button>
            </div>

            <!-- SUB-TAB 1: LINEUPS -->
            <div id="modal-sub-lineups" class="modal-sub-content active">
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>POS</th>
                                <th>Player</th>
                                <th>AVG</th>
                                <th>OBP</th>
                                <th>SLG</th>
                                <th>OPS</th>
                                <th>HR</th>
                                <th>RBI</th>
                            </tr>
                        </thead>
                        <tbody id="lineupTableBody"></tbody>
                    </table>
                </div>
            </div>

            <!-- SUB-TAB 2: PITCHING STAFF -->
            <div id="modal-sub-pitching" class="modal-sub-content">
                <h3>Pitching Staff Statistics</h3>
                <div class="table-wrapper mt-2">
                    <table>
                        <thead>
                            <tr>
                                <th>Role</th>
                                <th>Pitcher</th>
                                <th>W-L</th>
                                <th>ERA</th>
                                <th>IP</th>
                                <th>WHIP</th>
                                <th>K/9</th>
                                <th>SV</th>
                            </tr>
                        </thead>
                        <tbody id="pitchingStaffTableBody"></tbody>
                    </table>
                </div>
            </div>

            <!-- SUB-TAB 3: DEFENSIVE RATINGS -->
            <div id="modal-sub-defense" class="modal-sub-content">
                <h3>Defensive Metrics & Ratings</h3>
                <div class="table-wrapper mt-2">
                    <table>
                        <thead>
                            <tr>
                                <th>POS</th>
                                <th>Player</th>
                                <th>Zone Rating (ZR)</th>
                                <th>Fielding % (FLD%)</th>
                                <th>Errors</th>
                            </tr>
                        </thead>
                        <tbody id="defenseTableBody"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script src="app.js"></script>
</body>
</html>"""

    # 2. STYLES.CSS
    styles_css = """* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

body {
    background-color: #0f172a;
    color: #f8fafc;
    line-height: 1.5;
    padding-bottom: 50px;
}

.navbar {
    background-color: #1e293b;
    border-bottom: 1px solid #334155;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
    flex-wrap: wrap;
    gap: 1rem;
}

.logo-group {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.logo {
    font-size: 1.25rem;
    font-weight: 700;
    color: #38bdf8;
}

.badge {
    background-color: #0284c7;
    color: white;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-right: 6px;
}

.league-selector-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: #0f172a;
    padding: 6px 12px;
    border-radius: 8px;
    border: 1px solid #334155;
}

.league-selector-wrapper label {
    font-size: 0.8rem;
    font-weight: 700;
    color: #38bdf8;
}

.league-selector-wrapper select {
    background: transparent;
    color: #f8fafc;
    border: none;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    outline: none;
}

.nav-links {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.nav-btn {
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 8px 16px;
    font-size: 0.95rem;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.nav-btn:hover {
    color: #f8fafc;
    background-color: #334155;
}

.nav-btn.active {
    color: white;
    background-color: #0284c7;
}

.container {
    max-width: 1300px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.search-section {
    margin-bottom: 1.5rem;
}

#globalSearch {
    width: 100%;
    padding: 12px 18px;
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    color: white;
    font-size: 1rem;
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
    gap: 1.5rem;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
    gap: 1.5rem;
}

.grid-4 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.2rem;
}

.card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 1.25rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}

.card h3 {
    color: #38bdf8;
    font-size: 1.1rem;
    margin-bottom: 0.25rem;
}

.card-subtitle {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.2rem;
}

.table-wrapper {
    overflow-x: auto;
    margin-top: 0.75rem;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    text-align: left;
}

th {
    background-color: #0f172a;
    color: #38bdf8;
    padding: 10px;
    border-bottom: 2px solid #334155;
}

td {
    padding: 8px 10px;
    border-bottom: 1px solid #334155;
}

tr:hover {
    background-color: #2b394e;
}

.team-cell, .player-cell {
    display: flex;
    align-items: center;
    gap: 10px;
}

.team-logo-small {
    width: 24px;
    height: 24px;
    object-fit: contain;
}

.team-logo-medium {
    width: 36px;
    height: 36px;
    object-fit: contain;
}

.player-headshot {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    object-fit: cover;
    background-color: #334155;
}

.team-link {
    color: #38bdf8;
    cursor: pointer;
    text-decoration: underline;
    font-weight: 600;
}

.team-link:hover {
    color: #7dd3fc;
}

.btn-primary {
    background-color: #0284c7;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
}

.btn-primary:hover {
    background-color: #0369a1;
}

/* MODAL WINDOW STYLES */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(4px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    width: 90%;
    max-width: 950px;
    max-height: 85vh;
    overflow-y: auto;
    padding: 1.5rem;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #334155;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.modal-title-group {
    display: flex;
    align-items: center;
    gap: 12px;
}

.close-btn {
    background: transparent;
    border: none;
    color: #94a3b8;
    font-size: 1.5rem;
    cursor: pointer;
}

.close-btn:hover {
    color: #ef4444;
}

.modal-nav {
    display: flex;
    gap: 8px;
    margin-bottom: 1rem;
    border-bottom: 1px solid #334155;
    padding-bottom: 8px;
}

.modal-tab-btn {
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 6px 14px;
    font-size: 0.9rem;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
}

.modal-tab-btn.active {
    background-color: #0284c7;
    color: white;
}

.modal-sub-content {
    display: none;
}

.modal-sub-content.active {
    display: block;
}

.matchup-inputs {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.input-group label {
    display: block;
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 4px;
}

.input-group input {
    background-color: #0f172a;
    border: 1px solid #334155;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.95rem;
}

.vs-badge {
    background-color: #ef4444;
    color: white;
    font-weight: 800;
    padding: 6px 12px;
    border-radius: 50%;
    font-size: 0.9rem;
}

.no-data {
    color: #94a3b8;
    font-style: italic;
    padding: 1rem 0;
}

.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1.5rem; }
.mb-2 { margin-bottom: 0.75rem; }
.subtitle { color: #94a3b8; margin-bottom: 1rem; }
"""

    # 3. APP.JS
    app_js = """let leagueData = null;
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
                    <a class="team-link" onclick="openTeamSummary('${teamName.replace(/'/g, "\\'")}')">${teamName}</a>
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
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✓ Successfully generated index.html (v8)")

    with open("styles.css", "w", encoding="utf-8") as f:
        f.write(styles_css)
    print("✓ Successfully generated styles.css (v8)")

    with open("app.js", "w", encoding="utf-8") as f:
        f.write(app_js)
    print("✓ Successfully generated app.js (v8)")

if __name__ == "__main__":
    generate_v8_web_files()
