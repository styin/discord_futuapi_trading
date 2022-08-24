import os
import requests
import asyncio

import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

# Cog Extensions
extensions = [
    'client.cogs.utils_cog',
    'client.cogs.query_cog',
]

# API requests rate limit checker
r = requests.head(url="https://discord.com/api/v1")
try:
    print(f"[WARNING] Rate limit: {int(r.headers['Retry-After']) / 60} minutes left")
except:
    print("[LOG] Rate limit has not been reached")

# Bot Client
class botClient:
    # Bot Constructor
    def __init__(self, token=None):
        self.token = token or os.getenv('botSecret')
        self.bot = commands.Bot(command_prefix=os.getenv('PREFIX'), case_insensitive=True, intents=discord.Intents.all())
        self.on_ready = self.bot.event(self.on_ready)

    # on_ready event
    async def on_ready(self):  # When the bot is ready
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Success! Logged in as [{0}]".format(self.bot.user))
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("")
        print("API Trader Discord Bot -by sty")
        print("")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Current Build: {0}".format(os.getenv('VERSION')))
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    async def load_extensions(self):
        for extension in extensions:
            await self.bot.load_extension(extension)

    # bot boot up
    async def run(self):
        async with self.bot:
            await self.load_extensions()
            await self.bot.start(self.token)

# main function
def main():
    bot_obj = botClient()
    asyncio.run(bot_obj.run())
    

# Ensures this is the file being ran
if __name__ == '__main__':  
    main()
