document.addEventListener('DOMContentLoaded', () => {
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
