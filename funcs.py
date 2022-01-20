import os
import json
import time
import commands

import configs as cfg

bot = None
data = None


def preventRatelimit(discreply):
    if "retry_after" in discreply.text:
        jdata = json.loads(discreply.text)
        print(f">{jdata['retry_after']} TIMEOUT")
        # wait as long as discord said
        time.sleep(jdata['retry_after'])


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
    if not (hasattr(ctx, 'guild_id')):
        guildName = "Direct-messages"
        channelName = f"{ctx.author.username}-{ctx.author.id}"
        guildPath = f"logger\\{guildName}"
        channelPath = guildPath + f"\\{channelName}.{cfg.logFormat}"

    else:
        guildName = bot.gateway.session.guild(ctx.guild_id).name
        channelName = bot.gateway.session.guild(
            ctx.guild_id).channel(ctx.channel_id)['name']
        guildPath = f"logger\\{guildName}_{ctx.guild_id}"
        channelPath = guildPath + \
            f"\\{channelName}-{ctx.channel_id}.{cfg.logFormat}"

    if not(os.path.exists("logger")):
        os.makedirs("logger")

    if not(os.path.exists(guildPath)):
        os.makedirs(guildPath)

    if not(os.path.exists(channelPath)):
        with open(channelPath, "w") as f:
            f.write("==== BEGINNING ====\n")

    with open(channelPath, "a", encoding="utf-8") as f:
        timestamp = ctx.timestamp.replace("T", " ")
        timestamp = timestamp.split(".")
        timestamp = timestamp[0]

        if(hasattr(ctx, "message_reference")):  # checking if the message was a reply
            f.write(f"REPLY TO: {ctx.message_reference.message_id}\n")
        f.write(
            f"{ctx.author.username}#{ctx.author.discriminator} AT {timestamp} --- Message ID {ctx.id}\n{ctx.content}\n\n")


def handleReactSpam(ctx):
    reactSpamData = loadJson("reactspam.json")
    if(ctx.author.id in reactSpamData):
        for emoji in reactSpamData[ctx.author.id]:
            ctx.addReaction(emoji)

    wordReactSpamData = loadJson("wordreactspam.json")
    for word in ctx.content.split(" "):
        if(word in wordReactSpamData):
            for emoji in wordReactSpamData[word]:
                ctx.addReaction(emoji)
            break


def loadJson(filename, enctype='utf-16'):
    if not(os.path.exists(filename)):
        with open(filename, "w") as f:
            f.write("{}")

    with open(filename, encoding=enctype) as f:
        content = json.load(f)

    return content


def writeJson(file, data, enctype='utf-16'):
    playlist_file = open(file, 'w', encoding=enctype)
    json.dump(data, playlist_file, indent=4, ensure_ascii=False)
    playlist_file.close()


def loadData():
    print(">LOADING DATA:")
    print(">Loading Gifs...", end="\r")
    if not (os.path.isfile("giflist.json")):
        writeJson("giflist.json", {
                  "nigger": "https://media.discordapp.net/attachments/911923982821904427/924651985024720956/image0-16-1.gif"})
    print(">Loading Gifs... [OK]")

    print(">Loading Reacts...", end="\r")
    if not (os.path.isfile("reactspam.json")):
        writeJson("reactspam.json", {})
    print(">Loading Reacts... [OK]")

    print(">Loading Keyword Reacts...", end="\r")
    if not (os.path.isfile("wordreactspam.json")):
        writeJson("wordreactspam.json", {})
    print(">Loading Keyword Reacts... [OK]")

    print(">Loading Statuses...", end="\r")
    if not(os.path.exists("statuscycle.json")):
        writeJson("statuscycle.json", {})
    print(">Loading Statuses... [OK]")
