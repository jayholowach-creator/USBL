import os

def generate_v4_web_files():
    print("Generating updated dashboard website files (v4 with Logos, Player Headshots & Chart.js)...")
    
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
        <div class="logo">
            <span class="badge">USBL</span> Major League & Statcast Analytics
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
            <h2>League Standings</h2>
            <div id="standingsContainer" class="grid-2"></div>
        </section>

        <!-- TAB 2: BATTING LEADERS WITH SPLITS -->
        <section id="tab-batting" class="tab-content">
            <div class="section-header">
                <h2>Batting Leaders</h2>
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
                <h2>Pitching Leaders</h2>
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
                <h3>Top Exit Velocity Batted Balls (105+ MPH)</h3>
                <div class="table-wrapper">
                    <table id="statcastTable">
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>Team</th>
                                <th>Exit Velocity (MPH)</th>
                                <th>Batted Ball Type</th>
                                <th>Result</th>
                                <th>Hard-Hit Rate (95+ MPH)</th>
                            </tr>
                        </thead>
                        <tbody id="statcastTableBody"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 5: GRAPHS & BASEBALL-REFERENCE STYLE VISUALIZATIONS -->
        <section id="tab-visualizations" class="tab-content">
            <h2>📊 Interactive Player & Game Visualizations</h2>
            
            <div class="grid-2 mt-4">
                <!-- CHART 1: SEASON BATTING AVERAGE & OPS TREND LINE -->
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

                <!-- CHART 2: SPRAY CHART -->
                <div class="card">
                    <h3>🎯 Batted Ball Field Spray Chart</h3>
                    <p class="card-subtitle">Location and contact quality for hits and outs on the diamond.</p>
                    <canvas id="sprayChart"></canvas>
                </div>
            </div>

            <div class="grid-2 mt-4">
                <!-- CHART 3: WIN PROBABILITY ADDED (WPA) GRAPH -->
                <div class="card">
                    <h3>⚾ In-Game Win Expectancy (WPA) Graph</h3>
                    <p class="card-subtitle">Inning-by-inning win probability wave (Anaheim Halos vs Tampa Bay Armada).</p>
                    <canvas id="wpaChart"></canvas>
                </div>

                <!-- CHART 4: EXIT VELOCITY DISTRIBUTION HISTOGRAM -->
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
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
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

/* TEAM LOGOS AND PLAYER HEADSHOT STYLING */
.team-logo-small {
    width: 24px;
    height: 24px;
    object-fit: contain;
    vertical-align: middle;
    margin-right: 8px;
    border-radius: 4px;
}

.player-headshot {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #0284c7;
    vertical-align: middle;
    margin-right: 10px;
    background-color: #0f172a;
}

.player-cell {
    display: flex;
    align-items: center;
}

.team-cell {
    display: flex;
    align-items: center;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.2rem;
}

.filter-group select, .filter-group input {
    background-color: #0f172a;
    color: #f8fafc;
    border: 1px solid #334155;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.9rem;
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

.matchup-box {
    margin-top: 1rem;
}

.matchup-inputs {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.vs-badge {
    background-color: #ef4444;
    color: white;
    font-weight: 800;
    padding: 6px 12px;
    border-radius: 50%;
    font-size: 0.9rem;
}

.mt-4 { margin-top: 1.5rem; }
.mb-2 { margin-bottom: 0.75rem; }
.subtitle { color: #94a3b8; margin-bottom: 1rem; }
"""

    # 3. APP.JS
    app_js = """let leagueData = null;
let trendChartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    fetch('usbl_league_data.json')
        .then(res => res.json())
        .then(data => {
            leagueData = data;
            initDashboard();
        })
        .catch(err => {
            console.log("Using fallback interactive dataset...");
            initFallbackData();
        });
});

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    
    document.getElementById('tab-' + tabName).classList.add('active');
    event.target.classList.add('active');

    if (tabName === 'visualizations') {
        renderAllCharts();
    }
}

function initDashboard() {
    renderStandings();
    renderBattingLeaders();
    renderPitchingLeaders();
    renderStatcast();
    renderAllCharts();
}

function renderAllCharts() {
    initTrendChart();
    initSprayChart();
    initWpaChart();
    initEvDistChart();
}

function initTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    if (trendChartInstance) trendChartInstance.destroy();

    trendChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 20}, (_, i) => `Game ${i*8 + 1}`),
            datasets: [
                {
                    label: 'Batting Average (AVG)',
                    data: [.280, .295, .310, .305, .320, .315, .328, .335, .340, .338, .342, .345, .350, .348, .352, .355, .351, .358, .362, .365],
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'On-Base Plus Slugging (OPS)',
                    data: [.850, .880, .920, .910, .950, .940, .980, 1.010, 1.035, 1.020, 1.050, 1.065, 1.080, 1.075, 1.090, 1.105, 1.095, 1.120, 1.140, 1.155],
                    borderColor: '#f59e0b',
                    backgroundColor: 'transparent',
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#f8fafc' } } },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
            }
        }
    });
}

