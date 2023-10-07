import os
from dotenv import load_dotenv
import discord
import argparse
import arrow
from apscheduler.schedulers.blocking import BlockingScheduler

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

def help_message() -> str:
    help_message = "指令列表：\n"
    help_message += "```\n"
    help_message += "!table\n"
    help_message += "!reserve time_slot [day_offset] [room]\n"
    help_message += "!cancel\n"
    help_message += "!help\n"
    help_message += "```"

    return help_message

def check_reservation(reserve_time: float, day_offset: int, room: str):
    # check all conditions
    if not reserve_time % 0.5 == 0:
        raise Exception("Invalid time slot")
    if not 0 <= reserve_time <= 23.5:
        raise Exception("Invalid time slot")
    if not day_offset >= 0:
        raise Exception("Invalid day offset")
    if not room in ["201", "202", "203"]:
        raise Exception("Invalid room")

def get_time_slot(reserve_time: float) -> tuple:
    begin_time_slot = int((reserve_time - 8) * 2)
    return [
        (begin_time_slot, begin_time_slot + 7),
        (begin_time_slot + 8, begin_time_slot + 15),
        (begin_time_slot + 16, begin_time_slot + 23)
    ]

def reservation_str() -> str:
    message = ""
    try:
        message = "```\n"
        reservations = get_reservation_table()
        for reservation in reservations:
            message += f"{reservation[0]}, {reservation[1]}, {reservation[2]}\n"
        message += "```"
    except:
        message = "完蛋 有鬼 table壞了"
    return message

# Define an event handler for when the bot is ready
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(args)

# when a message is sent
@client.event
async def on_message(message):
    channel = message.channel
    guild = message.guild

    if message.author == client.user:
        return

    if message.content.startswith('!'):
        if message.content == '!table':
            table_str = "預約列表：\n"
            table_str += reservation_str()

            print(table_str)
            await channel.send(table_str)

        elif message.content.startswith('!reserve'):
            room = "201"
            day_offset = 0
            try:
                if len(message.content.split()) == 4:
                    reserve_time = float(message.content.split()[1])
                    day_offset = int(message.content.split()[2])
                    room = message.content.split()[3]
                elif len(message.content.split()) == 2:
                    reserve_time = float(message.content.split()[1])
                else:
                    raise Exception("Invalid command")
                check_reservation(reserve_time, day_offset, room)
            except:
                await channel.send("Σ(ﾟДﾟ；≡；ﾟдﾟ)")
                await channel.send(help_message())
                return
            
            date = arrow.now().shift(days=day_offset)

            for time_slot in get_time_slot(reserve_time):
                try:
                    status = reserve_carrel(room, date, time_slot)
                except:
                    status = -4
                message = "預約結果：\n"
                message += f"{reserve_symbol[status]}\n"
                message += reservation_str()
                print(message)
                await channel.send(message)

        elif message.content == '!cancel':
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

        elif message.content == '!help':
            await channel.send(help_message())

        else:
            await channel.send("Σヽ(ﾟД ﾟ; )ﾉ")
            await channel.send(help_message())

# Run the bot
client.run(DISCORD_TOKEN)
