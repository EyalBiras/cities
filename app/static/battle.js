async function loadBattleHistory() {
  try {
    const battles = await getBattlesAPI();
    console.log("Battles fetched:", battles);
    const battleHistoryList = document.getElementById('battleHistoryList');
    battleHistoryList.innerHTML = '';

    battles.forEach(battle => {
      const battleItem = document.createElement('div');
      battleItem.classList.add('battle-group');

      // Create group header
      const groupHeader = document.createElement('div');
      groupHeader.classList.add('battle-group-header');
      groupHeader.innerHTML = `
        <span>${battle}</span>
        <button onclick="toggleBattleGroup(this, '${battle}')">▶</button>
      `;
      battleItem.appendChild(groupHeader);

      // Create hidden files container
      const filesContainer = document.createElement('div');
      filesContainer.classList.add('battle-group-files');
      filesContainer.style.display = 'none';
      filesContainer.id = `files-${battle}`;
      battleItem.appendChild(filesContainer);

      battleHistoryList.appendChild(battleItem);
    });
  } catch (error) {
    console.error('Failed to load battle history:', error);
    alert(error.message);
  }
}

async function toggleBattleGroup(button, battle) {
  const filesContainer = document.getElementById(`files-${battle}`);

  // If files are not loaded yet
  if (filesContainer.children.length === 0) {
    try {
      const files = await getBattleDirectoryAPI(battle);
      console.log(`Files fetched for directory "${battle}":`, files);

      files.forEach(file => {
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');
        fileItem.innerHTML = `
          <span>${file}</span>
          <button onclick="downloadBattle('${battle}', '${file}')">Download</button>
        `;
        filesContainer.appendChild(fileItem);
      });
    } catch (error) {
      console.error('Failed to load directory files:', error);
      alert(error.message);
      return;
    }
  }

  // Toggle visibility and button icon
  if (filesContainer.style.display === 'none') {
    filesContainer.style.display = 'block';
    button.textContent = '▼';
  } else {
    filesContainer.style.display = 'none';
    button.textContent = '▶';
  }
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  console.log("Document loaded, initializing battle history...");
  loadBattleHistory();
});

async function loadDirectoryFiles(directory) {
  try {
    const files = await getBattleDirectoryAPI(directory);
    console.log(`Files fetched for directory "${directory}":`, files);
    const battleHistoryList = document.getElementById('battleHistoryList');
    battleHistoryList.innerHTML = '';

    files.forEach(file => {
      const fileItem = document.createElement('div');
      fileItem.classList.add('file-item');
      fileItem.innerHTML = `
        <span>${file}</span>
        <button onclick="downloadBattle('${directory}', '${file}')">Download</button>
      `;
      battleHistoryList.appendChild(fileItem);
    });
  } catch (error) {
    console.error('Failed to load directory files:', error);
    alert(error.message);
  }
}

function downloadBattle(enemyGroup, filename) {
  const fullPath = `${enemyGroup}/${filename}`;
  downloadBattleAPI(fullPath)
    .then(() => {
      console.log(`Successfully downloaded ${filename}`);
    })
    .catch(error => {
      console.error('Download failed:', error);
      alert(`Failed to download file: ${error.message}`);
    });
}

// Confirming that the initialization calls are made
document.addEventListener('DOMContentLoaded', () => {
  console.log("Document loaded, initializing battle history...");
  loadBattleHistory();
});

// Updated battle_api.js
async function getBattlesAPI() {
  const token = getAuthToken();
  try {
    const response = await fetch('/get_battles', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch battles');
    }

    return response.json();
  } catch (error) {
    console.error('Error fetching battles:', error);
    throw error;
  }
}

async function getBattleDirectoryAPI(directory) {
  const token = getAuthToken();
  try {
    const response = await fetch(`/get_battle/${directory}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch directory contents');
    }

    return response.json();
  } catch (error) {
    console.error('Error fetching directory contents:', error);
    throw error;
  }
}
async function loadAvailableGroups() {
  try {
    const groups = await getGroupsAPI();
    console.log("Available groups:", groups); // Debugging log
    const availableGroupsList = document.getElementById('availableGroupsList');
    availableGroupsList.innerHTML = '';

    groups.forEach(group => {
      const groupItem = document.createElement('div');
      groupItem.classList.add('group-item');

      groupItem.innerHTML = `
        <span>${group.name}</span>
        <button onclick="startBattle('${group.name}')">Battle</button>
      `;

      availableGroupsList.appendChild(groupItem);
    });
  } catch (error) {
    console.error('Failed to load available groups:', error);
    alert(error.message);
  }
}

function startBattle(groupName) {
  startBattleAPI(groupName)
    .then(() => {
      alert(`Battle with ${groupName} started successfully!`);
      loadBattleHistory(); // Refresh battle history after starting a battle
    })
    .catch(error => {
      console.error('Battle start failed:', error);
      alert(`Failed to start battle: ${error.message}`);
    });
}

// Update the document load event listener
document.addEventListener('DOMContentLoaded', () => {
  console.log("Document loaded, initializing battle components...");
  loadBattleHistory();
  loadAvailableGroups();
});