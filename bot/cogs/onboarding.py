import discord
from discord import app_commands
from discord.ext import commands
from .. import coc_api
from .. import app_fonts
from .. layouts import embed
from .. layouts.proceed_button import DynamicProceedView

class Onboarding(commands.Cog): 
  def __init__(self, bot):
    self.bot = bot
    self.player_data = None

  @app_commands.command(name='start-onboarding', description='Start the onboarding process of a player')
  async def start_onboarding(self, interactin:discord.Interaction, member: discord.Member, player_tag : str):

    await interactin.response.defer()

    try:
      # Fetch the player's details from coc
      self.player_data = await coc_api.get_player_details(player_tag=player_tag) 
      # Welcome message embed
      welcome_embed = embed.create_embed(title=f'{app_fonts.welcome_title.format(name=self.player_data["name"])}', description=app_fonts.welcome_description)

      view = DynamicProceedView(next_step_callback=self.optional_guide, restricted_callback=False)

      await interactin.followup.send(content=member.mention ,embed=welcome_embed, view=view)
  
    except Exception as e:
      await interactin.followup.send(f"Error: {e}")
      return
    
  async def optional_guide(self, interaction: discord.Interaction):
    optional_embed = embed.create_embed(title=app_fonts.optional_title, description=app_fonts.optional_description)

    view = DynamicProceedView(next_step_callback=self.task_3, restricted_callback=False)

    await interaction.response.send_message(embed=optional_embed, view=view)

  async def task_3(self, interatction: discord.Interaction):
    task3_embed = embed.create_embed(title=app_fonts.task3_title, description=app_fonts.task3_description) 

    view = DynamicProceedView(next_step_callback=self.task_4, restricted_callback=True)

    await interatction.response.send_message(embed=task3_embed, view=view)

  async def task_4(self, interatction: discord.Interaction):
    task4_embed = embed.create_embed(title=app_fonts.task3_title, description=app_fonts.task3_description) 

    view = DynamicProceedView(next_step_callback=self.task_5, restricted_callback=True)

    await interatction.response.send_message(embed=task4_embed, view=view)

  async def task_5(self, interatction: discord.Interaction):
    task5_embed = embed.create_embed(title=app_fonts.task3_title, description=app_fonts.task3_description) 

    await interatction.response.send_message(embed=task5_embed)

async def setup(bot):
    await bot.add_cog(Onboarding(bot))
