import random

import discord
from discord.ext import commands

with open('token.txt', 'r') as f:
    ACCESS_TOKEN = f.readline()

# Create a bot
# Represents a bot connection that connects to Discord.
bot = commands.Bot(['/'], intents=discord.Intents.all())

answer = ''
dictionary = []

# Add more words in dictionary.txt
with open('dictionary.txt', 'r') as f:
    dictionary = f.read().split()

# When the bot has successfully logged in to the server, on_ready() will be triggered.
@bot.event
async def on_ready():
    print(f'We have logged in as `{bot.user}`!!')

# Handle reset command
@bot.command()
async def reset(ctx: commands.Context):

    global answer
    answer = random.choice(dictionary)
    print(f'{ctx.author} start a new game.')
    await ctx.send(f'{ctx.author} start a new game.')


# Handle guess command
@bot.command()
async def guess(ctx: commands.Context, arg: str):

    if answer == '':
        await reset(ctx)

    # TODO:
    # if <condition>:
    #     return await ctx.send(f'Invalid guess.')
    
    # 0: black, 1: green, 2: yellow
    status = [1 for i in range(5)]  

    # TODO: 
    # modify status list

    send_message = f'{arg}\n'
    for i in status:
        send_message += '⬛' if i == 0 else '🟩' if i == 1 else '🟨'
    await ctx.send(send_message)

# Run the Discord BOT
if __name__ == '__main__':
    bot.run(ACCESS_TOKEN)
