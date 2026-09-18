let leagueData = null;
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
}