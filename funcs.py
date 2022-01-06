import os
import json
import time

import configs as cfg

bot = None

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

            emojiList[f":{emojis[emojiId]['name']}:"] = [
                f"https://cdn.discordapp.com/emojis/{emojiId}.png?size=64", [guild]]

    if(os.path.exists('emojis.json')):
        os.remove('emojis.json')

    f = open('emojis.json', 'w')
    json.dump(emojiList, f)
    f.close()
    loadEmotes()


def logger(ctx):

    if not ('guild_id' in ctx.keys()):
        guildName = "Direct-messages"
        channelName = f"{ctx['author']['username']}-{ctx['author']['id']}"
        guildPath = f"logger\\{guildName}"
        channelPath = guildPath + f"\\{channelName}.{cfg.logFormat}"

    else:
        guildName = bot.gateway.session.guild(ctx['guild_id']).name
        channelName = bot.gateway.session.guild(ctx['guild_id']).channelData(ctx['channel_id'])['name']
        guildPath = f"logger\\{guildName}_{ctx['guild_id']}"
        channelPath = guildPath + f"\\{channelName}-{ctx['channel_id']}.{cfg.logFormat}"

    if not(os.path.exists("logger")):
        os.makedirs("logger")

    if not(os.path.exists(guildPath)):
        os.makedirs(guildPath)

    if not(os.path.exists(channelPath)):
        with open(channelPath, "w") as f:
            f.write("==== BEGINNING ====\n")

    with open(channelPath, "a", encoding="utf-8") as f:
        timestamp = ctx['timestamp'].replace("T", " ")
        timestamp = timestamp.split(".")
        timestamp = timestamp[0]

        if('message_reference' in ctx.keys()): # checking if the message was a reply 
            f.write(f"REPLY TO: {ctx['message_reference']['message_id']}\n")
        f.write(
            f"{ctx['author']['username']}#{ctx['author']['discriminator']} AT {timestamp} --- Message ID {ctx['id']}\n{ctx['content']}\n\n")
        
        
