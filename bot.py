import discord

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents = intents)

# 調用event函式庫
@client.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {client.user}")

@client.event
# 當頻道有新訊息
async def on_message(message):
    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return
    # 新訊息包含Hello，回覆Hello, world!
    if message.content == "Hello":
        await message.channel.send("Hello, world!")

client.run("MTExMjMyMjI4MDc4MjA1NzU1NA.GqLqqL.1p0VP8YEHPJ6hQxahvIjHP4LxanLLohmWl3nyc")