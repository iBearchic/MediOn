from fastapi import FastAPI, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import UserHealthRecord, UserHealthRecordORM, get_db, User, UserORM
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

@app.post("/health_record/")
@user_registered(required=True)
async def create_health_record(record: UserHealthRecordORM, db: AsyncSession = Depends(get_db)):
    new_record = UserHealthRecord(**record.dict())
    db.add(new_record)
    await db.commit()
    return {"message": f"Информация по диагнозу: {record.disease} успешна добавлена! Спасибо!"}

@app.get("/check_registration/{telegram_id}")
async def check_user_registration(telegram_id: int = Path(..., description="The Telegram ID of the user to check"), db: AsyncSession = Depends(get_db)) -> bool:
    result = await db.execute(select(User).filter_by(telegram_id=telegram_id))
    user = result.scalars().first()
    return {"is_registered": user is not None}