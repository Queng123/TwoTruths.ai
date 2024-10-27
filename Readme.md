# Description

This project was made during the AI/Journalism Hackathon in Berkeley, CA. The goal was to create a tool that helps news readers to understand if what they are reading as a lot of bias or not. This tool can also rewrite the text to make it less biased.

# How to use

## Backend

Build the backend:
```
cd backend
pip install -r requirements.txt
flask run --host=0.0.0.0 --port=5000
```

add a `.env` file with the following content
```
OPENAI_API_KEY
```

Install and run ngrok:
```
ngrok http http://localhost:5000 
```

## Frontend

Copy the add-on folder to the Chrome browser, on the extensions page.
Remember to change the URL in the `popup.js` file to the one provided by ngrok.

