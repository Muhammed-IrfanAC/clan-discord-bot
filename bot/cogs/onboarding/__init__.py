from .onboarding import Onboarding

async def setup(bot):
    await bot.add_cog(Onboarding(bot))