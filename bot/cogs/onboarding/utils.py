import asyncio
import discord
from datetime import datetime
from ...utils import app_fonts

async def delete_old_message(channel, message_id):
    """Deletes the previous message if it exists."""
    try:
        if message_id:
            previous_message = await channel.fetch_message(message_id)
            await previous_message.delete()
    except discord.NotFound:
        pass

async def send_reminder(bot, player_id, players):
    """Sends a reminder to the player if they haven't completed their task in time."""
    while True:
        await asyncio.sleep(86400)
        if is_time_up(player_id, players):
            break
        
        current_step = players[player_id]["current_step"]
        if current_step in [4, 5]:
            continue

        user = await bot.fetch_user(player_id)
        await user.send(f"Reminder: You haven't completed step {current_step} in your onboarding process.")

async def update_timer(channel, player_id, players, pinned_message):
    """Updates the countdown timer pinned message every 24 hours."""
    while True:
        now = datetime.utcnow()
        end_time = players[player_id]['end_time']
        remaining_time = end_time - now

        if remaining_time.total_seconds() <= 0:
            await channel.send(f"## <@{player_id}>, your time for onboarding has expired!")
            break

        unix_timestamp = int(end_time.timestamp())

        timer_message = await channel.send(
            app_fonts.countdown_message.format(player_id=player_id, unix_timestamp=unix_timestamp)
        )

        if player_id in pinned_message and pinned_message[player_id]:
            await pinned_message[player_id].delete()

        pinned_message[player_id] = timer_message 
        await timer_message.pin()

        await asyncio.sleep(86400)

def is_time_up(player_id, players):
    """Checks if the time for onboarding is up."""
    end_time = players[player_id]["end_time"]
    return datetime.utcnow() >= end_time