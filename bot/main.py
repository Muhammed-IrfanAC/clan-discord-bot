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
    for item in os.listdir("./bot/cogs"):
        if item.endswith(".py"):
            # Load individual command files
            extension = f"bot.cogs.{item[:-3]}"
        elif os.path.isdir(os.path.join("./bot/cogs", item)) and item != "__pycache__":
            # Load commands from subdirectories
            extension = f"bot.cogs.{item}"
        else:
            continue  # Skip if it's not a .py file or a directory
        
        # Check if the extension is already loaded
        if extension not in bot.extensions:
            try:
                await bot.load_extension(extension)
                print(f"Loaded extension: {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}: {e}")
    
    await bot.tree.sync(guild=discord.Object(id=1028955810128216135))

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')

bot.run(TOKEN)
