const leaderboardBody = document.getElementById('leaderboardBody');
const leaderboardMeta = document.getElementById('leaderboardMeta');
const leaderboardMessage = document.getElementById('leaderboardMessage');
const leaderboardTableWrapper = document.getElementById('leaderboardTableWrapper');
const refreshLeaderboardBtn = document.getElementById('refreshLeaderboardBtn');
let leaderboardLoaded = false;
let allLeaderboardRows = [];

document.addEventListener('DOMContentLoaded', () => {
    loadLeaderboard();

    if (refreshLeaderboardBtn) {
        refreshLeaderboardBtn.addEventListener('click', () => loadLeaderboard(true));
    }
});

async function loadLeaderboard(forceRefresh = false) {
    if (leaderboardLoaded && !forceRefresh) {
        updateView(allLeaderboardRows);
        return;
    }

    setLoadingState(forceRefresh ? 'Refreshing leaderboard…' : 'Loading leaderboard…');

    try {
        const response = await fetch('/api/leaderboard?top=50', { cache: 'no-store' });
        if (!response.ok) {
            const payload = await response.json().catch(() => ({}));
            const message = payload?.metadata?.message || 'No benchmark results available. Run benchmark.py to populate data.';
            updateLeaderboardMessage(message);
            return;
        }

        const data = await response.json();
        allLeaderboardRows = data.rows || [];

        if (!allLeaderboardRows.length) {
            updateLeaderboardMessage('Benchmark has not produced any leaderboard rows yet.');
            return;
        }

        leaderboardLoaded = true;

        if (leaderboardMeta) {
            const meta = data.metadata || {};
            const benchmarkRun = meta.benchmark_date_display
                || (meta.benchmark_timestamp_iso ? new Date(meta.benchmark_timestamp_iso).toLocaleDateString() : (meta.benchmark_timestamp || 'Unknown'));
            const totalModels = meta.total_models || allLeaderboardRows.length;
            leaderboardMeta.textContent = `Latest benchmark date: ${benchmarkRun} • Models evaluated: ${totalModels}`;
        }

        updateView(allLeaderboardRows);
    } catch (error) {
        console.error('Failed to load leaderboard:', error);
        updateLeaderboardMessage('Failed to load leaderboard. Please ensure the benchmark API is available.');
    }
}

function setLoadingState(message) {
    updateLeaderboardMessage(message);
}

function updateView(rows) {
    if (!rows.length) {
        updateLeaderboardMessage('No models match the selected filters yet.');
        renderLeaderboard([]);
        return;
    }

    hideLeaderboardMessage();
    renderLeaderboard(rows);
}

function hideLeaderboardMessage() {
    if (leaderboardMessage) {
        leaderboardMessage.style.display = 'none';
    }
    if (leaderboardTableWrapper) {
        leaderboardTableWrapper.style.display = 'block';
    }
}

function updateLeaderboardMessage(message) {
    if (leaderboardMessage) {
        leaderboardMessage.textContent = message;
        leaderboardMessage.style.display = 'block';
    }
    if (leaderboardTableWrapper) {
        leaderboardTableWrapper.style.display = 'none';
    }
}

function renderLeaderboard(rows) {
    if (!leaderboardBody) return;

    if (!rows.length) {
        leaderboardBody.innerHTML = '';
        if (leaderboardTableWrapper) {
            leaderboardTableWrapper.style.display = 'none';
        }
        return;
    }

    leaderboardBody.innerHTML = rows.map(row => {
        const accuracy = row.accuracy_pct != null ? `${row.accuracy_pct.toFixed(1)}%` : '—';
        const fp = row.false_positives != null ? row.false_positives : '0';
        const fn = row.false_negatives != null ? row.false_negatives : '0';
        const stdMatch = row.standard_match_pct != null
            ? `${row.standard_match_pct.toFixed(1)}%`
            : '—';
        const subMatch = row.subcategory_match_pct != null
            ? `${row.subcategory_match_pct.toFixed(1)}%`
            : '—';
        const runDate = row.run_date
            || (row.run_timestamp_iso ? new Date(row.run_timestamp_iso).toLocaleDateString() : (row.run_timestamp_raw || '—'));

        return `
            <tr>
                <td class="rank-cell">${row.rank}</td>
                <td class="model-cell">
                    <div class="model-name">${row.model_name}</div>
                    <div class="model-id">${row.model_id}</div>
                </td>
                <td class="provider-cell">${row.provider || '—'}</td>
                <td>${runDate}</td>
                <td>${accuracy}</td>
                <td>${fp}</td>
                <td>${fn}</td>
                <td>${stdMatch}</td>
                <td>${subMatch}</td>
                <td>${row.total_tests}</td>
            </tr>
        `;
    }).join('');
}

