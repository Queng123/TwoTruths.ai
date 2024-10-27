document.getElementById("infoBtn").addEventListener("click", () => {
  fetchBackendData("info");
});

document.getElementById("rewriteBtn").addEventListener("click", () => {
  fetchBackendData("rewrite");
});

async function fetchBackendData(action) {
  try {

    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      const currentTab = tabs[0]; 
      const currentUrl = currentTab.url;

      const response = await fetch(`https://0468-2607-fb91-20ca-c5a0-2fb9-923d-e34b-c9db.ngrok-free.app/${action}`, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({url: currentUrl})
        });
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      document.getElementById("response").textContent = data.message;
    });
  } catch (error) {
    document.getElementById("response").textContent = "Error: " + error.message;
  }
}
