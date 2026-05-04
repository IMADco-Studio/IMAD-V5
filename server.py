from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import threading
import random
import time
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from core import FacebookDirectAutomator
from utils import Logger

app = FastAPI(title="Professional Facebook Automation API")

# Serve UI files
@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.get("/style.css")
async def read_css():
    return FileResponse("style.css")

@app.get("/app.js")
async def read_js():
    return FileResponse("app.js")

# Store active bot instances
active_bots = {}

class BotConfig(BaseModel):
    email: str
    password: str
    post_id: str
    comments: List[str]
    min_delay: int = 15
    max_delay: int = 45

@app.get("/health")
def health_check():
    return {"status": "online", "version": "2.0.0 (Stealth Edition)"}

@app.post("/validate")
def validate_credentials(config: BotConfig):
    bot = FacebookDirectAutomator(config.email, config.password, headless=True)
    success = bot.login()
    bot.close()
    if success:
        return {"status": "success", "message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail="Login failed. Check credentials or checkpoint.")

@app.post("/start")
def start_bot(config: BotConfig):
    bot_id = f"bot_{config.post_id}"
    
    def run_loop():
        bot = FacebookDirectAutomator(config.email, config.password, headless=True)
        if bot.login():
            while True:
                comment = random.choice(config.comments)
                bot.post_comment(config.post_id, comment)
                delay = random.randint(config.min_delay, config.max_delay)
                Logger.info(f"Stealth delay for {delay}s...")
                time.sleep(delay)
        bot.close()

    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()
    return {"status": "success", "message": "Stealth bot started"}

if __name__ == "__main__":
    Logger.info("Starting Professional Automation Server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
