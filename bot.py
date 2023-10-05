import os
from dotenv import load_dotenv
import discord
import argparse
import arrow

from web_interact import reserve_carrel

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
    27: "21:30-21:59"
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
parser.add_argument("-d", "--delete", action="store_true", help="delete a reservation")
args = parser.parse_args()

# Define a dictionary of reserve status
reserve_message = {
    0: "啊哈！預約嚕！",
    -1: "被約走ㄌ。",
    -2: "沒有這個時段。"
}

# Define an event handler for when the bot is ready
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(args)
    
    if args.reserve:
        room = "201"
        time_slots = [
            (3, 10),
            (11, 18),
            (19, 26)
        ]
        date = arrow.now().shift(days=10)
        return_status = reserve_carrel(room, date, time_slots)

        # send message to discord
        guild = client.get_guild(int(SH_GUILD_ID))
        channel = guild.get_channel(int(SH_TEXT_CHANNEL_ID))
        
        for i in range(len(time_slots)):
            message = f"討論室{room}預約狀態：\n" \
                        f"日期：{date.format('YYYY-MM-DD')}\n" \
                        f"時間：{time_slot_table[time_slots[i][0]]} - {time_slot_table[time_slots[i][1]]}\n" \
                        f"{reserve_message[return_status[i]]}\n"
            print(message)
            await channel.send(message)
    elif args.delete:
        pass

# Run the bot
client.run(DISCORD_TOKEN)
