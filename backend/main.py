from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from backend.app import App
from .requests import UserLoginRequest, UserLoginResponse, UserList

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def root():
    return RedirectResponse(url="/frontend/landingPage.html")

@app.post("/api/register")
async def register(payload: UserLoginRequest) -> UserLoginResponse:
    username = payload.name
    response = UserLoginResponse(True, username)
    ok = App.instance().add_user(username)
    if not ok:
        return UserLoginResponse(False, "Error: el usuario ya existe o está vacio")
    return response

@app.get("/api/users")
def users():
    return UserList(App.instance().list_users())