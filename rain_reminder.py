import discord
import asyncio
import time
import requests
import json
import threading
from datetime import datetime, time, timedelta
from discord.ext import tasks
from discord.ext import commands

intents = discord.Intents.all()
client = discord.Client(intents = intents)
token = open('token.txt', 'r').read() #enter your bot's token and it should be a string
channel_id = 1006250336954089532 #enter your channel id and it should be a integer  
#bot = commands.Bot(intents= intents, command_prefix="$") 
channel = client.get_channel(channel_id)
@tasks.loop(seconds=10)
@client.event
async def weather(message: discord.Message):
    print("test")
    global channel
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
                        #if currert_time == time :
                        print(time, timeDict["elementValue"][0]["value"], timeDict["elementValue"][0]["measures"])
                        msg = timeDict["startTime"] + timeDict["elementValue"][0]["value"]
                        message.channel.send(msg)
# schedule.every(10).seconds.do(weather)
async def schedule_thread():
    await (weather.start(discord.Message))
t = threading.Thread(target=lambda: asyncio.run(schedule_thread()))
t.start()
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    

client.run(token)