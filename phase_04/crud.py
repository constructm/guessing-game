from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
# from models import SQLModel, User, UserCreate, UserRead, UserUpdate, Game, GameCreate, GameUpdate, Guess
import models
from game import Game
import logging
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import random

# Configure logging
# logging.basicConfig(filename='logs/logfile.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# logger = logging.getLogger(__name__)

# --- Generic ---
class CRUDBase:

    def __init__(self, session: Session, model_class: type):
        self.session: Session = session
        self.model_class: type = model_class


    def create(self, model_create: models.SQLModel, validate: bool = True) -> models.SQLModel:
        model = self.model_class.model_validate(model_create) if validate else model_create
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model
    

    def read(self, model_id: int | None = None) -> list[models.SQLModel] | models.SQLModel:
        if model_id is not None:
            return self.session.get(self.model_class, model_id)
        else:
            return self.session.exec(select(self.model_class)).all()
    

    def get_by_field(self, field_name: str, value, return_first: bool = False) -> models.SQLModel | list[models.SQLModel]:
        query = select(self.model_class).where(getattr(self.model_class, field_name) == value)
        if return_first:    
            return self.session.exec(query).first()
        else:
            return self.session.exec(query).all()
    

    def update(self, model_id: int, model_update: models.SQLModel) -> models.SQLModel | None:
        model = self.session.get(self.model_class, model_id)
        if not model:
            return None

        model_data = model_update.model_dump(exclude_unset=True)
        for key, value in model_data.items():
            setattr(model, key, value)

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model


    def delete(self, model_id: int) -> models.SQLModel | None:
        model = self.session.get(self.model_class, model_id)
        if not model:
            return None
        self.session.delete(model)
        self.session.commit()
        return model


# --- User ---
class CRUDUser(CRUDBase):
    def __init__(self, session: Session):
        super().__init__(session=session, model_class=models.User)


# --- Game Level ---
class CRUDGameLevel(CRUDBase):

    def __init__(self, session: Session):
        super().__init__(session=session, model_class=models.GameLevel)

    def get_by_level(self, level: str) -> models.GameLevel | None:
        return self.get_by_field('level', level, return_first=True)
    
    def get_all_levels(self) -> list[models.GameLevel]:
        return self.read()
    

# --- Guess ---
class CRUDGuess(CRUDBase):

    def __init__(self, session: Session):
        super().__init__(session=session, model_class=models.Guess)

    def create_guess(self, game_id: int, guess_value: int, is_correct: bool) -> models.Guess:
        guess = models.Guess(game_id=game_id, guess_value=guess_value, is_correct=is_correct)
        return self.create(guess)
    
    def get_guesses_by_game_id(self, game_id: int) -> list[models.Guess]:
        return self.get_by_field('game_id', game_id)


# --- Game ---
class CRUDGame(CRUDBase):

    def __init__(self, session):
        super().__init__(session=session, model_class = models.Game)
    
    def has_open_game(self, session: Session, user_id: int) -> int | bool:
        active_game = session.exec(
            select(models.Game).where(
                models.Game.user_id == user_id,
                models.Game.status == 'in_progress'
            )
        ).first()
        return active_game.id if active_game else False
    
    def close_game(self, session: Session, game_id: int) -> bool:
        game = session.get(models.Game, game_id)
        if not game:
            return False
        
        game.status = 'closed'
        game.ended_at = models.now_utc()
        session.add(game)
        session.commit()
        return True
    
    def get_total_attempts(self, session: Session, game_id: int) -> int | bool:
        guesses = select(models.Game).where(models.Game.id == game_id).join(models.Guess).count()
        return guesses
    
    def generate_secret_number(self, game_level: models.GameLevel) -> int:
        return random.randint(game_level.min, game_level.max)
   
    
    def create_game(self, game_create: models.GameCreate) -> models.Game:

        data = game_create.model_dump()

        # clean-up: close open game if exists
        game_id = self.has_open_game(self.session, data['user_id'])
        if game_id: self.close_game(self.session, game_id)

        
        # prepare data for creation
        if data.get("status") in [None, 'string']: data["status"] = "in_progress"

        # Handle default level if not provided or zero
        if data.get("game_level_id") in [None, 0]:
            # game_level = self.get_by_field('level', 'easy', return_first=True)
            game_level = CRUDGameLevel(self.session).get_by_level('easy')
            
            if game_level:
                data["game_level_id"] = game_level.id
            else:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Default game level 'easy' not found in database."
                )
        else:
            # Validate that provided game_level_id exists
            game_level = CRUDGameLevel(self.session).read(data["game_level_id"])
            if not game_level:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=f"GameLevel with id {data['game_level_id']} does not exist.",
                )
            
        if data.get("secret_number") is None: 
            data["secret_number"] = self.generate_secret_number(game_level)

        return self.create(data)
    