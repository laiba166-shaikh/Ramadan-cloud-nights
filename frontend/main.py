import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "backend_url": BACKEND_URL},
    )
