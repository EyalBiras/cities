const API_URL = '';
// Function to get the token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('token');
}

async function runTournamentAPI() {
  const token = getAuthToken();
  const response = await fetch('/run_tournament', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to run tournament');
  }

  return response.json();
}