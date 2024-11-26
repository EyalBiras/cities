const API_URL = '';
// Function to get the token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('token');
}

// Function to make a POST request for login
async function loginUser(username, password) {
  const response = await fetch(`${API_URL}/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: username,
      password: password,
    }),
  });
  if (!response.ok) {
    throw new Error('Invalid username or password');
  }
  const data = await response.json();
  return data.access_token;
}

// Function to sign up a new user
async function signupUser(username, password) {
  const response = await fetch('/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Signup failed');
  }

  return response.json();
}

// Function to create a group
async function createGroup(groupName) {
  const token = getAuthToken();
  const response = await fetch('/create_group', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': `Bearer ${token}`
    },
    body: new URLSearchParams({
      group_name: groupName
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to create group');
  }

  return response.json();
}

// Function to leave a group
async function leaveGroup() {
  const token = getAuthToken();
  const response = await fetch('/leave_group', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to leave group');
  }

  return response.json();
}

// Function to get all groups
async function getGroups() {
  const token = getAuthToken();
  const response = await fetch('/groups', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error('Failed to fetch groups');
  }

  return response.json();
}

// Function to send a join request
async function sendJoinRequest(groupName) {
  const token = getAuthToken();
  const response = await fetch('/join_request', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': `Bearer ${token}`
    },
    body: new URLSearchParams({
      group_name: groupName
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to send join request');
  }

  return response.json();
}

// Function to get join requests
async function getJoinRequests() {
  const token = getAuthToken();
  const response = await fetch('/get_join_requests', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch join requests');
  }

  return response.json();
}

// Function to accept a join request
async function api_acceptJoinRequest(username) {
  const token = getAuthToken();
  const response = await fetch('/accept_join_request', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': `Bearer ${token}`
    },
    body: new URLSearchParams({
      user: username
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to accept join request');
  }

  return response.json();
}