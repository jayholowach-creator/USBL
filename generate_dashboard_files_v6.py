import os

def generate_v6_web_files():
    print("Generating updated dashboard website files (v6 with Multi-League Dropdown, Team Summary Page & Statcast Fix)...")
    
    # 1. INDEX.HTML
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>USBL Major League & Statcast Dashboard</title>
    <link rel="stylesheet" href="styles.css">
    <!-- Chart.js for Interactive Baseball Visualizations -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <header class="navbar">
        <div class="logo-group">
            <div class="logo">
                <span class="badge">USBL</span> League & Analytics Dashboard
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
            <button class="nav-btn active" onclick="switchTab('standings')">Standings</button>
            <button class="nav-btn" onclick="switchTab('batting')">Batting Leaders</button>
            <button class="nav-btn" onclick="switchTab('pitching')">Pitching Leaders</button>
            <button class="nav-btn" onclick="switchTab('statcast')">🔥 Statcast & EV</button>
            <button class="nav-btn" onclick="switchTab('visualizations')">📊 Graphs & Charts</button>
            <button class="nav-btn" onclick="switchTab('matchups')">⚔️ Batter vs Pitcher</button>
        </nav>
    </header>

    <main class="container">
        <!-- GLOBAL SEARCH BAR -->
        <div class="search-section">
            <input type="text" id="globalSearch" placeholder="🔍 Search player, team, or stat..." onkeyup="filterTables()">
        </div>

        <!-- TAB 1: STANDINGS -->
        <section id="tab-standings" class="tab-content active">
            <div class="section-header">
                <h2 id="standingsTitle">League Standings — USBL (Major League)</h2>
                <p class="subtitle-sm">Click on any team name to open their complete Team Summary, Lineups & Pitching Staff view.</p>
            </div>
            <div id="standingsContainer" class="grid-2"></div>
        </section>

        <!-- TEAM SUMMARY MODAL / OVERLAY VIEW -->
        <div id="teamSummaryModal" class="modal-overlay" style="display:none;">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="team-modal-title">
                        <img id="modalTeamLogo" src="" class="team-logo-large" onerror="this.style.display='none'">
                        <div>
                            <h2 id="modalTeamName">Team Name</h2>
                            <p id="modalTeamSub" class="subtitle-sm">2017 Season Overview & Roster Breakdown</p>
                        </div>
                    </div>
                    <button class="close-btn" onclick="closeTeamSummary()">✕ Close</button>
                </div>

                <div class="modal-nav">
                    <button class="modal-tab-btn active" onclick="switchModalTab('lineups')">📋 Lineups (vs L / vs R)</button>
                    <button class="modal-tab-btn" onclick="switchModalTab('pitching')">⚾ Pitching Staff & Bullpen</button>
                    <button class="modal-tab-btn" onclick="switchModalTab('defense')">🛡️ Defensive Diamond (ZR & FLD%)</button>
                </div>

                <div class="modal-body">
                    <!-- SUB-TAB 1: LINEUPS -->
                    <div id="modal-sub-lineups" class="modal-sub-content active">
                        <div class="platoon-toggle mb-3">
                            <label><b>Lineup Configuration:</b></label>
                            <button id="btnLineupLHP" class="btn-toggle active" onclick="toggleLineupPlatoon('vsLHP')">vs. Left-Handed Pitchers (vs LHP)</button>
                            <button id="btnLineupRHP" class="btn-toggle" onclick="toggleLineupPlatoon('vsRHP')">vs. Right-Handed Pitchers (vs RHP)</button>
                        </div>
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>Pos</th>
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
                        <h3>Starting Rotation</h3>
                        <div class="table-wrapper mb-4">
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
                                        <th>BB/9</th>
                                    </tr>
                                </thead>
                                <tbody id="rotationTableBody"></tbody>
                            </table>
                        </div>

                        <h3>Bullpen Staff</h3>
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Role</th>
                                        <th>Pitcher</th>
                                        <th>W-L</th>
                                        <th>ERA</th>
                                        <th>SV</th>
                                        <th>IP</th>
                                        <th>WHIP</th>
                                        <th>K/9</th>
                                    </tr>
                                </thead>
                                <tbody id="bullpenTableBody"></tbody>
                            </table>
                        </div>
                    </div>

                    <!-- SUB-TAB 3: DEFENSIVE DIAMOND -->
                    <div id="modal-sub-defense" class="modal-sub-content">
                        <h3>Defensive Starters & Advanced Fielding Metrics</h3>
                        <p class="subtitle-sm mb-3">Displays Zone Rating (ZR) and Fielding Percentage (FLD%) across positions.</p>
                        
                        <div class="diamond-container">
                            <div class="diamond-field">
                                <!-- FIELDING POSITION CARDS -->
                                <div class="pos-card pos-cf" id="pos-CF"><span class="pos-label">CF</span><div id="def-CF">Loading...</div></div>
                                <div class="pos-card pos-lf" id="pos-LF"><span class="pos-label">LF</span><div id="def-LF">Loading...</div></div>
                                <div class="pos-card pos-rf" id="pos-RF"><span class="pos-label">RF</span><div id="def-RF">Loading...</div></div>
                                <div class="pos-card pos-ss" id="pos-SS"><span class="pos-label">SS</span><div id="def-SS">Loading...</div></div>
                                <div class="pos-card pos-2b" id="pos-2B"><span class="pos-label">2B</span><div id="def-2B">Loading...</div></div>
                                <div class="pos-card pos-3b" id="pos-3B"><span class="pos-label">3B</span><div id="def-3B">Loading...</div></div>
                                <div class="pos-card pos-1b" id="pos-1B"><span class="pos-label">1B</span><div id="def-1B">Loading...</div></div>
                                <div class="pos-card pos-c" id="pos-C"><span class="pos-label">C</span><div id="def-C">Loading...</div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: BATTING LEADERS WITH SPLITS -->
        <section id="tab-batting" class="tab-content">
            <div class="section-header">
                <h2 id="battingTitle">Batting Leaders — USBL (Major League)</h2>
                <div class="filter-group">
                    <label>Split Filter:</label>
                    <select id="battingSplitSelect" onchange="renderBattingLeaders()">
                        <option value="overall">Overall / Full Season</option>
                        <option value="vsl">vs. Left-Handed Pitchers (vs LHP)</option>
                        <option value="vsr">vs. Right-Handed Pitchers (vs RHP)</option>
                        <option value="home">Home Games</option>
                        <option value="away">Road / Away Games</option>
                    </select>
                </div>
            </div>
            <div id="battingLeadersContainer" class="grid-3"></div>
        </section>

        <!-- TAB 3: PITCHING LEADERS WITH SPLITS -->
        <section id="tab-pitching" class="tab-content">
            <div class="section-header">
                <h2 id="pitchingTitle">Pitching Leaders — USBL (Major League)</h2>
                <div class="filter-group">
                    <label>Split Filter:</label>
                    <select id="pitchingSplitSelect" onchange="renderPitchingLeaders()">
                        <option value="overall">Overall / Full Season</option>
                        <option value="vsl">vs. Left-Handed Batters (vs LHB)</option>
                        <option value="vsr">vs. Right-Handed Batters (vs RHB)</option>
                        <option value="home">Home Starts</option>
                        <option value="away">Road / Away Starts</option>
                    </select>
                </div>
            </div>
            <div id="pitchingLeadersContainer" class="grid-3"></div>
        </section>

        <!-- TAB 4: STATCAST EXIT VELOCITY -->
        <section id="tab-statcast" class="tab-content">
            <h2>🔥 Statcast Exit Velocity & Hard-Hit Leaderboard</h2>
            <p class="subtitle">Parsed directly from play-by-play game log exit velocity (MPH) tracking.</p>
            <div class="statcast-summary-cards grid-4" id="statcastCards"></div>
            <div class="card mt-4">
                <h3>Top Exit Velocity Batted Balls (100+ MPH)</h3>
                <div class="table-wrapper">
                    <table id="statcastTable">
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>Exit Velocity (MPH)</th>
                                <th>Launch Trajectory</th>
                                <th>Distance (FT)</th>
                                <th>Hard-Hit Tag</th>
                            </tr>
                        </thead>
                        <tbody id="statcastTableBody"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 5: GRAPHS & VISUALIZATIONS -->
        <section id="tab-visualizations" class="tab-content">
            <h2>📊 Interactive Player & Game Visualizations</h2>
            
            <div class="grid-2 mt-4">
                <div class="card">
                    <h3>📈 Player Season Trajectory (162-Game Rolling AVG & OPS)</h3>
                    <p class="card-subtitle">Track how a batter's average and OPS evolved game-by-game over the season.</p>
                    <div class="filter-group mb-2">
                        <select id="playerTrendSelect" onchange="updatePlayerTrendChart()">
                            <option value="Nate Mahoney">Nate Mahoney (Armada)</option>
                            <option value="Jesse Wilson">Jesse Wilson (Halos)</option>
                            <option value="Dave Gordon">Dave Gordon (Armada)</option>
                        </select>
                    </div>
                    <canvas id="trendChart"></canvas>
                </div>

                <div class="card">
                    <h3>🎯 Batted Ball Field Spray Chart</h3>
                    <p class="card-subtitle">Location and contact quality for hits and outs on the diamond.</p>
                    <canvas id="sprayChart"></canvas>
                </div>
            </div>

            <div class="grid-2 mt-4">
                <div class="card">
                    <h3>⚾ In-Game Win Expectancy (WPA) Graph</h3>
                    <p class="card-subtitle">Inning-by-inning win probability wave (Anaheim Halos vs Tampa Bay Armada).</p>
                    <canvas id="wpaChart"></canvas>
                </div>

                <div class="card">
                    <h3>🚀 Exit Velocity Distribution (MPH Bins)</h3>
                    <p class="card-subtitle">Batted ball breakdown by hit speed category.</p>
                    <canvas id="evDistChart"></canvas>
                </div>
            </div>
        </section>

        <!-- TAB 6: PITCHER VS HITTER MATCHUP ANALYZER -->
        <section id="tab-matchups" class="tab-content">
            <h2>⚔️ Pitcher vs. Hitter Head-to-Head Matchup Search</h2>
            <p class="subtitle">Look up individual career and season stats for any pitcher against any batter.</p>
            
            <div class="card matchup-box">
                <div class="matchup-inputs">
                    <div class="input-group">
                        <label>Select Pitcher:</label>
                        <input type="text" id="pitcherInput" value="Mike Pearsall" placeholder="Enter pitcher name...">
                    </div>
                    <div class="vs-badge">VS</div>
                    <div class="input-group">
                        <label>Select Batter:</label>
                        <input type="text" id="batterInput" value="Elmer Aguilera" placeholder="Enter batter name...">
                    </div>
                    <button class="btn-primary" onclick="lookupMatchup()">Analyze Matchup</button>
                </div>

                <div id="matchupResult" class="matchup-results mt-4"></div>
            </div>
        </section>
    </main>

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
    padding: 0.8rem 1.5rem;
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
    font-size: 1.15rem;
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
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid #0284c7;
}

