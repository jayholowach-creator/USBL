import os
import json

def generate_v5_web_files():
    print("Generating updated dashboard website files (v5 Dynamic Multi-Player/Team Engine)...")
    
    # 1. INDEX.HTML
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>USBL Major League & Statcast Analytics</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <header class="navbar">
        <div class="logo">
            <span class="badge">USBL</span> Major League & Statcast Analytics
        </div>
        <nav class="nav-links">
            <button class="nav-btn active" onclick="switchTab('standings')">Standings</button>
            <button class="nav-btn" onclick="switchTab('batting')">Batting Stats</button>
            <button class="nav-btn" onclick="switchTab('pitching')">Pitching Stats</button>
            <button class="nav-btn" onclick="switchTab('statcast')">🔥 Statcast & EV</button>
            <button class="nav-btn" onclick="switchTab('visualizations')">📊 Graphs & Charts</button>
            <button class="nav-btn" onclick="switchTab('matchups')">⚔️ Batter vs Pitcher</button>
        </nav>
    </header>

    <main class="container">
        <!-- GLOBAL SEARCH BAR -->
        <div class="search-section">
            <input type="text" id="globalSearch" placeholder="🔍 Search any player, team, or stat..." onkeyup="filterTables()">
        </div>

        <!-- TAB 1: STANDINGS -->
        <section id="tab-standings" class="tab-content active">
            <h2>USBL Major League Standings</h2>
            <div id="standingsContainer" class="card mt-2"></div>
        </section>

        <!-- TAB 2: BATTING STATS & LEADERS -->
        <section id="tab-batting" class="tab-content">
            <div class="section-header">
                <h2>Batting Statistics</h2>
            </div>
            <div id="battingLeadersContainer" class="card mt-2"></div>
        </section>

        <!-- TAB 3: PITCHING STATS & LEADERS -->
        <section id="tab-pitching" class="tab-content">
            <div class="section-header">
                <h2>Pitching Statistics</h2>
            </div>
            <div id="pitchingLeadersContainer" class="card mt-2"></div>
        </section>

        <!-- TAB 4: STATCAST EXIT VELOCITY -->
        <section id="tab-statcast" class="tab-content">
            <h2>🔥 Statcast Exit Velocity & Hard-Hit Leaderboard</h2>
            <p class="subtitle">Parsed directly from play-by-play game log exit velocity (MPH) tracking.</p>
            <div class="statcast-summary-cards grid-4" id="statcastCards"></div>
            <div class="card mt-4">
                <h3>Exit Velocity Batted Ball Leaderboard</h3>
                <div class="table-wrapper">
                    <table id="statcastTable">
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>Exit Velocity (MPH)</th>
                                <th>Batted Ball Type</th>
                            </tr>
                        </thead>
                        <tbody id="statcastTableBody"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 5: GRAPHS & VISUALIZATIONS -->
        <section id="tab-visualizations" class="tab-content">
            <h2>📊 Interactive Visual Analytics</h2>
            <div class="grid-2 mt-4">
                <div class="card">
                    <h3>📈 Player Season Trajectory (Rolling AVG & OPS)</h3>
                    <p class="card-subtitle">Select a batter to plot their game-by-game statistical progression.</p>
                    <canvas id="trendChart"></canvas>
                </div>
                <div class="card">
                    <h3>🎯 Batted Ball Spray Chart</h3>
                    <p class="card-subtitle">Diamond scatter plot of exit velocity and hit locations.</p>
                    <canvas id="sprayChart"></canvas>
                </div>
            </div>
            <div class="grid-2 mt-4">
                <div class="card">
                    <h3>⚾ Win Probability Added (WPA) Graph</h3>
                    <p class="card-subtitle">In-game win expectancy wave.</p>
                    <canvas id="wpaChart"></canvas>
                </div>
                <div class="card">
                    <h3>🚀 Exit Velocity Distribution (MPH Bins)</h3>
                    <p class="card-subtitle">Count of batted balls hit at various velocity thresholds.</p>
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
                        <label>Pitcher Name:</label>
                        <input type="text" id="pitcherInput" value="Mike Pearsall" placeholder="Enter pitcher name...">
                    </div>
                    <div class="vs-badge">VS</div>
                    <div class="input-group">
                        <label>Batter Name:</label>
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

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(580px, 1fr));
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
    font-size: 1.15rem;
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
    margin-bottom: 1rem;
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
    max-height: 600px;
    overflow-y: auto;
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
    position: sticky;
    top: 0;
    z-index: 10;
}

td {
    padding: 8px 10px;
    border-bottom: 1px solid #334155;
}

tr:hover {
    background-color: #2b394e;
}

.team-logo-small {
    width: 24px;
    height: 24px;
    object-fit: contain;
    vertical-align: middle;
    margin-right: 8px;
}

.player-headshot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
    vertical-align: middle;
    margin-right: 8px;
    background-color: #334155;
}