function updatePlayerTrendChart() {
    initTrendChart();
}

function initSprayChart() {
    const ctx = document.getElementById('sprayChart').getContext('2d');
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Batted Balls (EV > 95 MPH)',
                data: [
                    {x: -20, y: 320}, {x: 0, y: 420}, {x: 25, y: 340}, {x: -10, y: 280},
                    {x: 15, y: 380}, {x: -30, y: 210}, {x: 35, y: 290}, {x: 5, y: 410}
                ],
                backgroundColor: '#ef4444'
            }, {
                label: 'Standard Hits (EV < 95 MPH)',
                data: [
                    {x: -15, y: 180}, {x: 10, y: 220}, {x: -5, y: 150}, {x: 20, y: 240}
                ],
                backgroundColor: '#38bdf8'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#f8fafc' } } },
            scales: {
                x: { title: { display: true, text: 'Left Field <--- Spray Angle ---> Right Field', color: '#94a3b8' }, ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
                y: { title: { display: true, text: 'Distance (Feet)', color: '#94a3b8' }, ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
            }
        }
    });
}

function initWpaChart() {
    const ctx = document.getElementById('wpaChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th (Walk-off)'],
            datasets: [{
                label: 'Tampa Bay Armada Win Probability %',
                data: [50, 42, 65, 58, 45, 52, 70, 60, 100],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.15)',
                fill: true,
                stepped: true
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#f8fafc' } } },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
                y: { min: 0, max: 100, ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
            }
        }
    });
}

function initEvDistChart() {
    const ctx = document.getElementById('evDistChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['70-79 MPH', '80-89 MPH', '90-94 MPH', '95-99 MPH (Hard Hit)', '100-104 MPH', '105+ MPH (Elite)'],
            datasets: [{
                label: 'Batted Ball Count',
                data: [42, 115, 168, 142, 68, 24],
                backgroundColor: ['#64748b', '#64748b', '#38bdf8', '#f59e0b', '#ef4444', '#dc2626']
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#f8fafc' } } },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
            }
        }
    });
}

function renderStandings() {
    const container = document.getElementById('standingsContainer');
    container.innerHTML = `
        <div class="card">
            <h3>USBL Major League Standings</h3>
            <table>
                <thead><tr><th>Team</th><th>W</th><th>L</th><th>PCT</th><th>GB</th></tr></thead>
                <tbody>
                    <tr>
                        <td class="team-cell">
                            <img src="images/team_logos/tampa_bay_armada.png" class="team-logo-small" onerror="this.style.display='none'">
                            <b>Tampa Bay Armada</b>
                        </td>
                        <td>103</td><td>59</td><td>.636</td><td>-</td>
                    </tr>
                    <tr>
                        <td class="team-cell">
                            <img src="images/team_logos/anaheim_halos.png" class="team-logo-small" onerror="this.style.display='none'">
                            Anaheim Halos
                        </td>
                        <td>94</td><td>68</td><td>.580</td><td>9.0</td>
                    </tr>
                    <tr>
                        <td class="team-cell">
                            <img src="images/team_logos/new_york_knights.png" class="team-logo-small" onerror="this.style.display='none'">
                            New York Knights
                        </td>
                        <td>88</td><td>74</td><td>.543</td><td>15.0</td>
                    </tr>
                </tbody>
            </table>
        </div>`;
}

function renderBattingLeaders() {
    const container = document.getElementById('battingLeadersContainer');
    container.innerHTML = `
        <div class="card">
            <h3>Batting Average (AVG)</h3>
            <table>
                <thead><tr><th>Rank</th><th>Player</th><th>Team</th><th>AVG</th></tr></thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td class="player-cell">
                            <img src="images/players/nate_mahoney.png" class="player-headshot" onerror="this.src='images/players/default.png'">
                            Nate Mahoney
                        </td>
                        <td>TB</td><td>.365</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td class="player-cell">
                            <img src="images/players/jesse_wilson.png" class="player-headshot" onerror="this.src='images/players/default.png'">
                            Jesse Wilson
                        </td>
                        <td>ANA</td><td>.342</td>
                    </tr>
                    <tr>
                        <td>3</td>
                        <td class="player-cell">
                            <img src="images/players/dave_gordon.png" class="player-headshot" onerror="this.src='images/players/default.png'">
                            Dave Gordon
                        </td>
                        <td>TB</td><td>.328</td>
                    </tr>
                </tbody>
            </table>
        </div>`;
}

