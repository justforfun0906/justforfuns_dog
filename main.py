import discord

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
    await message.channel.send(message.content)

# Run the Discord BOT
if __name__ == '__main__':
    client.run(ACCESS_TOKEN)