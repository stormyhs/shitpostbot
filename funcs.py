import os, json, time

def preventRatelimit(discreply):
    if "retry_after" in discreply.text:
        jdata = json.loads(discreply.text)
        print(f">{jdata['retry_after']} TIMEOUT")
        # wait as long as discord said + 0.5 so we dont get fucked for botting
        time.sleep(jdata['retry_after'] + 0.5)
    else:
        time.sleep(0.20)

def loadEmotes():
    global emoteDictionary
    f = open('emojis.json', 'r')
    emoteDictionary = json.load(f)
    f.close()

def getEmojis(bot, ctx):
    emojiList = {}
    for guild in bot.gateway.session.guilds:
        emojis = bot.gateway.session.guild(guild).emojis
        for emojiId in emojis.keys():
            if f":{emojis[emojiId]['name']}:" in emojiList:
                emojiList[f":{emojis[emojiId]['name']}:"][1].append(guild)
                continue

            emojiList[f":{emojis[emojiId]['name']}:"] = [f"https://cdn.discordapp.com/emojis/{emojiId}.png?size=64", [guild]]

    if(os.path.exists('emojis.json')):
        os.remove('emojis.json')

    f = open('emojis.json', 'w')
    json.dump(emojiList, f)
    f.close()
    loadEmotes()