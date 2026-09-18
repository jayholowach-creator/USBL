let leagueData = null;
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
}