from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File storage paths
API_KEY_FILE = "user_api_key.txt"
USER_DATA_FILE = "user_data.json"

# ------------------ API Key Management ------------------

@app.post("/save_api_key")
async def save_api_key(request: Request):
    data = await request.json()
    api_key = data.get("api_key", "").strip()

    if not api_key:
        return {"message": "Invalid API Key."}

    # Save API key
    with open(API_KEY_FILE, "w") as file:
        file.write(api_key)

    return {"message": "API Key saved successfully!"}

@app.get("/get_api_key")
async def get_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as file:
            return {"api_key": file.read().strip()}
    return {"api_key": None}

# ------------------ Form Data Management ------------------

@app.post("/submit_form")
async def submit_form(request: Request):
    data = await request.json()

    # Save user financial data
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

    return {"message": "User data saved successfully!"}

@app.get("/get_user_data")
async def get_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {"message": "No user data found."}
