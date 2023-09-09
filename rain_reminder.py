from discord.ext import commands
from datetime import datetime, time, timedelta
import requests
import json
import asyncio

bot = commands.Bot(command_prefix="$")
WHEN = time(22, 0, 0)  # 6:00 PM
channel_id = 1006250336954089532 # Put your channel id here
ACCESS_TOKEN = open('token.txt', 'r').read()

async def called_once_a_day():  # Fired every day
    await bot.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    channel = bot.get_channel(channel_id) # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
    now = datetime.now()
    currert_time = now.strftime("%H:%M:%S")
    authorization = "CWB-4E884048-6F63-4D56-AA33-D37CD194C120"
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-053"
    res = requests.get(url, {"Authorization": authorization}).json()
    locations = res["records"]["locations"][0]["location"]
    for location in locations:
        if location["locationName"]=="東區":
            print(location["locationName"])
            weatherElements = location["weatherElement"]
            for weatherElement in weatherElements:
                #print("weather element ={}".format(weatherElement))
                if weatherElement["elementName"] == "PoP12h":
                    timeDicts = weatherElement["time"]
                    for timeDict in timeDicts:
                        date , time = timeDict["startTime"].split()
                        if currert_time == time :
                            print(time, timeDict["elementValue"][0]["value"], timeDict["elementValue"][0]["measures"])
                            await channel.send(time, timeDict["elementValue"][0]["value"], timeDict["elementValue"][0]["measures"])

async def background_task():
    now = datetime.utcnow()
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration


if __name__ == "__main__":
    bot.loop.create_task(background_task())
    bot.run(ACCESS_TOKEN)