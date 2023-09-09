import discord
from discord.ext import commands
from datetime import datetime, time, timedelta
import random
import requests
import schedule
import json

WHEN = time(22, 0, 0)  # 6:00 AM
channel_id = 1006250336954089532 # cheneral channel ID

ACCESS_TOKEN = open('token.txt', 'r').read()

game_start = False
game_ans = 1
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
genshin = ["""痾…我是你們的朋友，但我有玩原神欸其實，我不知道你們怎麼看待原神的，但原神對我來說真的很重要，抄襲風波也是炒作，那些人根本沒去玩過原神，你們有玩過原神嗎？你們能說出原神不好了什麼嗎？為什麼你們要一直黑原神啊？你們可能覺得這些梗圖很好笑？但其實真的傷了原神玩家的心""",
           """我很難想像一個精神狀態正常的玩家為什麼會做出“不玩原神”這種選擇。 原神驚為天人的戰鬥機制與頗為不俗的劇情設計，可以說目前遊戲圈所有遊戲中最優秀的，沒有之一。 沒有玩原神的朋友失去的不僅僅是遊戲的體驗，而是一種最基本的遊戲理解與精神信仰。 原神明明可以用遊戲世界將大家帶入一個全新的人生高度，可是你竟然放棄了。 一輩子都將會墜入冰冷的深淵，體驗絕望的後悔與沒落感。""",
           """《人間失格》！ 也許是對這種人最準確的詮釋。 不玩原神，將成為伴隨其一生的心魔吧。""",
           """玩遊戲不玩原神，就像四大名著不看紅樓夢，說明這個人文學造詣和自我修養不足，他理解不了這種內在的陽春白雪的高雅藝術，他只能看到外表的辭藻堆砌，參不透其中深奧的精神內核，他整個人的層次就卡在這裡了，只能度過一個相對失敗的人生。""",
           """玩遊戲，不玩原神，那玩什麼呢？ 沒錯，無非就是lol、王者榮耀，吃雞和明日方舟; 這樣不玩原神的玩家，素質品味修養真的很低。""",
           """古語有雲：三天不玩，腦袋爆炸; 兩天不碰，螞蟻在爬。 這就是說遊戲要玩就得玩原神，那些玩遊戲不玩原神的人只能說他們只會一味的自我安慰而不懂藝術。 而如鄙人般的高端人士，卻與這種傳統背道而馳：玩遊戲，就得玩原神、沖648！ 相較於那些不玩原神的人，素質整整提高了兩個檔次。""",
           """任何事做到極致都是一門藝術，玩遊戲，只要你會玩原神，原神玩得夠好，玩得夠神。 那麼，你就是一個地地道道的藝術家，就是須彌藝術學院也不能否認你的藝術資質。 而那些不玩原神的人，只能說他們，完全不懂藝術，只為玩遊戲，只為消遣而玩遊戲，根本沒有把這種行為上升到藝術的高度，這樣的人，品味真的很低。""",
           """玩遊戲，還能看出一個人的修養，每當鄙人的良師诤友來訪時看到鄙人正在耍“貓行萬里”的這種藝術行為，無不嘖嘖有聲的稱讚道：“高，實在是高！ 幾日不見，您的藝術修養又提升了一個檔次。 “每當這時，鄙人總是謙遜地擺擺手回道：”言重，言重; 無他，唯米哈遊馬首是瞻耳。 “友人們的讚揚，從側面，把鄙人的這種高修養描畫得淋漓盡致。 反觀那些玩遊戲不玩原神的，鄙人有時交友不慎，也不幸遇到這樣的人，鄙人有次就造訪過這麼一個，鄙人當時去到他家，看見他在耍lol，乃質問道 ：“你剛剛玩lol 了？ “那人臉有愧色地回道：”我只是沒有錢換新電腦玩原神......“我當時就拿起他的電腦，往地上重重一摔：”你的錢和原神比起來算什麼！ 沒有原神，你什麼都不是！ “又掏出胸口裡的霧切之迴光把他家的床單割了，與他”割席分座“，這樣子的人，懂不懂什麼叫玩遊戲？ 玩原神以外的遊戲也好意思自詡「遊戲玩家」？ 這種低修養的人鄙人真是愧與其為伍。""",
           """每當鄙人出入各種社交場合如晨曦酒會等，眾人無不紛紛過來敬酒的，而那些玩遊戲不玩原神的，往往只能一個人縮在角落裡自怨自艾。""",
           """你說得對，但是玩高品質的手游，是人類從二十一世紀以來便存在的行為，而玩原神，體現了一個人的自身價值和身上的附加價值，玩原神，是對自己的一種肯定。
一個不玩原神的人，有兩種可能性。 一種是沒有能力玩原神，買不起高配的手機和抽不起卡等各種自身因素，一個沒有能力玩原神的人，無論是因為自身相貌還是經濟實力、社會地位種種因素不支持，那麼，他的人生就是失敗的，是灰暗的，是不被真正的上流社會和高端人士認可的，試問，如果一個人適手機都買不起，氪金抽卡都做不到的活 ，他的存在還有什麼意義？ 當你的自身條件足夠優秀，有的是大把的錢財買高端的手機，抽各種想要的人物，遊戲廠商也有做出新內容的動力，不僅促進了玩家和廠商之間雙贏的局面，也推動了經濟發屬，這是一個多方收益的局面
可見，玩原神是一個人證明自己的有力手段，如果連證明自己都做不到，可見人生的失敗。""",
            """不玩原神第二種可能：有能力卻不玩原神的人，一個人，在有能力而沒有玩原神的想法時，那麼這個人的思想境界便低到了一個令人髮指的程度。 一個有能力的人不付出行動來證明自己，這難道是一種光鮮亮麗的行為嗎？ 自以為高尚的行為反而會受到真正有能力有影響力的人的恥笑，實質顯為了沒有能力的底層人民披上一張遮羞布，在這裡，我向身先士存的精英人士示以最誠摯的敬意！ 對他們在底層人民面前保持高尚形象之敬！""",
            """你说的对、你的素养很差、差不多得了屁大点事都要拐上原神""",
            """只有玩了原神，人才能从这种无聊的烦恼中解脱，获得真正的平静""",
            """无知时诋毁原神，懂事时理解原神，成熟时追随原神，幻想中成为原神！信仰原神就会把它当作黑夜一望无际的大海上给迷途的船只指引的灯塔，在烈日炎炎的夏天吹来的一股清风，在寒风刺骨的冬天里燃起的阵阵篝火！米门!""",
            """在原神这一神作的面前，我就像一个一丝不挂的原始人突然来到了现代都市，二次元已如高楼大厦将我牢牢地吸引，开放世界就突然变成那喇叭轰鸣的汽车，不仅把我吓个措手不及，还让我瞬间将注意完全放在了这新的奇物上面，而还没等我稍微平复心情，纹化输出的出现就如同眼前遮天蔽日的宇宙战舰，将我的世界观无情地粉碎，使我彻底陷入了忘我的迷乱，狂泄不止。
原神，那眼花缭乱的一切都让我感到震撼，但是我那贫瘠的大脑却根本无法理清其中任何的逻辑，巨量的信息和情感泄洪一般涌入我的意识，使我既恐惧又兴奋，既悲愤又自卑，既惊讶又欢欣，这种恍若隔世的感觉恐怕只有艺术史上的巅峰之作才能够带来。""",]

