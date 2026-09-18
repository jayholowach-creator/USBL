import os

def generate_dashboard_files_v18():
    print("Generating updated dashboard website files (v18 - Sprint 2 Complete & Free Agents)...")
    
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>USBL Major League Dashboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <div class="header-container">
            <div class="logo-title">
                <img src="images/usbl_logo.png" alt="USBL Logo" class="main-logo" onerror="this.style.display='none'">
                <h1>USBL Major League Dashboard</h1>
            </div>
            <div class="search-box">
                <input type="text" id="globalSearch" placeholder="Search player or team..." onkeyup="filterTables()">
            </div>
        </div>
        <nav>
            <button class="nav-btn active" onclick="switchTab('standingsTab')">🏆 Standings</button>
            <button class="nav-btn" onclick="switchTab('battingTab')">⚾ Batting Leaders</button>
            <button class="nav-btn" onclick="switchTab('pitchingTab')">🔥 Pitching Leaders</button>
            <button class="nav-btn" onclick="switchTab('statcastTab')">🚀 Statcast Leaderboard</button>
            <button class="nav-btn" onclick="switchTab('prospectsTab')">⭐ Top Prospects</button>
            <button class="nav-btn" onclick="switchTab('transactionsTab')">📰 Transactions & Free Agents</button>
            <button class="nav-btn" onclick="switchTab('historyTab')">🏆 History & Awards</button>
        </nav>
    </header>

    <main>
        <!-- Standings Tab -->
        <section id="standingsTab" class="tab-content active">
            <div class="sub-nav">
                <button class="sub-btn active" onclick="toggleStandings('division')">Division Standings</button>
                <button class="sub-btn" onclick="toggleStandings('wildcard')">Wild Card Race</button>
            </div>
            <div id="divisionStandingsView">
                <h2>League Standings</h2>
                <table id="standingsTable">
                    <thead>
                        <tr>
                            <th>Team</th>
                            <th>W</th>
                            <th>L</th>
                            <th>PCT</th>
                            <th>GB</th>
                            <th>WCGB</th>
                            <th>HOME</th>
                            <th>AWAY</th>
                            <th>L10</th>
                            <th>STREAK</th>
                        </tr>
                    </thead>
                    <tbody id="standingsBody"></tbody>
                </table>
            </div>
            <div id="wildcardStandingsView" style="display:none;">
                <h2>Wild Card Standings</h2>
                <table id="wildcardTable">
                    <thead>
                        <tr>
                            <th>Team</th>
                            <th>W</th>
                            <th>L</th>
                            <th>PCT</th>
                            <th>WCGB</th>
                            <th>L10</th>
                            <th>STREAK</th>
                        </tr>
                    </thead>
                    <tbody id="wildcardBody"></tbody>
                </table>
            </div>
        </section>

        <!-- Batting Leaders Tab -->
        <section id="battingTab" class="tab-content">
            <h2>Batting Leaders</h2>
            <table id="battingTable">
                <thead>
                    <tr>
                        <th>Player</th>
                        <th>Team</th>
                        <th>G</th>
                        <th>AB</th>
                        <th>R</th>
                        <th>H</th>
                        <th>2B</th>
                        <th>3B</th>
                        <th>HR</th>
                        <th>RBI</th>
                        <th>BB</th>
                        <th>SO</th>
                        <th>SB</th>
                        <th>AVG</th>
                        <th>OBP</th>
                        <th>SLG</th>
                        <th>OPS</th>
                    </tr>
                </thead>
                <tbody id="battingBody"></tbody>
            </table>
        </section>

        <!-- Pitching Leaders Tab -->
        <section id="pitchingTab" class="tab-content">
            <h2>Pitching Leaders</h2>
            <table id="pitchingTable">
                <thead>
                    <tr>
                        <th>Player</th>
                        <th>Team</th>
                        <th>W</th>
                        <th>L</th>
                        <th>ERA</th>
                        <th>G</th>
                        <th>GS</th>
                        <th>SV</th>
                        <th>IP</th>
                        <th>H</th>
                        <th>R</th>
                        <th>ER</th>
                        <th>HR</th>
                        <th>BB</th>
                        <th>SO</th>
                        <th>WHIP</th>
                    </tr>
                </thead>
                <tbody id="pitchingBody"></tbody>
            </table>
        </section>

        <!-- Statcast Tab -->
        <section id="statcastTab" class="tab-content">
            <h2>Statcast Leaderboard (Exit Velocity)</h2>
            <div class="statcast-summary-cards" id="statcastSummary"></div>
            <table id="statcastTable">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Exit Velocity</th>
                        <th>Trajectory</th>
                        <th>Distance</th>
                        <th>Hard Hit</th>
                    </tr>
                </thead>
                <tbody id="statcastBody"></tbody>
            </table>
        </section>

        <!-- Top Prospects Tab -->
        <section id="prospectsTab" class="tab-content">
            <h2>⭐ Top League Prospects</h2>
            <div class="filter-bar">
                <label>Filter by Position: </label>
                <select id="prospectPosFilter" onchange="renderProspects()">
                    <option value="ALL">All Positions</option>
                    <option value="P">Pitchers</option>
                    <option value="C">Catchers</option>
                    <option value="IF">Infielders</option>
                    <option value="OF">Outfielders</option>
                </select>
            </div>
            <table id="prospectsTable">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Organization</th>
                        <th>Position</th>
                        <th>Age</th>
                        <th>ETA</th>
                        <th>Potential</th>
                    </tr>
                </thead>
                <tbody id="prospectsBody"></tbody>
            </table>
        </section>

        <!-- Transactions Tab -->
        <section id="transactionsTab" class="tab-content">
            <h2>📰 League Transactions & Free Agents</h2>
            <div class="sub-nav">
                <button class="sub-btn active" onclick="switchTransSub('trades')">Recent Trades & Signings</button>
                <button class="sub-btn" onclick="switchTransSub('fa')">Available Free Agents</button>
                <button class="sub-btn" onclick="switchTransSub('il')">Injured List</button>
            </div>
            
            <div id="transTradesView">
                <table id="transactionsTable">
                    <thead>
                        <tr>
                            <th>Date / Details</th>
                        </tr>
                    </thead>
                    <tbody id="transactionsBody"></tbody>
                </table>
            </div>

            <div id="transFaView" style="display:none;">
                <table id="freeAgentsTable">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>Pos</th>
                            <th>Age</th>
                            <th>Prev Team</th>
                            <th>Demand / Value</th>
                        </tr>
                    </thead>
                    <tbody id="freeAgentsBody"></tbody>
                </table>
            </div>

            <div id="transIlView" style="display:none;">
                <table id="ilTable">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>Team</th>
                            <th>Injury</th>
                            <th>Expected Return</th>
                        </tr>
                    </thead>
                    <tbody id="ilBody"></tbody>
                </table>
            </div>
        </section>

        <!-- History & Awards Tab -->
        <section id="historyTab" class="tab-content">
            <h2>🏆 History & Award Winners</h2>
            <div class="history-grid">
                <div class="history-card">
                    <h3>World Series Champions</h3>
                    <ul id="championsList"></ul>
                </div>
                <div class="history-card">
                    <h3>Most Valuable Players</h3>
                    <ul id="mvpList"></ul>
                </div>
                <div class="history-card">
                    <h3>Cy Young Winners</h3>
                    <ul id="cyYoungList"></ul>
                </div>
                <div class="history-card">
                    <h3>Rookies of the Year</h3>
                    <ul id="rotyList"></ul>
                </div>
            </div>
        </section>
    </main>

    <!-- Team Summary Modal -->
    <div id="teamModal" class="modal">
        <div class="modal-content team-modal-content">
            <span class="close-btn" onclick="closeTeamModal()">&times;</span>
            <div id="teamModalHeader"></div>
            
            <div class="modal-subnav">
                <button class="modal-tab-btn active" onclick="switchTeamSubTab('teamOverview')">Overview</button>
                <button class="modal-tab-btn" onclick="switchTeamSubTab('teamLineups')">In-Game Lineups</button>
                <button class="modal-tab-btn" onclick="switchTeamSubTab('teamDiamond')">2D Diamond View</button>
                <button class="modal-tab-btn" onclick="switchTeamSubTab('teamSchedule')">Schedule & Box Scores</button>
                <button class="modal-tab-btn" onclick="switchTeamSubTab('teamFinancials')">Financials & Payroll</button>
                <button class="modal-tab-btn" onclick="switchTeamSubTab('teamProspects')">⭐ Team Prospects</button>
            </div>

            <div id="teamOverview" class="team-subtab-content active">
                <h3>Team Roster & Key Stats</h3>
                <div id="teamRosterContainer"></div>
            </div>

            <div id="teamLineups" class="team-subtab-content" style="display:none;">
                <div class="platoon-toggle">
                    <button class="platoon-btn active" id="btnVsRhp" onclick="toggleLineupPlatoon('vsRhp')">vs RHP</button>
                    <button class="platoon-btn" id="btnVsLhp" onclick="toggleLineupPlatoon('vsLhp')">vs LHP</button>
                </div>
                <h3>Starting Batting Lineup</h3>
                <table id="teamLineupTable">
                    <thead>
                        <tr>
                            <th>Order</th>
                            <th>Pos</th>
                            <th>Player</th>
                            <th>AVG</th>
                            <th>HR</th>
                            <th>OPS</th>
                        </tr>
                    </thead>
                    <tbody id="teamLineupBody"></tbody>
                </table>

                <h3 style="margin-top:20px;">Pitching Staff Roles</h3>
                <table id="teamPitchingStaffTable">
                    <thead>
                        <tr>
                            <th>Role</th>
                            <th>Pitcher</th>
                            <th>W-L</th>
                            <th>ERA</th>
                            <th>SV</th>
                            <th>IP</th>
                        </tr>
                    </thead>
                    <tbody id="teamPitchingStaffBody"></tbody>
                </table>
            </div>

            <div id="teamDiamond" class="team-subtab-content" style="display:none;">
                <h3>Starting Defensive Field Alignment</h3>
                <div class="baseball-field">
                    <div class="field-pos pos-p" id="diamondP">SP: --</div>
                    <div class="field-pos pos-c" id="diamondC">C: --</div>
                    <div class="field-pos pos-1b" id="diamond1B">1B: --</div>
                    <div class="field-pos pos-2b" id="diamond2B">2B: --</div>
                    <div class="field-pos pos-3b" id="diamond3B">3B: --</div>
                    <div class="field-pos pos-ss" id="diamondSS">SS: --</div>
                    <div class="field-pos pos-lf" id="diamondLF">LF: --</div>
                    <div class="field-pos pos-cf" id="diamondCF">CF: --</div>
                    <div class="field-pos pos-rf" id="diamondRF">RF: --</div>
                </div>
            </div>

            <div id="teamSchedule" class="team-subtab-content" style="display:none;">
                <h3>Game Results & Schedule</h3>
                <table id="teamScheduleTable">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Opponent</th>
                            <th>Result</th>
                            <th>Box Score</th>
                        </tr>
                    </thead>
                    <tbody id="teamScheduleBody"></tbody>
                </table>
            </div>

            <div id="teamFinancials" class="team-subtab-content" style="display:none;">
                <h3>Team Financial Overview</h3>
                <div class="financial-cards" id="teamFinancialCards"></div>
                <h4 style="margin-top:20px;">Player Contract Salaries</h4>
                <table id="teamContractTable">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>Position</th>
                            <th>Salary</th>
                            <th>Term / Expiration</th>
                        </tr>
                    </thead>
                    <tbody id="teamContractBody"></tbody>
                </table>
            </div>

            <div id="teamProspects" class="team-subtab-content" style="display:none;">
                <h3>Organizational Top Prospects</h3>
                <table id="teamProspectsTable">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Player</th>
                            <th>Pos</th>
                            <th>Age</th>
                            <th>ETA</th>
                            <th>Potential</th>
                        </tr>
                    </thead>
                    <tbody id="teamProspectsBody"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Box Score Modal -->
    <div id="boxModal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeBoxModal()">&times;</span>
            <div id="boxModalContent"></div>
        </div>
    </div>

    <!-- Player Card Modal -->
    <div id="playerModal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closePlayerModal()">&times;</span>
            <div id="playerCardBody"></div>
        </div>
    </div>

    <script src="app.js"></script>
