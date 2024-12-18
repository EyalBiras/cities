const tournamentResultsEl = document.getElementById('tournamentResults');
const availableGroupsListEl = document.getElementById('availableGroupsList');
const groupGamesSectionEl = document.getElementById('groupGamesSection');
const selectedGroupNameEl = document.getElementById('selectedGroupName');
const groupGamesListEl = document.getElementById('groupGamesList');

// Add error display function
function displayError(message) {
    const errorEl = document.createElement('div');
    errorEl.textContent = message;
    errorEl.style.color = 'red';
    tournamentResultsEl.appendChild(errorEl);
}

// Fetch tournament results
async function fetchTournamentResults() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/get_tournament_results', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const results = await response.json();
        console.log('Raw results:', JSON.stringify(results, null, 2));

        // Clear previous table rows
        const tableBody = tournamentResultsEl.querySelector('tbody');
        tableBody.innerHTML = '';

        // Populate the table with results
        Object.entries(results).forEach(([group, details]) => {
            const row = document.createElement('tr');
            const groupName = document.createElement('td');
            const totalScore = document.createElement('td');
            const wins = document.createElement('td');
            const losses = document.createElement('td');
            const draws = document.createElement('td');

            groupName.textContent = group;
            totalScore.textContent = details['total score'] || 0;
            wins.textContent = details['wins'] || 0;
            losses.textContent = details['losses'] || 0;
            draws.textContent = details['draws'] || 0;

            row.appendChild(groupName);
            row.appendChild(totalScore);
            row.appendChild(wins);
            row.appendChild(losses);
            row.appendChild(draws);

            // Add click event to the row
            row.addEventListener('click', () => {
                fetchGroupGames(group);
            });

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Failed to fetch tournament results:', error);
        displayError("Failed to load tournament results.");
    }
}
// Fetch groups
async function fetchGroups() {
    try {
        const response = await fetch('/groups', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const groups = await response.json();

        availableGroupsListEl.innerHTML = groups.map(group =>
            `<div class="group-item" data-group-name="${group.name}">${group.name}</div>`
        ).join('');

        // Add click event listeners to groups
        document.querySelectorAll('.group-item').forEach(groupEl => {
        groupEl.addEventListener('click', () => {
            const groupName = groupEl.dataset.groupName;
            fetchGroupGames(groupName);
        });
    });
    } catch (error) {
        console.error('Failed to fetch groups:', error);
    }
}

// Fetch group games
// Add this function to your existing script
function triggerDownload(url, fileName) {
    window.open(url, '_blank');
    window.location.href = url;
}

// Modify your fetchGroupGames function
async function fetchGroupGames(groupName) {
    try {
        const response = await fetch(`/get_group_games/${groupName}`);
        const games = await response.json();

        selectedGroupNameEl.textContent = groupName;
        groupGamesListEl.innerHTML = games.map(game =>
            `<div class="game-item" data-game-name="${game}">${game}</div>`
        ).join('');

        // Remove any existing event listeners before adding new ones
        groupGamesListEl.removeEventListener('click', gameClickHandler);
        groupGamesListEl.addEventListener('click', gameClickHandler);

        groupGamesSectionEl.style.display = 'block';
    } catch (error) {
        console.error('Failed to fetch group games:', error);
        displayError("Failed to load group games.");
    }
}
function gameClickHandler(event) {
    if (event.target.matches('.game-item')) {
        const gameName = event.target.textContent;
        console.log(`Game clicked: ${gameName}`);

        const downloadUrl = `/download_game/${gameName}`;
        const fileName = `${gameName}.zip`;

        console.log(`Attempting to download: ${fileName} from ${downloadUrl}`);

        triggerDownload(downloadUrl, fileName);
    }
}

// Modify your addClickHandler function
function addClickHandler(groupName) {
    groupGamesListEl.addEventListener('click', function(event) {
        if (event.target.matches('.game-item')) {
            const gameName = event.target.textContent;
            console.log(`Game clicked: ${gameName}`);

            // Assuming your API returns a URL for downloading the game
            const downloadUrl = `/download_game/${gameName}`;
            const fileName = `${gameName}.zip`; // Adjust file extension as needed

            console.log(`Attempting to download: ${fileName} from ${downloadUrl}`);

            triggerDownload(downloadUrl, fileName);

            // Add error handling
            if (!downloadUrl || !fileName) {
                console.error('Invalid download URL or filename');
                displayError("Failed to generate download link.");
            }
        }
    });
}

function triggerDownload(url, fileName) {
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Initialize
fetchTournamentResults();
fetchGroups();
