(async () => {
  const pageData = {
    url: window.location.href,
    title: document.title,
    content: document.body.innerText
  };

  try {
    await fetch("http://172.20.10.2:5000/check-page", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(pageData)
    });
    console.log("Données envoyées à l'API avec succès.");
  } catch (error) {
    console.error("Erreur lors de l'envoi des données à l'API :", error);
  }
})();
