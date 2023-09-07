import discord
import random
ACCESS_TOKEN = open('token.txt', 'r').read()

# Intents are bitwise values, identifying which correlate to a set of related events.
# Set all for convenience.
intents = discord.Intents.all()

# Create a client
# Represents a client connection that connects to Discord.
client = discord.Client(intents=intents)

# When the bot has successfully logged in to the server, on_ready() will be triggered.
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# When client send message, on_message() will be triggered.
@client.event
async def on_message(message: discord.Message):
    # When author is BOT itself, ignore
    if message.author == client.user:
        return
    
    print('User "{}" send a message {}'.format(
        message.author.name,
        message.content
    ))
    # Send same message content back to that channel
    if(message.content=="countdown"):
        a = 5
        while(a):
            await message.channel.send(a)
            a-=1
@client.event
async def guess(ans, message:discord.message):
    if message.author == client.user:
        return 0
    if int(message.content) > ans:
        await message.channel.send("guess smaller")
        return 1
    elif int(message.content) < ans:
        await message.channel.send("guess bigger")
        return 1
    elif int(message.content) == ans :
        await message.channel.send("you're right")
        return 0
    else:
        return 0
    
@client.event
async def game_start(message: discord.message):
    if message.author == client.user:
        return
    if message.content == "game start":
        ans = random.randint(1,10000)
        await message.channel.send("guess a number between 1 to 10000")
        while(guess(ans)!=0):
            guess(ans,message)


# Run the Discord BOT
if __name__ == '__main__':
    client.run(ACCESS_TOKEN)