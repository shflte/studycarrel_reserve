import os
from dotenv import load_dotenv
import discord
import argparse
import arrow

from web_interact import (
    reserve_carrel,
    cancel_reservation,
    get_reservation_table
)

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
parser.add_argument("-t", "--table", action="store_true", help="get reservation table")
args = parser.parse_args()

'''
status of reserving:
    reserved successfully: 0
    not available (reserved): -1
    not available (no such time slot): -2
    limit exceeded: -3
    unexpected error: -4

delete reservation:
    success: 0
    no reservation: 1
    no expiring reservation: 2
    unexpected error: -1
'''

# Define a dictionary of reserve status
reserve_symbol = {
    0: "啊哈!預約嚕!",
    -1: "已經被預約了",
    -2: "沒有這個時段",
    -3: "借太多囉",
    -4: "完蛋 有鬼"
}

cancel_symbol = {
    0: "啊哈!取消嚕!",
    1: "沒有任何預約",
    2: "沒有快到期的預約",
    -1: "完蛋 有鬼"
}

def reservation_str() -> str:
    message = "```\n"
    try:
        reservations = get_reservation_table()
        for reservation in reservations:
            message += f"{reservation[0]}, {reservation[1]}, {reservation[2]}\n"
        message += "```"
    except:
        message += "完蛋 有鬼 table壞了"
    return message

# Define an event handler for when the bot is ready
@client.event
async def on_ready():
    guild = client.get_guild(int(SH_GUILD_ID))
    channel = guild.get_channel(int(SH_TEXT_CHANNEL_ID))
    print('We have logged in as {0.user}'.format(client))
    print(args)
        
    room = "201"
    if args.reserve:
        time_slots = [
            (3, 10),
            (11, 18),
            (19, 26)
        ]
        date = arrow.now().shift(days=2)

        for i in range(len(time_slots)):
            try:
                status = reserve_carrel(room, date, time_slots[i])
            except:
                status = -4
            message = "預約結果：\n"
            message += f"{reserve_symbol[status]}\n"
            message += reservation_str()
            print(message)
            await channel.send(message)
        await client.close()

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

        message = "取消結果：\n"
        message += f"{cancel_symbol[status]}\n"
        message += reservation_str()
        if retry_count == 0:
            message += error_message

        print(message)
        await channel.send(message)
        await client.close()

    elif args.table:
        message = "預約列表：\n"
        message += reservation_str()

        print(message)
        await channel.send(message)
    
    # terminate the bot

# when a message is sent
@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        if message.content == '!table':
            table_str = "預約列表：\n"
            table_str += reservation_str()

            print(table_str)
            await channel.send(table_str)

# Run the bot
client.run(DISCORD_TOKEN)
