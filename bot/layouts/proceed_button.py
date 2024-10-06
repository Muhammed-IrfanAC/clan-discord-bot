import discord

class DynamicProceedView(discord.ui.View):
    def __init__(self, next_step_callback, restricted_callback):
        super().__init__()
        self.next_step_callback = next_step_callback
        self.restricted_callback = restricted_callback

    @discord.ui.button(label="Proceed", style=discord.ButtonStyle.blurple, emoji=discord.PartialEmoji(id=1292127779915300864, name="right_arrow"))
    async def proceed_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        async def role_checker(user: discord.Member):
          role = discord.utils.get(user.guild.roles, name="Trainers")
          return role in user.roles if role else False
        
        if self.restricted_callback:
          has_role = await role_checker(user=interaction.user)
          if has_role:
            await self.next_step_callback(interaction)
          else:
            await interaction.response.send_message(content="Please wait for a trainer before you proceed", ephemeral=True)
        else:
           await self.next_step_callback(interaction)