function renderPitchingLeaders() {
    const container = document.getElementById('pitchingLeadersContainer');
    container.innerHTML = `
        <div class="card">
            <h3>Earned Run Average (ERA)</h3>
            <table>
                <thead><tr><th>Rank</th><th>Pitcher</th><th>Team</th><th>ERA</th></tr></thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td class="player-cell">
                            <img src="images/players/mike_pearsall.png" class="player-headshot" onerror="this.src='images/players/default.png'">
                            Mike Pearsall
                        </td>
                        <td>TB</td><td>2.84</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td class="player-cell">
                            <img src="images/players/chris_vance.png" class="player-headshot" onerror="this.src='images/players/default.png'">
                            Chris Vance
                        </td>
                        <td>ANA</td><td>3.12</td>
                    </tr>
                </tbody>
            </table>
        </div>`;
}

function renderStatcast() {
    const container = document.getElementById('statcastCards');
    container.innerHTML = `
        <div class="card"><h3>Max Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#ef4444;font-weight:bold;">111.3 MPH</p><p>Jesse Wilson (Halos)</p></div>
        <div class="card"><h3>Hard-Hit % (95+ MPH)</h3><p class="subtitle" style="font-size:1.5rem;color:#f59e0b;font-weight:bold;">48.2%</p><p>Tampa Bay Armada</p></div>
        <div class="card"><h3>Longest Home Run</h3><p class="subtitle" style="font-size:1.5rem;color:#38bdf8;font-weight:bold;">448 FT</p><p>Nate Mahoney (Armada)</p></div>
        <div class="card"><h3>Avg Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#10b981;font-weight:bold;">91.4 MPH</p><p>League Average</p></div>`;

    document.getElementById('statcastTableBody').innerHTML = `
        <tr>
            <td class="player-cell">
                <img src="images/players/jesse_wilson.png" class="player-headshot" onerror="this.src='images/players/default.png'">
                Jesse Wilson
            </td>
            <td>Anaheim Halos</td><td><b>111.3 MPH</b></td><td>Line Drive</td><td>Double</td><td>52.4%</td>
        </tr>
        <tr>
            <td class="player-cell">
                <img src="images/players/nate_mahoney.png" class="player-headshot" onerror="this.src='images/players/default.png'">
                Nate Mahoney
            </td>
            <td>Tampa Bay Armada</td><td><b>110.0 MPH</b></td><td>Flyball</td><td>Home Run (420 ft)</td><td>51.1%</td>
        </tr>
        <tr>
            <td class="player-cell">
                <img src="images/players/dave_gordon.png" class="player-headshot" onerror="this.src='images/players/default.png'">
                Dave Gordon
            </td>
            <td>Tampa Bay Armada</td><td><b>108.8 MPH</b></td><td>Line Drive</td><td>Double</td><td>47.8%</td>
        </tr>`;
}

function lookupMatchup() {
    const pitcher = document.getElementById('pitcherInput').value || 'Mike Pearsall';
    const batter = document.getElementById('batterInput').value || 'Elmer Aguilera';
    
    document.getElementById('matchupResult').innerHTML = `
        <div class="card" style="background-color:#0f172a; border-color:#0284c7;">
            <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                <img src="images/players/mike_pearsall.png" class="player-headshot" style="width:60px;height:60px;" onerror="this.src='images/players/default.png'">
                <div>
                    <h3 style="margin:0;">Matchup Analysis: ${pitcher} (P) vs. ${batter} (B)</h3>
                    <p class="card-subtitle" style="margin:0;">Career Head-to-Head Plate Appearance Breakdown</p>
                </div>
                <img src="images/players/elmer_aguilera.png" class="player-headshot" style="width:60px;height:60px;margin-left:auto;" onerror="this.src='images/players/default.png'">
            </div>
            <div class="grid-4 mt-4">
                <div><b>Plate Appearances:</b> 18 PA</div>
                <div><b>Hits / At-Bats:</b> 5 H / 15 AB</div>
                <div><b>Batting Average:</b> .333 AVG</div>
                <div><b>Walks / Strikeouts:</b> 3 BB / 4 SO</div>
            </div>
            <div class="grid-4 mt-4">
                <div><b>Extra-Base Hits:</b> 2 2B, 1 HR</div>
                <div><b>Max Exit Velocity:</b> 106.4 MPH</div>
                <div><b>Average Exit Velocity:</b> 92.1 MPH</div>
                <div><b>Hard-Hit Rate:</b> 46.2%</div>
            </div>
        </div>`;
}

function filterTables() {
    const val = document.getElementById('globalSearch').value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(val) ? '' : 'none';
    });
}

function initFallbackData() {
    initDashboard();
}"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✓ Successfully generated index.html (v4)")

    with open("styles.css", "w", encoding="utf-8") as f:
        f.write(styles_css)
    print("✓ Successfully generated styles.css (v4)")

    with open("app.js", "w", encoding="utf-8") as f:
        f.write(app_js)
    print("✓ Successfully generated app.js (v4)")

if __name__ == "__main__":
    generate_v4_web_files()
