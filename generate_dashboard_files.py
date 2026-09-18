import os

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>USBL League Stats & Reports</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <header class="navbar">
        <div class="nav-container">
            <div class="brand">
                <span class="logo-icon">⚾</span>
                <span class="brand-name">USBL League Dashboard</span>
                <span class="season-badge">2017 Season</span>
            </div>
            <nav class="nav-tabs">
                <button class="tab-btn active" data-tab="standings">Standings</button>
                <button class="tab-btn" data-tab="batting">Batting Leaders</button>
                <button class="tab-btn" data-tab="pitching">Pitching Leaders</button>
                <button class="tab-btn" data-tab="team-stats">Team Stats</button>
            </nav>
        </div>
    </header>

    <main class="main-content">
        <div class="search-bar-container">
            <input type="text" id="playerSearch" placeholder="🔍 Search players, teams, or stats...">
        </div>

        <!-- Standings Section -->
        <section id="standings" class="tab-content active">
            <div class="section-header">
                <h2>League Standings</h2>
                <p>USBL Major League Standings & Divisional Rankings</p>
            </div>
            <div id="standingsContainer" class="table-card">
                <div class="loading">Loading standings data...</div>
            </div>
        </section>

        <!-- Batting Leaders Section -->
        <section id="batting" class="tab-content">
            <div class="section-header">
                <h2>Batting Leaders</h2>
                <p>Top Hitters by AVG, HR, RBI, OPS, and WAR</p>
            </div>
            <div id="battingContainer" class="table-card">
                <div class="loading">Loading batting data...</div>
            </div>
        </section>

        <!-- Pitching Leaders Section -->
        <section id="pitching" class="tab-content">
            <div class="section-header">
                <h2>Pitching Leaders</h2>
                <p>Top Pitchers by ERA, Wins, Strikeouts, Saves, and WHIP</p>
            </div>
            <div id="pitchingContainer" class="table-card">
                <div class="loading">Loading pitching data...</div>
            </div>
        </section>

        <!-- Team Stats Section -->
        <section id="team-stats" class="tab-content">
            <div class="section-header">
                <h2>Team Overview & Statistics</h2>
                <p>Comprehensive Team Performance Breakdown</p>
            </div>
            <div id="teamStatsContainer" class="table-card">
                <div class="loading">Loading team stats...</div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <p>USBL Baseball Simulation Dashboard &bull; Generated from OOTP 27 Almanac</p>
    </footer>

    <script src="app.js"></script>
</body>
</html>
"""

STYLES_CSS = """:root {
    --bg-main: #0f172a;
    --bg-card: #1e293b;
    --bg-card-hover: #334155;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --accent-teal: #14b8a6;
    --accent-blue: #3b82f6;
    --border-color: #334155;
    --radius: 12px;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-main);
    color: var(--text-main);
    line-height: 1.5;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.navbar {
    background-color: rgba(30, 41, 59, 0.8);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border-color);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.logo-icon {
    font-size: 1.5rem;
}

.brand-name {
    font-weight: 800;
    font-size: 1.25rem;
    background: linear-gradient(135deg, #2dd4bf, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.season-badge {
    background-color: #0284c7;
    color: #fff;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
}

.nav-tabs {
    display: flex;
    gap: 0.5rem;
}

.tab-btn {
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.2s ease;
}

.tab-btn:hover {
    color: var(--text-main);
    background-color: rgba(255, 255, 255, 0.05);
}

.tab-btn.active {
    color: #fff;
    background-color: var(--accent-teal);
}

.main-content {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1.5rem;
    flex: 1;
    width: 100%;
}

.search-bar-container {
    margin-bottom: 2rem;
}

#playerSearch {
    width: 100%;
    padding: 0.85rem 1.25rem;
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    color: var(--text-main);
    font-size: 1rem;
    outline: none;
    transition: border-color 0.2s;
}

#playerSearch:focus {
    border-color: var(--accent-teal);
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

.section-header {
    margin-bottom: 1.5rem;
}

.section-header h2 {
    font-size: 1.75rem;
    font-weight: 700;
}

.section-header p {
    color: var(--text-muted);
    font-size: 0.95rem;
}

.table-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 1.5rem;
    overflow-x: auto;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}

table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

th, td {
    padding: 0.85rem 1rem;
    border-bottom: 1px solid var(--border-color);
}

