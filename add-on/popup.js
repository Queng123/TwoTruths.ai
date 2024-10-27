const base_url = "https://8e55-2607-fb91-20c5-ce14-331d-644a-1588-a5db.ngrok-free.app"

document.getElementById("infoBtn").addEventListener("click", async () => {
  try {

    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      const currentTab = tabs[0]; 
      const currentUrl = currentTab.url;

      const response = await fetch(`${base_url}/info`, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({url: currentUrl})
        });
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();

      const [side1, side2] = data.two_sides.split("side 2: ").map(s => s.trim());
      document.getElementById("side1").innerHTML = `<b>${side1.replace("side 1: ", "").replaceAll("\"", "").trim()}</b>`;
      document.getElementById("side2").innerHTML = `<b>${side2.replaceAll("\"", "").trim()}</b>`;

      const [adjectives1, adjectives2] = data.adjectives.split("side 2: ").map(s => s.trim());
      document.getElementById("adjectives1").innerHTML = adjectives1.replace("side 1: ", "").replaceAll("\"", "").replace(/, /g, "<br>").trim();
      document.getElementById("adjectives2").innerHTML = adjectives2.replaceAll("\"", "").replace(/, /g, "<br>").trim();

      const [verbs1, verbs2] = data.verbs.split("side 2: ").map(s => s.trim());
      document.getElementById("verbs1").innerHTML = verbs1.replace("side 1: ", "").replaceAll("\"", "").replace(/, /g, "<br>").trim();
      document.getElementById("verbs2").innerHTML = verbs2.replaceAll("\"", "").replace(/, /g, "<br>").trim();

      const [verbs_act1, verbs_act2] = data.verbs_act.split("side 2: ").map(s => s.trim());
      document.getElementById("verbs_act1").innerHTML = verbs_act1.replace("side 1: ", "").replaceAll("\"", "").replace(/, /g, "<br>").trim();
      document.getElementById("verbs_act2").innerHTML = verbs_act2.replaceAll("\"", "").replace(/, /g, "<br>").trim();

      document.getElementById("response").textContent = `${data.bias}`;
      document.body.classList.toggle('active-info');
      document.body.classList.remove('active-rewrite');
      document.getElementById("slogan").style.display = "none";
    });
  } catch (error) {
    document.getElementById("response").textContent = "Error: " + error.message;
  }
});

document.getElementById("rewriteBtn").addEventListener("click", async () => {
  try {

    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      const currentTab = tabs[0]; 
      const currentUrl = currentTab.url;

      const response = await fetch(`${base_url}/rewrite`, {
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
      document.body.classList.toggle('active-rewrite');
      document.body.classList.remove('active-info');
      document.getElementById("slogan").style.display = "none";
    });
  } catch (error) {
    document.getElementById("response").textContent = "Error: " + error.message;
  }
});