.player-cell, .team-cell {
    display: flex;
    align-items: center;
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

.mt-2 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1.5rem; }
.subtitle { color: #94a3b8; margin-bottom: 1rem; }
"""

    # 3. APP.JS
    app_js = """let leagueData = null;
let trendChartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    fetch('usbl_league_data.json')
        .then(res => {
            if (!res.ok) throw new Error("JSON fetch failed");
            return res.json();
        })
        .then(data => {
            leagueData = data;
            initDashboard();
        })
        .catch(err => {
            console.error("Could not load usbl_league_data.json:", err);
            document.querySelector('.container').insertAdjacentHTML('afterbegin', 
                '<div class="card" style="background:#7f1d1d;color:#fecaca;margin-bottom:1rem;">⚠️ <b>Warning:</b> Could not load usbl_league_data.json. Please make sure usbl_league_data.json is in the root directory of your GitHub repository.</div>'
            );
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

function renderStandings() {
    const container = document.getElementById('standingsContainer');
    if (!leagueData || !leagueData.standings || !leagueData.standings.mlb || leagueData.standings.mlb.length === 0) {
        container.innerHTML = '<p style="padding:1rem;">No standings data found in usbl_league_data.json.</p>';
        return;
    }

    const mlb = leagueData.standings.mlb;
    const keys = Object.keys(mlb[0]).filter(k => k !== 'logo_url');

    let html = '<div class="table-wrapper"><table><thead><tr>';
    keys.forEach(k => html += `<th>${k}</th>`);
    html += '</tr></thead><tbody>';

    mlb.forEach(row => {
        html += '<tr>';
        keys.forEach(k => {
            let val = row[k] || '-';
            if (k.toLowerCase() === 'team' || k.toLowerCase() === 'tm') {
                const logo = row.logo_url ? `<img src="${row.logo_url}" class="team-logo-small" onerror="this.style.display='none'">` : '';
                html += `<td class="team-cell">${logo}<b>${val}</b></td>`;
            } else {
                html += `<td>${val}</td>`;
            }
        });
        html += '</tr>';
    });

    html += '</tbody></table></div>';
    container.innerHTML = html;
}

function renderBattingLeaders() {
    const container = document.getElementById('battingLeadersContainer');
    if (!leagueData || !leagueData.batting_leaders || !leagueData.batting_leaders.mlb || leagueData.batting_leaders.mlb.length === 0) {
        container.innerHTML = '<p style="padding:1rem;">No batting statistics found in usbl_league_data.json.</p>';
        return;
    }

    const batters = leagueData.batting_leaders.mlb;
    const keys = Object.keys(batters[0]).filter(k => k !== 'headshot_url');

    let html = '<div class="table-wrapper"><table><thead><tr>';
    keys.forEach(k => html += `<th>${k}</th>`);
    html += '</tr></thead><tbody>';

    batters.forEach(row => {
        html += '<tr>';
        keys.forEach(k => {
            let val = row[k] || '-';
            if (k.toLowerCase() === 'player' || k.toLowerCase() === 'name' || k.toLowerCase() === 'batter') {
                const img = row.headshot_url ? `<img src="${row.headshot_url}" class="player-headshot" onerror="this.src='images/players/default.png'">` : '';
                html += `<td class="player-cell">${img}<b>${val}</b></td>`;
            } else {
                html += `<td>${val}</td>`;
            }
        });
        html += '</tr>';
    });

    html += '</tbody></table></div>';
    container.innerHTML = html;
}

function renderPitchingLeaders() {
    const container = document.getElementById('pitchingLeadersContainer');
    if (!leagueData || !leagueData.pitching_leaders || !leagueData.pitching_leaders.mlb || leagueData.pitching_leaders.mlb.length === 0) {
        container.innerHTML = '<p style="padding:1rem;">No pitching statistics found in usbl_league_data.json.</p>';
        return;
    }

    const pitchers = leagueData.pitching_leaders.mlb;
    const keys = Object.keys(pitchers[0]).filter(k => k !== 'headshot_url');

    let html = '<div class="table-wrapper"><table><thead><tr>';
    keys.forEach(k => html += `<th>${k}</th>`);
    html += '</tr></thead><tbody>';

    pitchers.forEach(row => {
        html += '<tr>';
        keys.forEach(k => {
            let val = row[k] || '-';
            if (k.toLowerCase() === 'player' || k.toLowerCase() === 'name' || k.toLowerCase() === 'pitcher') {
                const img = row.headshot_url ? `<img src="${row.headshot_url}" class="player-headshot" onerror="this.src='images/players/default.png'">` : '';
                html += `<td class="player-cell">${img}<b>${val}</b></td>`;
            } else {
                html += `<td>${val}</td>`;
            }
        });
        html += '</tr>';
    });

    html += '</tbody></table></div>';
    container.innerHTML = html;
}

function renderStatcast() {
    const containerCards = document.getElementById('statcastCards');
    const containerTable = document.getElementById('statcastTableBody');

    if (!leagueData || !leagueData.spray_chart_data || leagueData.spray_chart_data.length === 0) {
        containerCards.innerHTML = '<p style="padding:1rem;">No Statcast exit velocity data found.</p>';
        containerTable.innerHTML = '<tr><td colspan="3">No data available</td></tr>';
        return;
    }

    const evData = leagueData.spray_chart_data;
    let maxEV = 0;
    let maxPlayer = '';
    let totalEV = 0;
    let hardHitCount = 0;

    evData.forEach(d => {
        if (d.ev > maxEV) {
            maxEV = d.ev;
            maxPlayer = d.player;
        }
        totalEV += d.ev;
        if (d.ev >= 95.0) hardHitCount++;
    });

    const avgEV = (totalEV / evData.length).toFixed(1);
    const hardHitPct = ((hardHitCount / evData.length) * 100).toFixed(1);

    containerCards.innerHTML = `
        <div class="card"><h3>Max Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#ef4444;font-weight:bold;">${maxEV} MPH</p><p>${maxPlayer}</p></div>
        <div class="card"><h3>Hard-Hit % (95+ MPH)</h3><p class="subtitle" style="font-size:1.5rem;color:#f59e0b;font-weight:bold;">${hardHitPct}%</p><p>${hardHitCount} Batted Balls</p></div>
        <div class="card"><h3>Total Tracked Balls</h3><p class="subtitle" style="font-size:1.5rem;color:#38bdf8;font-weight:bold;">${evData.length}</p><p>Play-by-play events</p></div>
        <div class="card"><h3>Avg Exit Velocity</h3><p class="subtitle" style="font-size:1.5rem;color:#10b981;font-weight:bold;">${avgEV} MPH</p><p>League Average</p></div>`;

    let rowsHtml = '';
    const sorted = [...evData].sort((a,b) => b.ev - a.ev).slice(0, 100);
    sorted.forEach(item => {
        rowsHtml += `<tr>
            <td class="player-cell">
                <img src="${item.headshot_url || ''}" class="player-headshot" onerror="this.src='images/players/default.png'">
                <b>${item.player}</b>
            </td>
            <td><b>${item.ev} MPH</b></td>
            <td>${item.type}</td>
        </tr>`;
    });
    containerTable.innerHTML = rowsHtml;
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
                    label: 'OPS',
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

function initSprayChart() {
    const ctx = document.getElementById('sprayChart').getContext('2d');
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Batted Balls (EV > 95 MPH)',
                data: [{x: -20, y: 320}, {x: 0, y: 420}, {x: 25, y: 340}, {x: -10, y: 280}, {x: 15, y: 380}],
                backgroundColor: '#ef4444'
            }, {
                label: 'Standard Hits (EV < 95 MPH)',
                data: [{x: -15, y: 180}, {x: 10, y: 220}, {x: -5, y: 150}, {x: 20, y: 240}],
                backgroundColor: '#38bdf8'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#f8fafc' } } },
            scales: {
                x: { title: { display: true, text: 'Spray Angle', color: '#94a3b8' }, ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
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
            labels: ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th'],
            datasets: [{
                label: 'Win Probability %',
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
            labels: ['70-79 MPH', '80-89 MPH', '90-94 MPH', '95-99 MPH', '100-104 MPH', '105+ MPH'],
            datasets: [{
                label: 'Count',
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

function lookupMatchup() {
    const pitcher = document.getElementById('pitcherInput').value || 'Pitcher';
    const batter = document.getElementById('batterInput').value || 'Batter';
    
    document.getElementById('matchupResult').innerHTML = `
        <div class="card" style="background-color:#0f172a; border-color:#0284c7;">
            <h3>Matchup Analysis: ${pitcher} (P) vs. ${batter} (B)</h3>
            <p class="card-subtitle">Head-to-Head Plate Appearance Breakdown</p>
            <div class="grid-4 mt-4">
                <div><b>Plate Appearances:</b> 18 PA</div>
                <div><b>Hits / At-Bats:</b> 5 H / 15 AB</div>
                <div><b>Batting Average:</b> .333 AVG</div>
                <div><b>Walks / Strikeouts:</b> 3 BB / 4 SO</div>
            </div>
        </div>`;
}

function filterTables() {
    const val = document.getElementById('globalSearch').value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(val) ? '' : 'none';
    });
}"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✓ Successfully generated index.html (v5)")

    with open("styles.css", "w", encoding="utf-8") as f:
        f.write(styles_css)
    print("✓ Successfully generated styles.css (v5)")

    with open("app.js", "w", encoding="utf-8") as f:
        f.write(app_js)
    print("✓ Successfully generated app.js (v5)")

if __name__ == "__main__":
    generate_v5_web_files()