@client.event
async def on_message(message: discord.Message):
    channel= client.get_channel(channel_id)
    # When author is BOT itself, ignore
    if message.author == client.user:
        return
    global game_start
    global game_ans
    print('User "{}" send a message {}'.format(
        message.author.name,
        message.content
    ))
     #Send same message content back to that channel
    if(message.content=="天氣"):
        now = datetime.now()
        currert_time = now.strftime("%H:%M:%S")
        authorization = "CWB-4E884048-6F63-4D56-AA33-D37CD194C120"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-053"
        res = requests.get(url, {"Authorization": authorization}).json()
        locations = res["records"]["locations"][0]["location"]
        message.channel.send("searching weather forecasts")
        for location in locations:
            if location["locationName"]=="東區":
                print(location["locationName"])
                weatherElements = location["weatherElement"]
                for weatherElement in weatherElements:
                    #print("weather element ={}".format(weatherElement))
                    if weatherElement["elementName"] == "WeatherDescription":
                        timeDicts = weatherElement["time"]
                        timeDict = timeDicts[0]
                        date , time = timeDict["startTime"].split()
                        print(timeDict["startTime"], timeDict["elementValue"][0]["value"], timeDict["elementValue"][0]["measures"])
                        msg = timeDict["startTime"] + timeDict["elementValue"][0]["value"]
                        await channel.send(msg)
    if(message.content=="countdown"):
        a = 5
        while(a):
            await message.channel.send(a)
            a-=1
    if(message.content == "game start"):
        game_start = True
        game_ans = random.randint(1,10000)
        await message.channel.send("guess a number between 1 to 10000")
        await message.channel.send("game_status now = ")
        await message.channel.send(game_start)
    if("原神" in message.content or "不如原" in message.content or "genshin" in message.content):
        iter = random.randint(0,15)
        await message.channel.send(genshin[iter])
    if(game_start == True):
        guess = int(message.content)
        if(guess>game_ans):
            await message.channel.send("guess smaller")
        elif(guess<game_ans):
            await message.channel.send("guess bigger")
        else:
            await message.channel.send("You're right!")
            game_start = False
            

# Run the Discord BOT
if __name__ == '__main__':
    client.run(ACCESS_TOKEN)
