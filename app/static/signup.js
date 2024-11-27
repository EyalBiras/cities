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
    window.location.href = "/";
  } catch (err) {
    signupError.textContent = err.message;
  }
}