th {
    background-color: rgba(15, 23, 42, 0.5);
    color: var(--accent-teal);
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

tr:hover {
    background-color: var(--bg-card-hover);
}

.loading {
    color: var(--text-muted);
    text-align: center;
    padding: 3rem;
    font-style: italic;
}

.footer {
    text-align: center;
    padding: 2rem;
    border-top: 1px solid var(--border-color);
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-top: 3rem;
}
"""

APP_JS = """document.addEventListener('DOMContentLoaded', () => {
    // Tab switching logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Fetch and render data from usbl_league_data.json
    fetch('usbl_league_data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            renderStandings(data);
            renderBatting(data);
            renderPitching(data);
            renderTeamStats(data);
            setupSearch(data);
        })
        .catch(err => {
            console.error('Error loading league data:', err);
            const errorMsg = `<div class="loading">Data file <code>usbl_league_data.json</code> not found. Make sure you ran <code>export_league_data_v2.py</code> in this folder!</div>`;
            document.getElementById('standingsContainer').innerHTML = errorMsg;
            document.getElementById('battingContainer').innerHTML = errorMsg;
            document.getElementById('pitchingContainer').innerHTML = errorMsg;
            document.getElementById('teamStatsContainer').innerHTML = errorMsg;
        });
});

function renderStandings(data) {
    const container = document.getElementById('standingsContainer');
    if (!data.standings || data.standings.length === 0) {
        container.innerHTML = '<div class="loading">No standings data found.</div>';
        return;
    }

    let html = `<table><thead><tr><th>Team</th><th>W</th><th>L</th><th>PCT</th><th>GB</th><th>HOME</th><th>ROAD</th><th>STRK</th></tr></thead><tbody>`;
    data.standings.forEach(row => {
        html += `<tr>
            <td><strong>${row.team || row.Team || ''}</strong></td>
            <td>${row.w || row.W || 0}</td>
            <td>${row.l || row.L || 0}</td>
            <td>${row.pct || row.PCT || '.000'}</td>
            <td>${row.gb || row.GB || '-'}</td>
            <td>${row.home || row.Home || '-'}</td>
            <td>${row.road || row.Road || '-'}</td>
            <td>${row.streak || row.Streak || '-'}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderBatting(data) {
    const container = document.getElementById('battingContainer');
    const batting = data.batting_leaders || data.batting || [];
    if (batting.length === 0) {
        container.innerHTML = '<div class="loading">No batting leader data found.</div>';
        return;
    }

    let html = `<table><thead><tr><th>Player</th><th>Team</th><th>AVG</th><th>HR</th><th>RBI</th><th>OPS</th><th>WAR</th></tr></thead><tbody>`;
    batting.forEach(p => {
        html += `<tr>
            <td><strong>${p.name || p.Player || ''}</strong></td>
            <td>${p.team || p.Team || ''}</td>
            <td>${p.avg || p.AVG || '.000'}</td>
            <td>${p.hr || p.HR || 0}</td>
            <td>${p.rbi || p.RBI || 0}</td>
            <td>${p.ops || p.OPS || '.000'}</td>
            <td>${p.war || p.WAR || '0.0'}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderPitching(data) {
    const container = document.getElementById('pitchingContainer');
    const pitching = data.pitching_leaders || data.pitching || [];
    if (pitching.length === 0) {
        container.innerHTML = '<div class="loading">No pitching leader data found.</div>';
        return;
    }

    let html = `<table><thead><tr><th>Player</th><th>Team</th><th>W-L</th><th>ERA</th><th>SO</th><th>SV</th><th>WHIP</th></tr></thead><tbody>`;
    pitching.forEach(p => {
        html += `<tr>
            <td><strong>${p.name || p.Player || ''}</strong></td>
            <td>${p.team || p.Team || ''}</td>
            <td>${p.wl || p.WL || '0-0'}</td>
            <td>${p.era || p.ERA || '0.00'}</td>
            <td>${p.so || p.SO || 0}</td>
            <td>${p.sv || p.SV || 0}</td>
            <td>${p.whip || p.WHIP || '0.00'}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderTeamStats(data) {
    const container = document.getElementById('teamStatsContainer');
    const teams = data.teams || [];
    if (teams.length === 0) {
        container.innerHTML = '<div class="loading">No team statistics found.</div>';
        return;
    }

    let html = `<table><thead><tr><th>Team</th><th>Runs Scored</th><th>Runs Allowed</th><th>Differential</th><th>Team AVG</th><th>Team ERA</th></tr></thead><tbody>`;
    teams.forEach(t => {
        html += `<tr>
            <td><strong>${t.name || t.Team || ''}</strong></td>
            <td>${t.rs || t.RS || 0}</td>
            <td>${t.ra || t.RA || 0}</td>
            <td>${t.diff || t.Diff || 0}</td>
            <td>${t.avg || t.AVG || '.000'}</td>
            <td>${t.era || t.ERA || '0.00'}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function setupSearch(data) {
    const searchInput = document.getElementById('playerSearch');
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(query) ? '' : 'none';
        });
    });
}
"""

def generate_website_files(output_dir="."):
    print(f"Generating website files in '{os.path.abspath(output_dir)}'...")
    
    files = {
        "index.html": INDEX_HTML,
        "styles.css": STYLES_CSS,
        "app.js": APP_JS
    }
    
    for filename, content in files.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ Created {filename}")
        
    print("\nSuccess! All dashboard website files have been created.")
    print("Files created: index.html, styles.css, app.js")

if __name__ == "__main__":
    generate_website_files(".")