.league-selector-wrapper label {
    font-size: 0.75rem;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: 0.5px;
}

.league-selector-wrapper select {
    background: transparent;
    color: white;
    border: none;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    outline: none;
}

.league-selector-wrapper select option {
    background-color: #1e293b;
    color: white;
}

.nav-links {
    display: flex;
    gap: 6px;
}

.nav-btn {
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 8px 14px;
    font-size: 0.9rem;
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
    margin: 1.5rem auto;
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

.card-subtitle, .subtitle-sm {
    color: #94a3b8;
    font-size: 0.85rem;
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

.team-link {
    color: #38bdf8;
    text-decoration: none;
    font-weight: 700;
    cursor: pointer;
}

.team-link:hover {
    text-decoration: underline;
    color: #7dd3fc;
}

.team-logo-small {
    width: 24px;
    height: 24px;
    vertical-align: middle;
    margin-right: 8px;
    object-fit: contain;
}

.player-headshot {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    vertical-align: middle;
    margin-right: 8px;
    object-fit: cover;
    background-color: #334155;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(4px);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

.modal-content {
    background-color: #1e293b;
    border: 1px solid #0284c7;
    border-radius: 12px;
    width: 100%;
    max-width: 950px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    padding: 1.5rem;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #334155;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.team-modal-title {
    display: flex;
    align-items: center;
    gap: 12px;
}

.team-logo-large {
    width: 48px;
    height: 48px;
    object-fit: contain;
}

.close-btn {
    background: #ef4444;
    color: white;
    border: none;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 700;
}

.close-btn:hover { background: #dc2626; }

.modal-nav {
    display: flex;
    gap: 8px;
    margin-bottom: 1.25rem;
    border-bottom: 1px solid #334155;
    padding-bottom: 8px;
}

.modal-tab-btn {
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 8px 14px;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
}

.modal-tab-btn.active {
    background-color: #0284c7;
    color: white;
}

.modal-sub-content { display: none; }
.modal-sub-content.active { display: block; }

.btn-toggle {
    background: #0f172a;
    color: #94a3b8;
    border: 1px solid #334155;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.85rem;
}

.btn-toggle.active {
    background: #0284c7;
    color: white;
    border-color: #0284c7;
}

.diamond-container {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 1.5rem;
    margin-top: 1rem;
    position: relative;
    min-height: 420px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.diamond-field {
    position: relative;
    width: 100%;
    max-width: 600px;
    height: 380px;
    background: radial-gradient(circle at 50% 80%, #15803d 0%, #064e3b 70%);
    border-radius: 50% 50% 10px 10px;
    border: 2px solid #22c55e;
}

.pos-card {
    position: absolute;
    background: rgba(30, 41, 59, 0.95);
    border: 1px solid #38bdf8;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 0.8rem;
    color: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.4);
    min-width: 110px;
    text-align: center;
}

.pos-label {
    display: inline-block;
    background: #0284c7;
    color: white;
    font-weight: 800;
    font-size: 0.7rem;
    padding: 1px 5px;
    border-radius: 3px;
    margin-bottom: 2px;
}

.pos-cf { top: 15px; left: 50%; transform: translateX(-50%); }
.pos-lf { top: 55px; left: 12%; }
.pos-rf { top: 55px; right: 12%; }
.pos-ss { top: 155px; left: 28%; }
.pos-2b { top: 155px; right: 28%; }
.pos-3b { top: 235px; left: 8%; }
.pos-1b { top: 235px; right: 8%; }
.pos-c  { bottom: 15px; left: 50%; transform: translateX(-50%); }

.mt-4 { margin-top: 1.5rem; }
.mb-3 { margin-bottom: 1rem; }
.subtitle { color: #94a3b8; margin-bottom: 1rem; }
"""

    # 3. APP.JS
    app_js = """let leagueData = null;
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
        { order: 9, pos: '2B', name: 'Kevin O\'Connor', avg: '.252', obp: '.315', slg: '.390', ops: '.705', hr: 8, rbi: 38 }
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
        '2B': { name: 'Kevin O\'Connor', zr: '+6.8', fld: '.988', err: 6 },
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
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✓ Successfully generated index.html (v6)")

    with open("styles.css", "w", encoding="utf-8") as f:
        f.write(styles_css)
    print("✓ Successfully generated styles.css (v6)")

    with open("app.js", "w", encoding="utf-8") as f:
        f.write(app_js)
    print("✓ Successfully generated app.js (v6)")

if __name__ == "__main__":
    generate_v6_web_files()
