import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from .database import OnboardingDatabase
from .utils import delete_old_message, send_reminder, update_timer
from ...utils import coc_api, app_fonts
from ...layouts import embed
from ...layouts.error_embed import error_embed_create
from ...layouts.proceed_button import DynamicProceedView
from datetime import datetime, timedelta

class Onboarding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.pinned_message = {}
        self.db = OnboardingDatabase()
        
        # Load all players' states from the DB and recreate buttons if needed
        self.load_players()
        asyncio.create_task(self.recreate_buttons())

    def load_players(self):
        """Loads the player data from the database into memory."""
        rows = self.db.get_all_players()
        for row in rows:
            member_id, player_tag, current_step, end_time, channel_id, message_id = row
            self.players[member_id] = {
                'player_info': {'tag': player_tag},
                'current_step': current_step,
                'end_time': end_time,
                'channel_id': channel_id,
                'message_id': message_id
            }

    async def recreate_buttons(self):
        """Recreates buttons for ongoing onboarding processes."""
        for member_id, player_data in self.players.items():
            channel_id = player_data.get('channel_id')
            channel = await self.bot.fetch_channel(channel_id)
            await delete_old_message(channel, player_data.get('message_id'))

            if player_data['current_step'] == 1:
                embed_message = embed.create_embed(title=app_fonts.welcome_title.format(name=player_data['player_info']['tag']), description=app_fonts.welcome_description)
                view = DynamicProceedView(next_step_callback=self.optional_guide)
                await channel.send(embed=embed_message, view=view)

            elif player_data['current_step'] == 2:
                await self.send_step_2_buttons(channel, member_id)

            elif player_data['current_step'] == 3:
                await self.send_step_3_buttons(channel, member_id)

            elif player_data['current_step'] == 4:
                await self.send_step_4_buttons(channel, member_id)

            elif player_data['current_step'] == 5:
                await self.send_step_5_buttons(channel, member_id)

    async def send_step_2_buttons(self, channel, member_id):
        old_message_id = self.players[member_id].get('message_id')
        await delete_old_message(channel, old_message_id)
        optional_embed = embed.create_embed(title=app_fonts.optional_title, description=app_fonts.optional_description)
        view = DynamicProceedView(next_step_callback=self.task_3)
        await channel.send(embed=optional_embed, view=view)

    async def send_step_3_buttons(self, channel, member_id):
        old_message_id = self.players[member_id].get('message_id')
        await delete_old_message(channel, old_message_id)
        task3_embed = embed.create_embed(title=app_fonts.task3_title, description=app_fonts.task3_description) 
        view = DynamicProceedView(next_step_callback=self.task_4)
        await channel.send(embed=task3_embed, view=view)

    async def send_step_4_buttons(self, channel, member_id):
        old_message_id = self.players[member_id].get('message_id')
        await delete_old_message(channel, old_message_id)
        task4_embed = embed.create_embed(title=app_fonts.task4_title, description=app_fonts.task4_description) 
        view = DynamicProceedView(next_step_callback=self.task_5)
        await channel.send(embed=task4_embed, view=view)

    async def send_step_5_buttons(self, channel, member_id):
        old_message_id = self.players[member_id].get('message_id')
        await delete_old_message(channel, old_message_id)
        task5_embed = embed.create_embed(title=app_fonts.task5_title, description=app_fonts.task5_description) 
        await channel.send(embed=task5_embed)

    @app_commands.command(name='start-onboarding', description='Start the onboarding process of a player')
    async def start_onboarding(self, interaction: discord.Interaction, member: discord.Member, player_tag: str):
        await interaction.response.send_message(content="<a:loading:1292784566964322355> *Preparing onboarding process...* ")

        try:
            # Fetch player's details
            self.player_data = await coc_api.get_player_details(player_tag=player_tag)
            end_time = datetime.utcnow() + timedelta(days=7)
            self.players[member.id] = {
                'player_info': self.player_data,
                'end_time': end_time,
                'current_step': 1 
            }

            welcome_embed = embed.create_embed(title=f'{app_fonts.welcome_title.format(name=self.player_data["name"])}', description=app_fonts.welcome_description)
            view = DynamicProceedView(next_step_callback=self.optional_guide)

            message= await interaction.edit_original_response(content=member.mention, embed=welcome_embed, view=view)

            # Persist the player's state in the database
            self.db.save_player(member.id, player_tag, 1, end_time, interaction.channel.id, message.id)

            asyncio.create_task(send_reminder(self.bot, member.id, self.players))
            asyncio.create_task(update_timer(interaction.channel, member.id, self.players, self.pinned_message))


        except Exception as e:
            print(e)
            error_embed = error_embed_create(description=e)
            await interaction.edit_original_response(content=None, embed=error_embed, view=None)

    @app_commands.command(name='cancel-onboarding', description='Cancel the onboarding process for a player')
    async def cancel_onboarding(self, interaction: discord.Interaction, member: discord.Member):
        player_id = member.id

        await interaction.response.send_message(content="<a:loading:1292784566964322355> *Checking onboarding processes...* ")

        if player_id not in self.players:
            error_embed = error_embed_create(description=f"*Player {member.mention} is not currently in the onboarding process.*")
            await interaction.edit_original_response(content=None, embed=error_embed)
            return

        # Remove from memory and database
        del self.players[player_id]
        self.db.remove_player(player_id)

        if player_id in self.pinned_message and self.pinned_message[player_id]:
            await self.pinned_message[player_id].delete()
            del self.pinned_message[player_id]

        await interaction.edit_original_response(content=f"Onboarding process for {member.mention} has been cancelled.")

    async def optional_guide(self, interaction: discord.Interaction):
        player_id = interaction.user.id

        # Move to the next step
        self.players[player_id]['current_step'] = 2
        optional_embed = embed.create_embed(title=app_fonts.optional_title, description=app_fonts.optional_description)
        view = DynamicProceedView(next_step_callback=self.task_3)
        
        await interaction.response.send_message(embed=optional_embed, view=view)
        message = await interaction.original_response()
        self.db.save_player(player_id, self.players[player_id]['player_info']['tag'], 2, self.players[player_id]['end_time'], interaction.channel.id, message.id)

    async def task_3(self, interaction: discord.Interaction):
        player_id = interaction.user.id
        self.players[player_id]['current_step'] = 3
        task3_embed = embed.create_embed(title=app_fonts.task3_title, description=app_fonts.task3_description) 
        view = DynamicProceedView(next_step_callback=self.task_4)
        
        await interaction.response.send_message(embed=task3_embed, view=view)
        message = await interaction.original_response()
        self.db.save_player(player_id, self.players[player_id]['player_info']['tag'], 3, self.players[player_id]['end_time'], interaction.channel.id, message.id)

    async def task_4(self, interaction: discord.Interaction):
        player_id = interaction.user.id
        self.players[player_id]['current_step'] = 4
        task4_embed = embed.create_embed(title=app_fonts.task4_title, description=app_fonts.task4_description) 
        view = DynamicProceedView(next_step_callback=self.task_5)
        
        await interaction.response.send_message(embed=task4_embed, view=view)
        message = await interaction.original_response()
        self.db.save_player(player_id, self.players[player_id]['player_info']['tag'], 4, self.players[player_id]['end_time'], interaction.channel.id, message.id)

    async def task_5(self, interaction: discord.Interaction):
        player_id = interaction.user.id
        self.players[player_id]['current_step'] = 5
        task5_embed = embed.create_embed(title=app_fonts.task5_title, description=app_fonts.task5_description) 
        await interaction.response.send_message(embed=task5_embed)
        message = await interaction.original_response()
        self.db.save_player(player_id, self.players[player_id]['player_info']['tag'], 5, self.players[player_id]['end_time'], interaction.channel.id, message.id)