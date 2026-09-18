import os

def generate_dashboard_files_v18():
    print("Generating updated dashboard website files (v17 - Sprint 2 Complete Feature Set & Free Agents)...")
    
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>USBL Major League Analytics Dashboard</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <header class="navbar">
        <div class="logo-group">
            <div class="logo">
                <span class="badge">USBL</span> Major League Analytics
            </div>
        </div>

        <nav class="nav-links">
            <button class="nav-btn active" onclick="switchTab('standings', event)">Standings & Wild Card</button>
            <button class="nav-btn" onclick="switchTab('batting', event)">Batting Leaders</button>
            <button class="nav-btn" onclick="switchTab('pitching', event)">Pitching Leaders</button>
            <button class="nav-btn" onclick="switchTab('statcast', event)">🔥 Statcast & EV</button>
            <button class="nav-btn" onclick="switchTab('transactions', event)">📰 Transactions & Free Agents</button>
            <button class="nav-btn" onclick="switchTab('history', event)">🏆 History & Awards</button>
            <button class="nav-btn" onclick="switchTab('prospects', event)">⭐ Top Prospects</button>
            <button class="nav-btn" onclick="switchTab('visualizations', event)">📊 Graphs & Charts</button>
            <button class="nav-btn" onclick="switchTab('matchups', event)">⚔️ Matchups</button>
        </nav>
    </header>

    <main class="container">
        <!-- GLOBAL SEARCH BAR -->
        <div class="search-section">
            <input type="text" id="globalSearch" placeholder="🔍 Search player, team, trade, or stat..." onkeyup="filterTables()">
        </div>

        <!-- TAB 1: STANDINGS & WILD CARD -->
        <section id="tab-standings" class="tab-content active">
            <h2>USBL Major League Standings & Playoff Race</h2>
            <div class="modal-nav mt-2">
                <button class="modal-tab-btn active" onclick="switchStandingsSubTab('division')">Division Standings</button>
                <button class="modal-tab-btn" onclick="switchStandingsSubTab('wildcard')">Wild Card Race</button>
            </div>
            <div id="standingsContainer" class="grid-1 mt-2"></div>
        </section>

        <!-- TAB 2: BATTING LEADERS -->
        <section id="tab-batting" class="tab-content">
            <h2>Major League Batting Leaders</h2>
            <div id="battingLeadersContainer" class="mt-2"></div>
        </section>

        <!-- TAB 3: PITCHING LEADERS -->
        <section id="tab-pitching" class="tab-content">
            <h2>Major League Pitching Leaders</h2>
            <div id="pitchingLeadersContainer" class="mt-2"></div>
        </section>

        <!-- TAB 4: STATCAST & EV -->
        <section id="tab-statcast" class="tab-content">
            <h2>🔥 Statcast Exit Velocity & Hard-Hit Leaderboard</h2>
            <div id="statcastCards" class="grid-4 mt-2"></div>
            <div class="card mt-4">
                <h3>Top Exit Velocity Batted Balls</h3>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>Exit Velocity</th>
                                <th>Trajectory</th>
                                <th>Distance</th>
                                <th>Hard-Hit Status</th>
                            </tr>
                        </thead>
                        <tbody id="statcastTableBody"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 5: TRANSACTIONS, TRADES & FREE AGENTS -->
        <section id="tab-transactions" class="tab-content">
            <h2>📰 League Transactions, Trades & Available Free Agents</h2>
            <div class="modal-nav mt-2">
                <button class="modal-tab-btn active" onclick="switchTxSubTab('trades')">Recent Trades & Signings</button>
                <button class="modal-tab-btn" onclick="switchTxSubTab('free_agents')">Available Free Agents</button>
                <button class="modal-tab-btn" onclick="switchTxSubTab('injured')">Injured List (IL)</button>
            </div>

            <!-- SUB-TAB 1: TRADES -->
            <div id="tx-sub-trades" class="tx-sub-content active mt-2">
                <div class="card">
                    <h3>Recent Transactions & Waiver Claims</h3>
                    <div id="transactionsContainer" class="mt-2"></div>
                </div>
            </div>

            <!-- SUB-TAB 2: FREE AGENTS -->
            <div id="tx-sub-free_agents" class="tx-sub-content mt-2">
                <div class="card">
                    <h3>Available Free Agents Table</h3>
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Player</th>
                                    <th>POS</th>
                                    <th>Age</th>
                                    <th>Prev Team</th>
                                    <th>Expected Salary</th>
                                    <th>Ratings / Notes</th>
                                </tr>
                            </thead>
                            <tbody id="freeAgentsTableBody"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- SUB-TAB 3: INJURED LIST -->
            <div id="tx-sub-injured" class="tx-sub-content mt-2">
                <div class="card">
                    <h3>Injured List (IL) Status</h3>
                    <div id="injuredListContainer" class="mt-2"></div>
                </div>
            </div>
        </section>

        <!-- TAB 6: HISTORY & AWARDS -->
        <section id="tab-history" class="tab-content">
            <h2>🏆 League History, Champions & Award Winners</h2>
            <div class="grid-2 mt-2">
                <div class="card">
                    <h3>World Series Champions</h3>
                    <div id="championsContainer" class="mt-2"></div>
                </div>
                <div class="card">
                    <h3>Most Valuable Player (MVP) Winners</h3>
                    <div id="mvpContainer" class="mt-2"></div>
                </div>
                <div class="card mt-4">
                    <h3>Cy Young Award Winners</h3>
                    <div id="cyYoungContainer" class="mt-2"></div>
                </div>
                <div class="card mt-4">
                    <h3>Rookie of the Year Winners</h3>
                    <div id="rotyContainer" class="mt-2"></div>
                </div>
            </div>
        </section>

        <!-- TAB 7: TOP PROSPECTS -->
        <section id="tab-prospects" class="tab-content">
            <h2>⭐ League Top Prospects</h2>
            <div id="prospectsContainer" class="mt-2"></div>
        </section>

        <!-- TAB 8: VISUALIZATIONS -->
        <section id="tab-visualizations" class="tab-content">
            <h2>📊 Interactive Player & Game Visualizations</h2>
            <div class="grid-2 mt-4">
                <div class="card">
                    <h3>📈 Player Season Trajectory</h3>
                    <div class="filter-group mb-2">
                        <select id="playerTrendSelect" onchange="updatePlayerTrendChart()">
                            <option value="">-- Select Player --</option>
                        </select>
                    </div>
                    <canvas id="trendChart"></canvas>
                </div>
                <div class="card">
                    <h3>🎯 Batted Ball Spray Chart</h3>
                    <canvas id="sprayChart"></canvas>
                </div>
            </div>
        </section>

        <!-- TAB 9: MATCHUPS -->
        <section id="tab-matchups" class="tab-content">
            <h2>⚔️ Pitcher vs. Hitter Head-to-Head Matchup</h2>
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

            <div class="modal-nav">
                <button class="modal-tab-btn active" onclick="switchModalTab('lineups')">📋 Lineups</button>
                <button class="modal-tab-btn" onclick="switchModalTab('pitching')">⚾ Pitching Staff</button>
                <button class="modal-tab-btn" onclick="switchModalTab('defense')">🛡️ 2D Diamond</button>
                <button class="modal-tab-btn" onclick="switchModalTab('schedule')">📅 Schedule</button>
                <button class="modal-tab-btn" onclick="switchModalTab('financials')">💰 Financials</button>
                <button class="modal-tab-btn" onclick="switchModalTab('prospects')">⭐ Prospects</button>
            </div>

            <!-- SUB-TAB 1: LINEUPS -->
            <div id="modal-sub-lineups" class="modal-sub-content active">
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Player</th>
                                <th>AB</th>
                                <th>H</th>
                                <th>HR</th>
                                <th>RBI</th>
                                <th>AVG</th>
                                <th>OBP</th>
                                <th>SLG</th>
                                <th>OPS</th>
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

            <!-- SUB-TAB 3: 2D DEFENSIVE DIAMOND -->
            <div id="modal-sub-defense" class="modal-sub-content">
                <h3>🛡️ 2D Interactive Field & Defensive Ratings</h3>
                <div class="diamond-field-wrapper mt-2">
                    <div class="baseball-field">
                        <div class="field-pos pos-c" id="field-pos-c"><span class="pos-label">C</span><span class="pos-player" id="def-c-name">Catcher</span></div>
                        <div class="field-pos pos-1b" id="field-pos-1b"><span class="pos-label">1B</span><span class="pos-player" id="def-1b-name">1st Base</span></div>
                        <div class="field-pos pos-2b" id="field-pos-2b"><span class="pos-label">2B</span><span class="pos-player" id="def-2b-name">2nd Base</span></div>
                        <div class="field-pos pos-3b" id="field-pos-3b"><span class="pos-label">3B</span><span class="pos-player" id="def-3b-name">3rd Base</span></div>
                        <div class="field-pos pos-ss" id="field-pos-ss"><span class="pos-label">SS</span><span class="pos-player" id="def-ss-name">Shortstop</span></div>
                        <div class="field-pos pos-lf" id="field-pos-lf"><span class="pos-label">LF</span><span class="pos-player" id="def-lf-name">Left Field</span></div>
                        <div class="field-pos pos-cf" id="field-pos-cf"><span class="pos-label">CF</span><span class="pos-player" id="def-cf-name">Center Field</span></div>
                        <div class="field-pos pos-rf" id="field-pos-rf"><span class="pos-label">RF</span><span class="pos-player" id="def-rf-name">Right Field</span></div>
                    </div>
                </div>
            </div>

            <!-- SUB-TAB 4: SCHEDULE -->
            <div id="modal-sub-schedule" class="modal-sub-content">
                <h3>Team Schedule & Game Results</h3>
                <div class="table-wrapper mt-2">
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Opponent</th>
                                <th>Result</th>
                                <th>Win Pitcher</th>
                                <th>Loss Pitcher</th>
                                <th>Save</th>
                                <th>Box Score</th>
                            </tr>
                        </thead>
                        <tbody id="scheduleTableBody"></tbody>
                    </table>
                </div>
            </div>

            <!-- SUB-TAB 5: FINANCIALS -->
            <div id="modal-sub-financials" class="modal-sub-content">
                <h3>Team Financial Overview</h3>
                <div id="financialSummaryCards" class="grid-4 mt-2"></div>
                <h4 class="mt-4">Active Contracts</h4>
                <div class="table-wrapper mt-2">
                    <table>
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>POS</th>
                                <th>Salary</th>
                                <th>Term</th>
                            </tr>
                        </thead>
                        <tbody id="financialContractsTableBody"></tbody>
                    </table>
                </div>
            </div>

            <!-- SUB-TAB 6: PROSPECTS -->
            <div id="modal-sub-prospects" class="modal-sub-content">
                <h3>Top Organizational Prospects</h3>
                <div class="table-wrapper mt-2">
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Prospect Name</th>
                                <th>POS</th>
                                <th>ETA</th>
                                <th>Potential Grade</th>
                            </tr>
                        </thead>
                        <tbody id="teamProspectsTableBody"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- PLAYER PROFILE CARD MODAL -->
    <div id="playerProfileModal" class="modal-overlay" style="display: none;">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title-group">
                    <img id="playerHeadshot" src="" class="player-headshot" style="width:50px;height:50px;" onerror="this.src='images/players/default.png';">
                    <div>
                        <h2 id="playerName">Player Name</h2>
                        <p id="playerTeamPos" style="color:#94a3b8;font-size:0.9rem;">Team • Position</p>
                    </div>
                </div>
                <button class="close-btn" onclick="closePlayerProfile()">✕</button>
            </div>

            <div id="playerCardHighlightGrid" class="grid-4 mt-4"></div>

            <div class="card mt-4">
                <h3>Full Season Statistics</h3>
                <div class="table-wrapper mt-2">
                    <table>
                        <thead id="playerStatsHeader"></thead>
                        <tbody id="playerStatsBody"></tbody>
                    </table>
                </div>
            </div>

            <div class="card mt-4" style="background:#0f172a;border-color:#334155;">
                <h4 style="color:#38bdf8;">📖 Standard Baseball Stat Legend</h4>
                <div class="grid-2 mt-2" style="font-size:0.85rem;color:#94a3b8;">
                    <div><b>AB:</b> At Bats | <b>H:</b> Hits | <b>HR:</b> Home Runs | <b>RBI:</b> Runs Batted In | <b>SB:</b> Stolen Bases</div>
                    <div><b>AVG:</b> Batting Average | <b>OBP:</b> On-Base % | <b>SLG:</b> Slugging % | <b>OPS:</b> On-Base + Slugging</div>
                    <div><b>ERA:</b> Earned Run Average | <b>IP:</b> Innings Pitched | <b>WHIP:</b> Walks+Hits/IP | <b>K/9:</b> Strikeouts/9</div>
                </div>
            </div>
        </div>
    </div>

    <!-- GAME BOX SCORE MODAL -->
    <div id="boxScoreModal" class="modal-overlay" style="display: none;">
        <div class="modal-card">
            <div class="modal-header">
                <h2 id="boxScoreTitle">Game Box Score</h2>
                <button class="close-btn" onclick="closeBoxScore()">✕</button>
            </div>
            <div id="boxScoreContent" class="mt-4"></div>
        </div>
    </div>

    <script src="app.js"></script>
