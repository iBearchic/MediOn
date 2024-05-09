from fastapi import Header, FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, User, UserORM
from sqlalchemy.future import select
from utils.decorators import user_registered

app = FastAPI()

@app.post("/register/")
@user_registered(required=False)
async def register_user(user: UserORM,  db: AsyncSession = Depends(get_db)):
    new_user = User(
        telegram_nickname=user.telegram_nickname, 
        telegram_id=user.telegram_id)
    db.add(new_user)
    await db.commit()
    return {"message": "Вы успешно зарегистрированы!"}