// Function to handle login form submission
async function login() {
  const username = document.getElementById('loginUsername').value;
  const password = document.getElementById('loginPassword').value;
  const loginError = document.getElementById('loginError');

  try {
    const token = await loginUser(username, password);
    localStorage.setItem('token', token);
    showDashboard();
  } catch (err) {
    loginError.textContent = err.message;
  }
}

// Function to handle signup form submission
async function signup() {
  const username = document.getElementById('signupUsername').value;
  const password = document.getElementById('signupPassword').value;
  const signupError = document.getElementById('signupError');

  try {
    await signupUser(username, password);
    alert('User created successfully! Please log in.');
    document.getElementById('signupUsername').value = '';
    document.getElementById('signupPassword').value = '';
  } catch (err) {
    signupError.textContent = err.message;
  }
}

// Helper function to fetch user info
async function fetchUserInfo() {
  const token = localStorage.getItem('token');
  const response = await fetch('/users/me/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error('Failed to fetch user info');
  }

  return response.json();
}

// Function to display available groups
async function displayAvailableGroups() {
  try {
    const groups = await getGroups();
    const groupsList = document.getElementById('availableGroupsList');
    groupsList.innerHTML = ''; // Clear previous list

    // Only show groups if user is not already in a group
    const user = await fetchUserInfo();
    if (!user.group) {
      groups.forEach(group => {
        const groupItem = document.createElement('div');
        groupItem.classList.add('group-item');
        groupItem.innerHTML = `
          <span>${group.name}</span>
          <button onclick="requestToJoinGroup('${group.name}')">Join Group</button>
        `;
        groupsList.appendChild(groupItem);
      });
      document.getElementById('availableGroupsSection').style.display = 'block';
    }
  } catch (error) {
    console.error('Error fetching groups:', error);
  }
}

// Function to update dashboard with user and group information
async function updateDashboard() {
  try {
    const user = await fetchUserInfo();
    document.getElementById('userInfo').innerHTML = `
      <p>Welcome, ${user.username}!</p>
      <p>Group: ${user.group || 'No Group'}</p>
    `;

    // Show/hide group-related sections
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
        document.getElementById('availableGroupsSection').style.display = 'none';
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

// Function to request to join a group
async function requestToJoinGroup(groupName) {
  try {
    await sendJoinRequest(groupName);
    alert('Join request sent successfully!');
    displayAvailableGroups(); // Refresh the groups list
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

// Function to show the dashboard after login
function showDashboard() {
  document.getElementById('loginForm').style.display = 'none';
  document.getElementById('signupForm').style.display = 'none';
  document.getElementById('dashboard').style.display = 'block';
  updateDashboard();
}

// Function to handle logout
function logout() {
  localStorage.removeItem('token');
  window.location.reload();
}
function showSignup() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('signupForm').style.display = 'block';
}

function showLogin() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('signupForm').style.display = 'none';
}
// Check if the user is logged in on page load
window.onload = () => {
  const token = localStorage.getItem('token');
  if (token) {
    showDashboard();
  }
};