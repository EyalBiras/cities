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

// Helper function to fetch all available groups
async function getGroups() {
    const response = await fetch('/groups/', {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
    });
    if (!response.ok) {
        throw new Error('Failed to fetch groups');
    }
    return response.json();
}

// Function to display the list of available groups
async function displayAvailableGroups() {
    try {
        const groups = await getGroups();
        const groupsList = document.getElementById('availableGroupsList');
        groupsList.innerHTML = ''; // Clear any existing group items

        const user = await fetchUserInfo();
        if (!user.group) {
            groups.forEach((group) => {
                const groupItem = document.createElement('div');
                groupItem.classList.add('group-item');
                groupItem.innerHTML = `
                    <span>${group.name} - Owner: ${group.owner} - Members: ${group.members}</span>
                    <button onclick="requestToJoinGroup('${group.name}')">Join</button>
                `;
                groupsList.appendChild(groupItem);
            });
        } else {
            groupsList.innerHTML = `You must leave your group inorder to join a different one`
            groups.forEach((group) => {
                const groupItem = document.createElement('div');
                groupItem.classList.add('group-item');
                groupItem.innerHTML = `
                    <span>${group.name} - Owner: ${group.owner} - Members: ${group.members}</span>
                `;
                groupsList.appendChild(groupItem);
            });
        }
    } catch (error) {
        console.error('Error fetching groups:', error);
    }
}

// Function to request to join a group
async function requestToJoinGroup(groupName) {
    try {
        await sendJoinRequest(groupName); // Assume `sendJoinRequest` sends a request to the backend
        alert('Join request sent successfully!');
        displayAvailableGroups(); // Refresh the groups list
    } catch (err) {
        alert(err.message);
    }
}

// Function to handle logout
function logout() {
    localStorage.removeItem('token');
    window.location.href = "/";
}

// Initialize groups page on load
window.onload = () => {
    const token = localStorage.getItem('token');
    if (token) {
        displayAvailableGroups(); // Display the available groups when the page loads
    } else {
        window.location.href = "/"; // Redirect to login if no token
    }
};
