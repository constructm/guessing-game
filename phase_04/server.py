from fastapi import FastAPI, Depends
from fastapi import HTTPException
from sqlmodel import Session
from contextlib import asynccontextmanager

from database import create_db_and_tables, get_session, engine, Session
from events import register_updated_at_listener, seed_game_levels
from models import User, UserCreate, UserRead, UserUpdate, Game, GameRead, GameCreate, GameUpdate, Guess
from crud import CRUDUser, CRUDGame

from datetime import datetime, timezone

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    register_updated_at_listener()
    with Session(engine) as session: 
        seed_game_levels(session)
    yield
    # Shutdown (optional cleanup code here)

app = FastAPI(lifespan=lifespan)


# --- User ---
@app.post("/users/", response_model=UserRead)
def create_new_user(user: UserCreate, session: Session = Depends(get_session)):
    return CRUDUser(session).create(user)

@app.get("/users/", response_model=list[UserRead])
def read_users(session: Session = Depends(get_session)):
    return CRUDUser(session).read()

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = CRUDUser(session).read(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = CRUDUser(session).update(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", response_model=UserRead)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    if not CRUDUser(session).read(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return CRUDUser(session).delete(user_id)



# --- Game ---
@app.post("/games/", response_model=GameRead)
def create_new_game(game: GameCreate, session: Session = Depends(get_session)):
    return CRUDGame(session).create_game(game)

@app.get("/games/", response_model=list[GameRead])
def read_games(session: Session = Depends(get_session)):
    return CRUDGame(session).read()

@app.get("/games/{game_id}", response_model=GameRead)
def read_game(game_id: int, session: Session = Depends(get_session)):
    game = CRUDGame(session).read(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="game not found")
    return game

@app.put("/games/{game_id}", response_model=GameRead)
def put_game(game_id: int, game_update: GameUpdate, session: Session = Depends(get_session)):
    game = CRUDGame(session).update(game_id, game_update)
    if not game:
        raise HTTPException(status_code=404, detail="game not found")
    return game


@app.get("/debug-time")
def debug_time():
    now = datetime.now(timezone.utc)
    from zoneinfo import ZoneInfo

    local_zone = ZoneInfo("Europe/Berlin")  # Or whatever zone you need

    local_time = now.astimezone(local_zone)

    # return {"utc_now": now.isoformat()}
    return {"utc_now": local_time.isoformat()}