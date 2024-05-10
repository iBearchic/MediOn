import aiohttp


async def check_user_registration(telegram_id: int) -> bool:
    url = f"http://localhost:8000/check_registration/{telegram_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data.get("is_registered", False)
        