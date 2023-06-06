from config import bot, dp
import asyncio
import start as start
import create_operation


async def main():
    dp.include_router(start.router)
    dp.include_router(create_operation.router)
    await dp.start_polling(bot)
    
    
asyncio.run(main())
