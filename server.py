from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx, os

app = FastAPI()

# Allow your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = os.getenv("BASE_URL", "https://aipipe.org/openai/v1")
API_KEY = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    user_message = body.get("message", "")

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": user_message}]
            }
        )
        response.raise_for_status()
        data = response.json()
        return {"reply": data["choices"][0]["message"]["content"]}