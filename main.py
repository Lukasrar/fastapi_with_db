from fastapi import FastAPI, Request, status
import models
from database import engine
from routers import admin, auth, todos, user
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import RedirectResponse
app = FastAPI(
    title="FastAPI with DB",
)

models.Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# PAGES
@app.get('/')
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

# ENDPOINTS
@app.get("/health-check")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