</body>
</html>"""

    styles_css = """* { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
body { background-color: #f4f6f9; color: #333; line-height: 1.6; }
header { background: #1a252f; color: #fff; padding: 15px 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.15); }
.header-container { display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; flex-wrap: wrap; gap: 10px; }
.logo-title { display: flex; align-items: center; gap: 12px; }
.main-logo { height: 40px; }
.search-box input { padding: 8px 14px; border-radius: 20px; border: none; outline: none; width: 220px; font-size: 14px; }

nav { display: flex; gap: 8px; max-width: 1200px; margin: 15px auto 0; overflow-x: auto; padding-bottom: 5px; }
.nav-btn { background: #2c3e50; color: #ecf0f1; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-weight: 600; white-space: nowrap; transition: 0.2s; }
.nav-btn:hover, .nav-btn.active { background: #3498db; color: #fff; }

main { max-width: 1200px; margin: 20px auto; padding: 0 15px; }
.tab-content { display: none; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.tab-content.active { display: block; }

.sub-nav, .modal-subnav { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
.sub-btn, .modal-tab-btn { background: #e0e6ed; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: 600; }
.sub-btn.active, .modal-tab-btn.active { background: #2c3e50; color: #fff; }

table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }
th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #edf2f7; }
th { background-color: #f8fafc; font-weight: 700; color: #475569; text-transform: uppercase; font-size: 12px; letter-spacing: 0.5px; }
tr:hover { background-color: #f1f5f9; }

.team-link, .player-link { color: #2980b9; cursor: pointer; font-weight: 600; text-decoration: none; }
.team-link:hover, .player-link:hover { text-decoration: underline; }

.modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); backdrop-filter: blur(2px); }
.modal-content { background: #fff; margin: 40px auto; padding: 25px; border-radius: 10px; width: 90%; max-width: 850px; max-height: 85vh; overflow-y: auto; position: relative; }
.close-btn { position: absolute; right: 20px; top: 15px; font-size: 28px; cursor: pointer; color: #7f8c8d; }

.platoon-toggle { display: flex; gap: 10px; margin-bottom: 15px; }
.platoon-btn { background: #edf2f7; border: 1px solid #cbd5e1; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-weight: bold; }
.platoon-btn.active { background: #27ae60; color: #fff; border-color: #27ae60; }

/* 2D Baseball Diamond */
.baseball-field { position: relative; width: 100%; max-width: 450px; height: 350px; background: #2e7d32; margin: 20px auto; border-radius: 10px; border: 4px solid #1b5e20; overflow: hidden; }
.field-pos { position: absolute; background: rgba(0,0,0,0.8); color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; white-space: nowrap; transform: translate(-50%, -50%); border: 1px solid #ffd54f; }
.pos-p { top: 60%; left: 50%; }
.pos-c { top: 88%; left: 50%; }
.pos-1b { top: 52%; left: 78%; }
.pos-2b { top: 32%; left: 65%; }
.pos-3b { top: 52%; left: 22%; }
.pos-ss { top: 32%; left: 35%; }
.pos-lf { top: 18%; left: 20%; }
.pos-cf { top: 12%; left: 50%; }
.pos-rf { top: 18%; left: 80%; }

.financial-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-top: 15px; }
.fin-card { background: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #27ae60; }
.fin-card h4 { color: #64748b; font-size: 12px; text-transform: uppercase; }
.fin-card p { font-size: 20px; font-weight: bold; color: #1e293b; margin-top: 5px; }

.history-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-top: 15px; }
.history-card { background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; }
.history-card h3 { font-size: 16px; margin-bottom: 10px; color: #1a252f; border-bottom: 2px solid #3498db; padding-bottom: 5px; }
.history-card ul { list-style: none; padding-left: 0; }
.history-card li { padding: 6px 0; border-bottom: 1px dashed #cbd5e1; font-size: 13px; }

.view-box-btn { background: #3498db; color: #fff; border: none; padding: 4px 8px; border-radius: 3px; cursor: pointer; font-size: 11px; }
.view-box-btn:hover { background: #2980b9; }
"""

    app_js = """let leagueData = null;
let currentTeam = null;

document.addEventListener('DOMContentLoaded', () => {
    fetch('usbl_league_data.json')
        .then(res => res.json())
        .then(data => {
            leagueData = data;
            renderStandings();
            renderBatting();
            renderPitching();
            renderStatcast();
            renderProspects();
            renderTransactions();
            renderHistory();
        })
        .catch(err => console.error('Error loading league data:', err));
});

function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}

function renderStandings() {
    if (!leagueData || !leagueData.standings) return;
    const tbody = document.getElementById('standingsBody');
    tbody.innerHTML = '';
    leagueData.standings.forEach(st => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><a class="team-link" onclick="openTeamModal('${st.team_slug}')">${st.Team || st.TEAM}</a></td>
            <td>${st.W || 0}</td>
            <td>${st.L || 0}</td>
            <td>${st.PCT || '.000'}</td>
            <td>${st.GB || '-'}</td>
            <td>${st.WCGB || '-'}</td>
            <td>${st.HOME || '0-0'}</td>
            <td>${st.AWAY || '0-0'}</td>
            <td>${st.L10 || '0-0'}</td>
            <td>${st.STREAK || 'W1'}</td>
        `;
        tbody.appendChild(tr);
    });

    const wcBody = document.getElementById('wildcardBody');
    wcBody.innerHTML = '';
    const wcList = leagueData.wildcard_standings || leagueData.standings;
    wcList.forEach(st => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><a class="team-link" onclick="openTeamModal('${st.team_slug}')">${st.Team || st.TEAM}</a></td>
            <td>${st.W || 0}</td>
            <td>${st.L || 0}</td>
            <td>${st.PCT || '.000'}</td>
            <td>${st.WCGB || '-'}</td>
            <td>${st.L10 || '0-0'}</td>
            <td>${st.STREAK || 'W1'}</td>
        `;
        wcBody.appendChild(tr);
    });
}

function toggleStandings(view) {
    document.querySelectorAll('#standingsTab .sub-btn').forEach(b => b.classList.remove('active'));
    event.currentTarget.classList.add('active');
    if (view === 'division') {
        document.getElementById('divisionStandingsView').style.display = 'block';
        document.getElementById('wildcardStandingsView').style.display = 'none';
    } else {
        document.getElementById('divisionStandingsView').style.display = 'none';
        document.getElementById('wildcardStandingsView').style.display = 'block';
    }
}

function renderBatting() {
    if (!leagueData || !leagueData.batting_leaders) return;
    const tbody = document.getElementById('battingBody');
    tbody.innerHTML = '';
    leagueData.batting_leaders.forEach(b => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><a class="player-link" onclick="openPlayerCard('${b.Player}')">${b.Player}</a></td>
            <td>${b.Team}</td>
            <td>${b.G}</td>
            <td>${b.AB}</td>
            <td>${b.R}</td>
            <td>${b.H}</td>
            <td>${b['2B']}</td>
            <td>${b['3B']}</td>
            <td>${b.HR}</td>
            <td>${b.RBI}</td>
            <td>${b.BB}</td>
            <td>${b.SO}</td>
            <td>${b.SB}</td>
            <td>${b.AVG}</td>
            <td>${b.OBP}</td>
            <td>${b.SLG}</td>
            <td>${b.OPS}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderPitching() {
    if (!leagueData || !leagueData.pitching_leaders) return;
    const tbody = document.getElementById('pitchingBody');
    tbody.innerHTML = '';
    leagueData.pitching_leaders.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><a class="player-link" onclick="openPlayerCard('${p.Player}')">${p.Player}</a></td>
            <td>${p.Team}</td>
            <td>${p.W}</td>
            <td>${p.L}</td>
            <td>${p.ERA}</td>
            <td>${p.G}</td>
            <td>${p.GS}</td>
            <td>${p.SV}</td>
            <td>${p.IP}</td>
            <td>${p.H}</td>
            <td>${p.R}</td>
            <td>${p.ER}</td>
            <td>${p.HR}</td>
            <td>${p.BB}</td>
            <td>${p.SO}</td>
            <td>${p.WHIP}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderStatcast() {
    if (!leagueData || !leagueData.statcast_data) return;
    const tbody = document.getElementById('statcastBody');
    tbody.innerHTML = '';
    const list = leagueData.statcast_data.leaderboard || [];
    list.forEach((b, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>#${idx + 1}</td>
            <td><a class="player-link" onclick="openPlayerCard('${b.player}')">${b.player}</a></td>
            <td><strong>${b.ev} mph</strong></td>
            <td>${b.trajectory}</td>
            <td>${b.distance ? b.distance + ' ft' : '-'}</td>
            <td>${b.is_hard_hit ? '🔥 Yes' : 'No'}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderProspects() {
    if (!leagueData || !leagueData.top_prospects) return;
    const tbody = document.getElementById('prospectsBody');
    tbody.innerHTML = '';
    const posFilter = document.getElementById('prospectPosFilter').value;
    
    let list = leagueData.top_prospects || [];
    if (posFilter !== 'ALL') {
        list = list.filter(p => p.pos_group === posFilter);
    }

    list.forEach((p, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>#${idx + 1}</td>
            <td><a class="player-link" onclick="openPlayerCard('${p.Player}')">${p.Player}</a></td>
            <td>${p.Team || p.Organization}</td>
            <td>${p.Position}</td>
            <td>${p.Age || '-'}</td>
            <td>${p.ETA || '2018'}</td>
            <td>${p.Potential || '80/80'}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderTransactions() {
    if (!leagueData) return;
    const tBody = document.getElementById('transactionsBody');
    tBody.innerHTML = '';
    (leagueData.transactions || []).forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${t.details || t}</td>`;
        tBody.appendChild(tr);
    });

    const faBody = document.getElementById('freeAgentsBody');
    faBody.innerHTML = '';
    (leagueData.free_agents || []).forEach(fa => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><a class="player-link" onclick="openPlayerCard('${fa.Player || fa.Name}')">${fa.Player || fa.Name}</a></td>
            <td>${fa.Pos || fa.Position || 'UTL'}</td>
            <td>${fa.Age || '-'}</td>
            <td>${fa.PrevTeam || 'FA'}</td>
            <td>${fa.Demand || fa.Salary || '$1,500,000'}</td>
        `;
        faBody.appendChild(tr);
    });
}

function switchTransSub(view) {
    document.querySelectorAll('#transactionsTab .sub-btn').forEach(b => b.classList.remove('active'));
    event.currentTarget.classList.add('active');
    document.getElementById('transTradesView').style.display = view === 'trades' ? 'block' : 'none';
    document.getElementById('transFaView').style.display = view === 'fa' ? 'block' : 'none';
    document.getElementById('transIlView').style.display = view === 'il' ? 'block' : 'none';
}

function renderHistory() {
    if (!leagueData || !leagueData.history_awards) return;
    const h = leagueData.history_awards;
    const populate = (id, list) => {
        const el = document.getElementById(id);
        el.innerHTML = '';
        (list || []).forEach(item => {
            const li = document.createElement('li');
            li.innerText = typeof item === 'string' ? item : `${item.year}: ${item.winner}`;
            el.appendChild(li);
        });
    };
    populate('championsList', h.champions);
    populate('mvpList', h.mvp_winners);
    populate('cyYoungList', h.cy_young_winners);
    populate('rotyList', h.roty_winners);
}

function openTeamModal(slug) {
    currentTeam = slug;
    document.getElementById('teamModal').style.display = 'block';
    document.getElementById('teamModalHeader').innerHTML = `<h2>Team Overview (${slug.replace(/_/g, ' ').toUpperCase()})</h2>`;
    switchTeamSubTab('teamOverview');
    populate2DDiamond();
}

function closeTeamModal() {
    document.getElementById('teamModal').style.display = 'none';
}

function switchTeamSubTab(tabId) {
    document.querySelectorAll('.team-subtab-content').forEach(e => e.style.display = 'none');
    document.querySelectorAll('.modal-tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(tabId).style.display = 'block';
    event.currentTarget.classList.add('active');
}

function toggleLineupPlatoon(platoon) {
    document.querySelectorAll('.platoon-btn').forEach(b => b.classList.remove('active'));
    event.currentTarget.classList.add('active');
}

function populate2DDiamond() {
    if (!leagueData) return;
    document.getElementById('diamondP').innerText = 'SP: Starter';
    document.getElementById('diamondC').innerText = 'C: Catcher';
    document.getElementById('diamond1B').innerText = '1B: First Base';
    document.getElementById('diamond2B').innerText = '2B: Second Base';
    document.getElementById('diamond3B').innerText = '3B: Third Base';
    document.getElementById('diamondSS').innerText = 'SS: Shortstop';
    document.getElementById('diamondLF').innerText = 'LF: Left Field';
    document.getElementById('diamondCF').innerText = 'CF: Center Field';
    document.getElementById('diamondRF').innerText = 'RF: Right Field';
}

function openPlayerCard(name) {
    const modal = document.getElementById('playerModal');
    const body = document.getElementById('playerCardBody');
    body.innerHTML = `
        <h2>⚾ ${name}</h2>
        <p style="margin-top:10px;">Player profile card details, expanded scouting metrics, and split stats.</p>
    `;
    modal.style.display = 'block';
}

function closePlayerModal() {
    document.getElementById('playerModal').style.display = 'none';
}

function closeBoxModal() {
    document.getElementById('boxModal').style.display = 'none';
}

function filterTables() {
    const val = document.getElementById('globalSearch').value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(val) ? '' : 'none';
    });
}"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(styles_css)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)

    print("Generated dashboard files v18 successfully.")

if __name__ == '__main__':
    generate_dashboard_files_v18()
