import os
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PATCH", "DELETE"])
async def proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=f"{BACKEND_URL}/{path}",
            content=await request.body(),
            headers={"Content-Type": request.headers.get("Content-Type", "application/json")},
        )
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type"),
    )
