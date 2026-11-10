from fastapi import FastAPI, Request
import models
from database import engine
from routers import admin, auth, todos, user
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="FastAPI with DB",
)

models.Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# PAGES
@app.get('/')
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# ENDPOINTS
@app.get("/health-check")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
