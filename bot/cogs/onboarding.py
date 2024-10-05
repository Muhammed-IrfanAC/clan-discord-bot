import discord
from discord import app_commands
from discord.ext import commands

class Onboarding(commands.cog): 
  def __init__(self, bot):
    self.bot = bot

  