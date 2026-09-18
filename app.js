let leagueData = null;
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
}