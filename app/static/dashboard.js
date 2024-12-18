// Helper function to fetch user info
async function fetchUserInfo() {
    const token = localStorage.getItem('token');
    const response = await fetch('/users/me/', {
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    });
    if (!response.ok) {
        throw new Error('Failed to fetch user info');
    }
    return response.json();
}

// Function to display available groups

// Function to update dashboard with user and group information
async function updateDashboard() {
  try {
    const user = await fetchUserInfo();
    document.getElementById('userInfo').innerHTML = `
      <p>Welcome, ${user.username}!</p>
      <p>Group: ${user.group || 'No Group'}</p>
    `;

    const groupSection = document.getElementById('groupSection');
    const joinRequestsSection = document.getElementById('joinRequests');

    if (user.group) {
      try {
        const joinRequests = await getJoinRequests();
        const requestsList = document.getElementById('requestsList');
        requestsList.innerHTML = '';
        joinRequests.forEach(request => {
          const li = document.createElement('li');
          li.innerHTML = `${request}
            <button onclick="acceptJoinRequest('${request}')">Accept</button>`;
          requestsList.appendChild(li);
        });
        joinRequestsSection.style.display = 'block';
      } catch (error) {
        console.error('Error fetching join requests:', error);
        joinRequestsSection.style.display = 'none';
      }
    } else {
      // If no group, show available groups
      joinRequestsSection.style.display = 'none';
      await displayAvailableGroups();
    }
  } catch (error) {
    console.error('Error updating dashboard:', error);
  }
}

// Function to create a new group
async function createNewGroup() {
  const groupName = document.getElementById('newGroupName').value;
  const groupError = document.getElementById('groupError');

  try {
    await createGroup(groupName);
    alert('Group created successfully!');
    updateDashboard();
  } catch (err) {
    alert(err.message);
  }
}


// Function to leave current group
async function leaveCurrentGroup() {
  try {
    await leaveGroup();
    alert('Left group successfully!');
    updateDashboard();
  } catch (err) {
    alert(err.message);
  }
}

// Function to accept a join request
async function acceptJoinRequest(username) {
  try {
    await api_acceptJoinRequest(username);
    alert(`Accepted ${username}'s join request!`);
    updateDashboard();
  } catch (err) {
    alert(err.message);
  }
}

// Function to logout
function logout() {
    localStorage.removeItem('token');
    window.location.href = "/";
}

// Initialize dashboard on load
window.onload = () => {
    const token = localStorage.getItem('token');
    if (token) {
        updateDashboard();
    }
};
async function downloadTemplate() {
    try {
        const response = await fetch('/download_template');
        if (!response.ok) {
            throw new Error('Download failed');
        }

        // Get the blob from the response
        const blob = await response.blob();

        // Create a URL for the blob
        const url = window.URL.createObjectURL(blob);

        // Create a temporary link element
        const link = document.createElement('a');
        link.href = url;
        link.download = 'Template.rar'; // The filename to save as

        // Append link to body, click it, and remove it
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Clean up the URL
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error downloading template:', error);
        alert('Failed to download template. Please try again.');
    }
}