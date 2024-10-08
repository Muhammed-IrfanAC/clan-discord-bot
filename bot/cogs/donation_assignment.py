import discord
from discord.ext import commands
from discord import app_commands
import random
from .. layouts.error_embed import eroor_embed_create

class RoleAssignment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.selection_hostory = []

    @app_commands.command(name='pick-donators', description='Pick the donators for war')
    async def assign_role(self, interaction: discord.Interaction, role: discord.Role):
        
        await interaction.response.send_message(content="<a:loading:1292784566964322355> *Picking random persons...* ")
        # Get all members in the guild who have the given role
        members_with_role = [member for member in interaction.guild.members if role in member.roles]
        
        if len(members_with_role) < 3:
            error_embed = eroor_embed_create(description="Not enough members with the role to assign donations")
            await interaction.edit_original_response(embed= error_embed)
            return

        # Randomly select three distinct members
        selected_members = random.sample(members_with_role, 3)

        available_memberss = [member for member in members_with_role if member not in self.selection_hostory]
        if len(members_with_role) < 3:
            error_embed = eroor_embed_create(description="Not enough distint members to assign doations without repeating")
            await interaction.edit_original_response(embed= error_embed)
            return

        # Assign roles
        assignments = {
            "HH": selected_members[0],
            "SB": selected_members[1],
            "SM": selected_members[2]
        }

        # Create a message with the assignments
        assignment_message = (
            f"## Donation assignments for upcoming war\n"
            f"<:HH:1292856700830875709>: {assignments['HH'].mention}\n\n"
            f"<:SB:1292856663274946621>: {assignments['SB'].mention}\n\n"
            f"<:SM:1292856684993052764>: {assignments['SM'].mention}\n\n"
            "*Please acknowledge to this message*"
        )

        await interaction.edit_original_response(content=assignment_message)

async def setup(bot):
    await bot.add_cog(RoleAssignment(bot))