</body>
</html>"""

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

.nav-links {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
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

select option {
    background-color: #1e293b;
    color: #f8fafc;
}

.container {
    max-width: 1350px;
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

.tab-content, .tx-sub-content {
    display: none;
}

.tab-content.active, .tx-sub-content.active {
    display: block;
}

.grid-1 { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(550px, 1fr)); gap: 1.5rem; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.2rem; }

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

.team-logo-small { width: 24px; height: 24px; object-fit: contain; }
.team-logo-medium { width: 36px; height: 36px; object-fit: contain; }

.player-headshot {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    object-fit: cover;
    background-color: #334155;
}

.team-link, .player-link {
    color: #38bdf8;
    cursor: pointer;
    text-decoration: underline;
    font-weight: 600;
}

.team-link:hover, .player-link:hover {
    color: #7dd3fc;
}

.btn-primary {
    background-color: #0284c7;
    color: white;
    padding: 6px 12px;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(15, 23, 42, 0.85);
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
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #334155;
    padding-bottom: 1rem;
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

.modal-nav {
    display: flex;
    gap: 8px;
    margin: 1rem 0;
    flex-wrap: wrap;
}

.modal-tab-btn {
    background-color: #0f172a;
    border: 1px solid #334155;
    color: #94a3b8;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.85rem;
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

/* 2D BASEBALL DIAMOND FIELD STYLES */
.diamond-field-wrapper {
    display: flex;
    justify-content: center;
    padding: 1rem 0;
}

.baseball-field {
    position: relative;
    width: 100%;
    max-width: 500px;
    height: 380px;
    background-color: #15803d;
    border: 3px solid #f8fafc;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
}

.field-pos {
    position: absolute;
    background-color: rgba(15, 23, 42, 0.9);
    border: 1px solid #38bdf8;
    border-radius: 6px;
    padding: 4px 8px;
    text-align: center;
    min-width: 90px;
}

.pos-label { display: block; font-size: 0.7rem; color: #38bdf8; font-weight: bold; }
.pos-player { display: block; font-size: 0.8rem; color: white; font-weight: 600; }

.pos-c { bottom: 15px; left: 50%; transform: translateX(-50%); }
.pos-1b { top: 200px; right: 40px; }
.pos-2b { top: 130px; right: 110px; }
.pos-3b { top: 200px; left: 40px; }
.pos-ss { top: 130px; left: 110px; }
.pos-lf { top: 40px; left: 40px; }
.pos-cf { top: 20px; left: 50%; transform: translateX(-50%); }
.pos-rf { top: 40px; right: 40px; }

.stat-box {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
}

.stat-box-title { font-size: 0.8rem; color: #94a3b8; }
.stat-box-val { font-size: 1.4rem; font-weight: bold; color: #38bdf8; }

.no-data { color: #94a3b8; font-style: italic; padding: 1rem 0; }
.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1.5rem; }
.mb-2 { margin-bottom: 0.75rem; }
"""

    app_js = """let leagueData = null;
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
                    <a class="team-link" onclick="openTeamSummary('${teamName.replace(/'/g, "\\\\'")}')">${teamName}</a>
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
                <a class="player-link" onclick="openPlayerProfile('${(p.Player || 'Player').replace(/'/g, "\\\\'")}')">${p.Player || "Player"}</a>
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
                <a class="player-link" onclick="openPlayerProfile('${(p.Player || 'Pitcher').replace(/'/g, "\\\\'")}')">${p.Player || "Pitcher"}</a>
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
                    <td><img src="${b.headshot_url}" class="player-headshot" onerror="this.src='images/players/default.png'"><a class="player-link" onclick="openPlayerProfile('${b.player.replace(/'/g, "\\\\'")}')">${b.player}</a></td>
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
                <a class="player-link" onclick="openPlayerProfile('${(fa.Player || fa.Name || 'Player').replace(/'/g, "\\\\'")}')">${fa.Player || fa.Name || "Player"}</a>
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
                <a class="player-link" onclick="openPlayerProfile('${(p.Player || 'Player').replace(/'/g, "\\\\'")}')">${p.Player || "Player"}</a>
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
                <a class="player-link" onclick="openPlayerProfile('${(p.Player || 'Pitcher').replace(/'/g, "\\\\'")}')">${p.Player || "Pitcher"}</a>
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
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(styles_css)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)

    print("Generated dashboard files v17 successfully.")

if __name__ == '__main__':
    generate_dashboard_files_v18()
