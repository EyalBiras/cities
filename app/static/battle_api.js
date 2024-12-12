const API_URL = '';

// Function to get the token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('token');
}

async function downloadBattleAPI(enemyGroup, filename) {
  const token = getAuthToken();
  try {
    const response = await fetch(`/download_battle/${enemyGroup}/${filename}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to download battle');
    }

    const blob = await response.blob();

    // Create a temporary anchor element
    const link = document.createElement('a');

    // Set the href attribute to the blob URL
    link.href = window.URL.createObjectURL(blob);

    // Set the download attribute with the filename
    link.download = filename;

    // Append the element to the body and click it
    document.body.appendChild(link);
    link.click();

    // Remove the element and revoke the Object URL
    document.body.removeChild(link);
    window.URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error('Error downloading battle:', error);
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

async function downloadBattleAPI(enemyGroup, filename) {
  const token = getAuthToken();
  try {
    const response = await fetch(`/download_battle/${enemyGroup}/${filename}`, {
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
    document.body.removeChild(a);
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