import os
import json
import time
import commands

import configs as cfg

bot = None


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


def loadGifs():
    print(">Loading Gifs...")
    if not (os.path.isfile("giflist.json")):
        print(">Gif list does not exist. Creating...")
        with open("giflist.json", "w") as gifFile:
            gifs = {
                "nigger": "https://media.discordapp.net/attachments/911923982821904427/924651985024720956/image0-16-1.gif"}
            json.dump(gifs, gifFile)
    else:
        with open("giflist.json", "r") as gifFile:
            gifs = json.loads(gifFile.read())
    return gifs


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
        channelName = bot.gateway.session.guild(ctx.guild_id).channel(ctx.channel_id)['name']
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
    if(ctx.author.id in commands.data):
        for emoji in commands.data[ctx.author.id]:
            ctx.addReaction(emoji)

    for word in ctx.content.split(" "):
        if(word in commands.data):
            for emoji in commands.data[word]:
                ctx.addReaction(emoji)
            break


def loadJson(filename, enctype='utf-16'):
    playlist_file = open(filename, encoding=enctype)
    playlists = json.load(playlist_file)
    playlist_file.close()
    return playlists


def writeJson(file, data, enctype='utf-16'):
    playlist_file = open(file, 'w', encoding=enctype)
    json.dump(data, playlist_file, indent=4, ensure_ascii=False)
    playlist_file.close()
