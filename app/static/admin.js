async function runTournament() {
  try {
    await runTournamentAPI();
    alert('Ran tournament successfully');
  } catch (err) {
    alert(err.message);
  }
}