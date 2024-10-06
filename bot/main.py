import os
import sys
import discord
from discord.ext import commands
from discord import Intents
from discord.ext.commands import Bot
from dotenv import load_dotenv
from discord import app_commands

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
TOKEN = os.getenv('PROD_BOT_TOKEN')

intents = Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def setup_hook():
    for filename in os.listdir("./bot/cogs"):
        if filename.endswith(".py"):
            extension = f"bot.cogs.{filename[:-3]}"
            await bot.load_extension(extension)
    await bot.tree.sync(guild=discord.Object(id=1028955810128216135))

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')

bot.run(TOKEN)
