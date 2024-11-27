// Function to handle login form submission
async function login() {
  const username = document.getElementById('loginUsername').value;
  const password = document.getElementById('loginPassword').value;
  const loginError = document.getElementById('loginError');

  try {
    const token = await loginUser(username, password);
    localStorage.setItem('token', token);
    window.location.href = "dashboard.html";
    showDashboard();
  } catch (err) {
    loginError.textContent = err.message;
  }
}

// Function to show the dashboard after login
function showDashboard() {
  document.getElementById('loginForm').style.display = 'none';
  document.getElementById('signupForm').style.display = 'none';
  document.getElementById('dashboard').style.display = 'block';
}

// Check if the user is logged in on page load
window.onload = () => {
  const token = localStorage.getItem('token');
  if (token) {
    window.location.href = "dashboard.html";
  }
};