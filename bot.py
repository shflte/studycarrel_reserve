import os
from dotenv import load_dotenv
import discord
import argparse
import arrow

from web_interact import (
    reserve_carrel,
    cancel_reservation
)

time_slot_table = {
    1: "08:30-08:59",
    2: "09:00-09:29",
    3: "09:30-09:59",
    4: "10:00-10:29",
    5: "10:30-10:59",
    6: "11:00-11:29",
    7: "11:30-11:59",
    8: "12:00-12:29",
    9: "12:30-12:59",
    10: "13:00-13:29",
    11: "13:30-13:59",
    12: "14:00-14:29",
    13: "14:30-14:59",
    14: "15:00-15:29",
    15: "15:30-15:59",
    16: "16:00-16:29",
    17: "16:30-16:59",
    18: "17:00-17:29",
    19: "17:30-17:59",
    20: "18:00-18:29",
    21: "18:30-18:59",
    22: "19:00-19:29",
    23: "19:30-19:59",
    24: "20:00-20:29",
    25: "20:30-20:59",
    26: "21:00-21:29",
    27: "21:30-21:59",
    -1: "-"
}

load_dotenv()  # Load environment variables from .env file

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SH_GUILD_ID = os.getenv('SH_GUILD_ID')
SH_TEXT_CHANNEL_ID = os.getenv('SH_TEXT_CHANNEL_ID')

# Create a Discord client with intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# arg parser
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reserve", action="store_true", help="reserve a carrel")
parser.add_argument("-c", "--cancel", action="store_true", help="cancel a reservation")
args = parser.parse_args()

'''
status of reserving:
    reserved successfully: 0
    not available (reserved): -1
    not available (no such time slot): -2
    unexpected error: -3

delete reservation:
    success: 0
    no reservation: 1
    no expiring reservation: 2
    unexpected error: -1
'''

# Define a dictionary of reserve status
reserve_symbol = {
    0: "啊哈！預約嚕！",
    -1: "已經預約過了。",
    -2: "沒有這個時段。",
    -3: "完蛋，有鬼。"
}

cancel_symbol = {
    0: "啊哈！取消嚕！",
    1: "沒有預約。",
    2: "沒有快到預約時間的預約。",
    -1: "完蛋，有鬼。"
}

# Define an event handler for when the bot is ready
@client.event
async def on_ready():
    guild = client.get_guild(int(SH_GUILD_ID))
    channel = guild.get_channel(int(SH_TEXT_CHANNEL_ID))
    print('We have logged in as {0.user}'.format(client))
    print(args)
        
    if args.reserve:
        date = arrow.now().shift(days=3)

        try:
            status = reserve_carrel(date)
        except:
            status = -3
        message = f"---------------------------\n"
        message += f" 預約狀態: {reserve_symbol[status]}\n"
        print(message)
        await channel.send(message)

    elif args.cancel:
        retry_count = 5
        error_message = ""

        while retry_count > 0:
            try:
                status = cancel_reservation()
                break
            except Exception as e:
                error_message += f"Error: {e}\n"
                print(error_message)

            retry_count -= 1

        if retry_count == 0:
            status = -1

        message = f"---------------------------\n"
        message += f" 預約狀態: {reserve_symbol[status]}\n"
    
        if retry_count == 0:
            message += error_message

        print(message)
        await channel.send(message)
    
    # terminate the bot
    await client.close()

# Run the bot
client.run(DISCORD_TOKEN)
