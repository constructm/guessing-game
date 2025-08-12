from typing import Optional, List
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from sqlmodel import SQLModel, Field, Relationship

def now_utc(): return datetime.now(ZoneInfo("Africa/Johannesburg"))

# ----------------------
# Database Table Models
# ----------------------

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
    username: str

    games: List["Game"] = Relationship(back_populates="user")


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
    ended_at: Optional[datetime] = None
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    game_level_id: Optional[int] = Field(default=None, foreign_key="game_level.id")
    secret_number: int
    status: str = Field(default="in_progress")  # in_progress, won, lost

    user: Optional[User] = Relationship(back_populates="games")
    guesses: List["Guess"] = Relationship(back_populates="game")
    # game_level_id: Optional[int] = Field(default=None, foreign_key="gamelevel.id")
    game_level: Optional["GameLevel"] = Relationship(back_populates="games")

class GameLevel(SQLModel, table=True):
    __tablename__ = "game_level"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
    level: str
    min: int
    max: int
    max_attempts: int
    
    games: list["Game"] = Relationship(back_populates="game_level")
    def __repr__(self):
        return f"GameLevels(level={self.level}, min={self.min}, max={self.max})"


class Guess(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
    game_id: int = Field(foreign_key="game.id")
    guess_value: int
    is_correct: bool

    game: Game = Relationship(back_populates="guesses")


# -------------------------
# Pydantic Models
# -------------------------

# --- User ---

class UserCreate(SQLModel):
    username: str
    


class UserRead(SQLModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True
    }



class UserUpdate(SQLModel):
    username: Optional[str] = None


# --- Game ---

class GameCreate(SQLModel):
    user_id: int
    secret_number: Optional[int] = None
    status: Optional[str] = None
    game_level_id: int


class GameRead(SQLModel):
    id: int
    # user_id: Optional[int]
    user: Optional[UserRead]
    # secret_number: int
    status: str
    created_at: datetime
    updated_at: datetime
    ended_at: Optional[datetime]
    # game_level_id: int
    game_level: Optional["GameLevelRead"]

    model_config = {
        "from_attributes": True
    }


class GameUpdate(SQLModel):
    status: Optional[str]
    ended_at: Optional[datetime]
    # user_id: Optional[int] = None
    # secret_number: int


# --- GameLevel ---
class GameLevelRead(SQLModel):
    id: int
    level: str
    
    model_config = {
        "from_attributes": True
    }


# --- Guess ---

class GuessCreate(SQLModel):
    game_id: int
    guess_value: int
    is_correct: bool


class GuessRead(SQLModel):
    id: int
    game_id: int
    guess_value: int
    is_correct: bool
    created_at: datetime
    updated_at: datetime