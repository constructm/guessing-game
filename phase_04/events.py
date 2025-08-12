from sqlalchemy import event
from sqlmodel import SQLModel
# from datetime import datetime
# from zoneinfo import ZoneInfo
from sqlmodel import Session, select
from models import now_utc, GameLevel

# def now_utc(): return datetime.now(ZoneInfo("Africa/Johannesburg"))

def register_updated_at_listener():
    def update_timestamp(mapper, connection, target):
        if hasattr(target, "updated_at"):
            target.updated_at = now_utc()

    for cls in SQLModel.__subclasses__():
        event.listen(cls, "before_update", update_timestamp)
        event.listen(cls, "before_insert", update_timestamp)

LEVELS = {
    'easy': {'min': 1, 'max': 10, 'max_attempts': 7},
    'medium': {'min': 1, 'max': 50, 'max_attempts': 7},
    'hard': {'min': 1, 'max': 100, 'max_attempts': 5},
    'hard-2': {'min': 1, 'max': 10000, 'max_attempts': 7},
    'hard-3': {'min': 1, 'max': 100000, 'max_attempts': 7},
    'extreme': {'min': 1, 'max': 1000000, 'max_attempts': 10},
    'impossible': {'min': 1, 'max': 1000000, 'max_attempts': 5}
}

def seed_game_levels(session: Session):
    for level_name, bounds in LEVELS.items():
        # Check if level already exists
        existing = session.exec(
            select(GameLevel).where(GameLevel.level == level_name)
        ).first()

        if not existing:
            game_level = GameLevel(
                level=level_name,
                min=bounds['min'],
                max=bounds['max'],
                max_attempts=bounds['max_attempts'],
                created_at=now_utc(),
                updated_at=now_utc()
            )
            session.add(game_level)

    session.commit()