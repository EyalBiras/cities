async function loadGroups() {
  try {
    const groups = await getGroupsAPI();
    const groupsList = document.getElementById('availableGroupsList');
    groupsList.innerHTML = '';
    groups.forEach(group => {
      const groupItem = document.createElement('div');
      groupItem.classList.add('group-item');
      groupItem.innerHTML = `
        <span>${group.name}</span>
        <button onclick="startBattle('${group.name}')">Battle</button>
      `;
      groupsList.appendChild(groupItem);
    });
  } catch (error) {
    console.error('Failed to load groups:', error);
    alert(error.message);
  }
}

async function loadBattleHistory() {
  try {
    const battles = await getBattlesAPI();
    const battleHistoryList = document.getElementById('battleHistoryList');
    battleHistoryList.innerHTML = '';
    battles.forEach(battle => {
      const gameItem = document.createElement('div');
      gameItem.classList.add('game-item');
      gameItem.innerHTML = `
        <span>${battle}</span>
        <button onclick="downloadBattle('${battle}')">Download</button>
      `;
      battleHistoryList.appendChild(gameItem);
    });
  } catch (error) {
    console.error('Failed to load battle history:', error);
    alert(error.message);
  }
}

async function startBattle(groupName) {
  try {
    await startBattleAPI(groupName);
    alert(`Battle started with ${groupName}!`);
    loadBattleHistory();
  } catch (error) {
    console.error('Battle failed:', error);
    alert(error.message);
  }
}

async function downloadBattle(filename) {
  try {
    await downloadBattleAPI(filename);
  } catch (error) {
    console.error('Download failed:', error);
    alert(error.message);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadGroups();
  loadBattleHistory();

  // Periodic refresh
  setInterval(loadBattleHistory, 60000);  // Refresh every minute
});