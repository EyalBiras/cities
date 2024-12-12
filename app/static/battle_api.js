const API_URL = '';

// Function to get the token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('token');
}

async function startBattleAPI(groupName) {
  const token = getAuthToken();
  try {
    const response = await fetch(`/battle/${groupName}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to start battle');
    }

    return response.json();
  } catch (error) {
    console.error('Error starting battle:', error);
    throw error;
  }
}

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

async function downloadBattleAPI(enemy, filename) {
  const token = getAuthToken();
  try {
    const response = await fetch(`/download_battle/${enemy}/${filename}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to download battle');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading battle:', error);
    throw error;
  }
}

async function getGroupsAPI() {
  const token = getAuthToken();
  try {
    const response = await fetch('/get_groups_to_battle', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch groups');
    }

    return response.json();
  } catch (error) {
    console.error('Error fetching groups:', error);
    throw error;
  }
}