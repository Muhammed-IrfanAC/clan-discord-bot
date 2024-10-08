import discord
from datetime import datetime

def eroor_embed_create(description):
    embed = discord.Embed(title="Error!", description=description, color=discord.Color.red())

    embed.set_thumbnail(url="https://media.giphy.com/media/TGxYxEusMpHqcuNAdi/giphy.gif?cid=ecf05e47g9yb19iaibdckjhly7ak4yp442f9ik5po9xg0bnu&ep=v1_gifs_search&rid=giphy.gif&ct=g")

    now = datetime.now()
    formatted_time = now.strftime("%B %d, %I:%M %p")
    
    embed.set_footer(text=f"FC-SLF Team \t |\t{formatted_time}", icon_url="https://i.ibb.co/dMPm9Yd/DALL-E-2024-10-02-08-16-40-A-dynamic-and-energetic-logo-for-a-Clash-of-Clans-group-named-FC-SLF-The.png")

    return embed