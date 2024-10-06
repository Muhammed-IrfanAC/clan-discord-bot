import discord
from datetime import datetime

def create_embed(title, description, fields=None, color = discord.Color.dark_blue()):
  embed = discord.Embed(title=title, description=description, color=color)

  if fields:
    for name, value in fields.item():
      embed.add_field(name=name, value=value)

  now = datetime.now()
  formatted_time = now.strftime("%B %d, %I:%M %p")
  logo = '<:logo:1292119577634934868>'
  
  embed.set_footer(text=f"FC-SLF Team \t |\t{formatted_time}", icon_url="https://i.ibb.co/dMPm9Yd/DALL-E-2024-10-02-08-16-40-A-dynamic-and-energetic-logo-for-a-Clash-of-Clans-group-named-FC-SLF-The.png")

  return embed