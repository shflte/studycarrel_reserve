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
    0: "+",
    -1: "*",
    -2: "∅",
    -3: "!"
}

cancel_symbol = {
    0: "-",
    1: "∅",
    2: "~",
    -1: "!"
}

def get_reservation_time() -> arrow.Arrow:
    reservation = arrow.now()
    if reservation.minute < 30:
        reservation = reservation.replace(minute=0)
    else:
        reservation = reservation.replace(minute=30)
    return reservation

def date_to_time_slot_pair(date: arrow.Arrow) -> tuple:
    time_slot = (date.hour - 8) * 2
    if date.minute >= 30:
        time_slot += 1
    
    if time_slot + 7 > 27:
        return (time_slot, -1)
    return (time_slot, time_slot + 7)

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
        date = arrow.now().shift(days=10)

        for i in range(len(time_slots)):
            try:
                status = reserve_carrel(room, date, time_slots[i])
            except:
                status = -3
            message = \
                f"------討論室 [{room}] 預約狀態------\n" \
                f"Date: {date.format('YYYY-MM-DD')}\n" \
                f"Time: [{reserve_symbol[status]}] {time_slot_table[time_slots[i][0]]} - {time_slot_table[time_slots[i][1]]}\n"
            print(message)
            await channel.send(message)

    elif args.cancel:
        try:
            status = cancel_reservation()
        except:
            status = -1
        reservation = get_reservation_time()
        time_slots = date_to_time_slot_pair(reservation)

        message = \
            f"------討論室 [{room}] 取消狀態------\n" \
            f"Date: {reservation.format('YYYY-MM-DD')}\n" \
            f"Time: [{cancel_symbol[status]}] {time_slot_table[time_slots[0]]} ~ {time_slot_table[time_slots[1]]}\n"
        print(message)
        await channel.send(message)

# Run the bot
client.run(DISCORD_TOKEN)
