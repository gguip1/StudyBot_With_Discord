import discord
from discord.ext import commands
from utils.config import get_bot_token
import os
import asyncio

from utils.database import initialize_database

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    initialize_database()

# 비동기 명령어 등록 함수
async def register_commands():
    for folder in ['commands', 'events']:
        for filename in os.listdir(f'./{folder}'):
            if filename.endswith('.py'):
                try:
                    await bot.load_extension(f'{folder}.{filename[:-3]}')
                    print(f"Loaded {filename}")
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")

# 메인 실행 함수
async def main():
    await register_commands()  # 명령어 등록
    await bot.start(get_bot_token())  # 봇 실행

if __name__ == "__main__":
    asyncio.run(main())  # 비동기 실행
