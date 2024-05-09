from fastapi import HTTPException, FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, User, UserRegistration
from sqlalchemy.future import select

app = FastAPI()

@app.post("/register/")
async def register_user(user: UserRegistration,  db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).filter(User.telegram_id == user.telegram_id))
    if existing_user.scalars().first() is not None:
        return {"message": "Вы уже зарегистрированы!"}
    
    new_user = User(
        telegram_nickname=user.telegram_nickname, 
        telegram_id=user.telegram_id)
    db.add(new_user)
    await db.commit()
    return {"message": "Вы успешно зарегистрированы!"}