async function makeRequest() {
  try {
      const response = await fetch('/info');
      const data = await response.text();
      document.getElementById('responseArea').value = JSON.stringify(JSON.parse(data), undefined, 4);
  } catch (error) {
      console.error('Request failed:', error);
  }
}

async function stopContainers() {
  try {
      await fetch('/stop', { method: 'POST' });
      alert('Stopping all containers...');
  } catch (error) {
      console.error('Failed to stop containers:', error);
  }
}

async function changeState(newState) {
  try {
      // PUT request to change the state
      let response = await fetch('/state', {
          method: 'PUT',
          headers: { 'Content-Type': 'text/plain' },
          body: newState
      });

      if (response.ok) {
          if (newState === 'INIT') {
              alert("System state changed to INIT");
              document.getElementById('responseArea').value = "";
              document.getElementById('runningButton').disabled = false;
              document.getElementById('shutdownButton').disabled = true;
              document.getElementById('pausedButton').disabled = true;
              document.getElementById('initButton').disabled = true;
          } else if (newState === 'SHUTDOWN') {
              console.log("Shutting down...");
          } else if (newState === 'RUNNING') {
              console.log("System is running...");
              alert("System state changed to RUNNING");
              document.getElementById('runningButton').disabled = true;
              document.getElementById('pausedButton').disabled = false;
              document.getElementById('initButton').disabled = false;
              document.getElementById('shutdownButton').disabled = false;
          } else if (newState === 'PAUSED') {
              console.log("System is paused...");
              alert("System state changed to PAUSED");
              document.getElementById('runningButton').disabled = false;
              document.getElementById('pausedButton').disabled = true;
              document.getElementById('initButton').disabled = false;
              document.getElementById('shutdownButton').disabled = false;
          }
      } else {
          if (response.status === 401) {
              alert("You need to re-login to perform this action.")
          }
          else {
              alert("Failed to change state to " + newState + 
                    ". Status code: " + response.status)
          }
      }
  } catch (error) {
      // Handle unexpected errors
      console.error('Error changing state:', error);
      alert('Unexpected error while changing state. Check console for details.');
  }
}

async function getState() {
  try {
      let response = await fetch('/state');
      if (response.ok) {
          let state = await response.text();
          document.getElementById('stateLogArea').value = "Current State: " + state;
      } else {
          alert('Failed to fetch state. Status code: ' + response.status);
      }
  } catch (error) {
      console.error('Error fetching state:', error);
      alert('Error fetching state. Check console for details.');
  }
}

async function getLog() {
  try {
      let response = await fetch('/run-log');
      if (response.ok) {
          let log = await response.text();
          document.getElementById('stateLogArea').value = log;
      } else {
          alert('Failed to fetch run log. Status code: ' + response.status);
      }
  } catch (error) {
      console.error('Error fetching run log:', error);
      alert('Error fetching run log. Check console for details.');
  }
}