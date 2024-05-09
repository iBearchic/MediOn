from functools import wraps
from fastapi import Depends, HTTPException
from sqlalchemy.future import select
from database import  User, get_db

def user_registered(required: bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db = kwargs.get('db', None) or await Depends(get_db)()
            user = kwargs.get('user')

            result = await db.execute(select(User).filter_by(telegram_id=user.telegram_id))
            cand = result.scalars().first()

            if required and not cand:
                # Пользователь должен быть зарегистрирован, но его нет в базе данных
                return {"message": "Пройдите регистрацию, чтобы команда стала доступной"}
            elif not required and cand:
                # Пользователь не должен быть зарегистрирован, но он есть
                return {"message": f"Пользователь {user.telegram_nickname} уже зарегистрирован"}

            return await func(*args, **kwargs)
        return wrapper
    return decorator