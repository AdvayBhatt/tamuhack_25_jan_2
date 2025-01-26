from fastapi import FastAPI, Request
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_FILE = "user_api_key.txt"

@app.post("/save_api_key")
async def save_api_key(request: Request):
    data = await request.json()
    api_key = data.get("api_key", "").strip()

    if not api_key:
        return {"message": "Invalid API Key."}

    # Save API key to file
    with open(API_KEY_FILE, "w") as file:
        file.write(api_key)

    return {"message": "API Key saved successfully!"}

@app.get("/get_api_key")
async def get_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as file:
            return {"api_key": file.read().strip()}
    return {"api_key": None}
