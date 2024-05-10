from functools import wraps
from fastapi import Depends
from sqlalchemy.future import select
from database import  User, get_db

def user_registered(required: bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db = kwargs.get('db', None) or await Depends(get_db)()

            # Предположим, что объект с telegram_id передается в параметрах
            param_name = next((key for key, value in kwargs.items() if hasattr(value, 'telegram_id')), None)
            if not param_name:
                return {"message": "Не получить Ваш Telegram ID"}
            
            telegram_id = getattr(kwargs[param_name], 'telegram_id', None)

            result = await db.execute(select(User).filter_by(telegram_id=telegram_id))
            cand: User = result.scalars().first()

            if required and not cand:
                # Пользователь должен быть зарегистрирован, но его нет в базе данных
                return {"message": "Пройдите регистрацию, чтобы команда стала доступной"}
            elif not required and cand:
                # Пользователь не должен быть зарегистрирован, но он есть
                return {"message": f"Пользователь {cand.telegram_nickname} уже зарегистрирован"}

            return await func(*args, **kwargs)
        return wrapper
    return decorator