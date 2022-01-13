import os
import json
import requests
import funcs
import time
import emoji
import random
import threading
import ctx as context
import statuscycle

gifs = {}
bot = None
data = {'userid': {}, 'keyword': {}}
statusCycleThread = threading.Thread(target=statuscycle.cycle)


def messageSpam(ctx):
    content = ctx.content[5:]
    content = content.split(" ")
    try:
        amount = int(content[1])
    except:
        amount = 5
    if not content[0] in gifs:
        content = content[0]
    else:
        content = gifs[content[0]]

    for i in range(amount):
        ctx.sendMessage(content)


def slowPrint(ctx):
    originalMessage = ctx.content[10:]
    print(originalMessage)
    currentMessage = ""
    for i in originalMessage:
        currentMessage += i
        ctx.editMessage(currentMessage)


def ascii(ctx):
    originalMessage = ctx.content[6:]
    originalMessage = originalMessage.replace(" ", "+")
    request = requests.get(
        "https://artii.herokuapp.com/make?text=" + originalMessage.upper())
    ctx.editMessage(f"```{request.text}```")


def binary(ctx):
    content = ctx.content.split(" ")
    content.pop(0)
    res = ""
    for word in content:
        for char in word:
            res += str(format(ord(char), '08b'))
            res += " "
        res += "\n"
    ctx.editMessage(res)


def tochar(ctx):
    content = ctx.content.split(" ")
    content.pop(0)
    res = ""
    for word in content:
        res += chr(int(word, 2))
    ctx.editMessage(res)


def addreactspam(ctx):
    global data
    content = ctx.content.split(" ")
    del content[0:2]  # remove command word and mention

    if not (len(ctx.mentions) > 0):
        return
    userId = ctx.mentions[0]['id']

    newKey = {userId: content}
    if not(os.path.exists("reactspam.json")):
        funcs.writeJson("reactspam.json", newKey)
    else:
        data = funcs.loadJson("reactspam.json")
        if not (userId in data['userid']):
            data['userid'][userId] = content
        else:
            data['userid'][userId] += content
        funcs.writeJson("reactspam.json", data)


def removereactspam(ctx):
    global data
    if not (len(ctx.mentions) > 0):
        return
    userId = ctx.mentions[0]['id']

    data = funcs.loadJson("reactspam.json")
    if(userId in data):
        del data['userid'][userId]
    funcs.writeJson("reactspam.json", data)


def clearreactspam():
    global data
    data = {'userid': {}, 'keyword': {}}
    funcs.writeJson("reactspam.json", data)


def addkeyspam(ctx):
    global data
    content = ctx.content.split(" ")
    content.pop(0)  # remove command word
    keyWord = content[0]
    theEmoji = content[1]

    newKey = {keyWord: theEmoji}
    if not(os.path.exists("reactspam.json")):
        funcs.writeJson("reactspam.json", newKey)
    else:
        data = funcs.loadJson("reactspam.json")
        if not (keyWord in data):
            data['keyword'][keyWord] = [theEmoji]
        else:
            data['keyword'][keyWord].append(theEmoji)
        funcs.writeJson("reactspam.json", data)


def removekeyspam(ctx):
    msg = ctx.content.split(" ")
    global data
    keyWord = msg[1]
    data = funcs.loadJson("reactspam.json")
    if(keyWord in data['keyword']):
        del data['keyword'][keyWord]
    funcs.writeJson("reactspam.json", data)


def addSpam(ctx):
    global gifs
    content = ctx.content.split(" ")
    content.pop(0)
    keyWord = content[0]
    gif = content[1]
    newKey = {keyWord: gif}
    if not(os.path.exists("giflist.json")):
        funcs.writeJson("giflist.json", newKey)
    else:
        gifFileContentJson = funcs.loadJson("giflist.json")
        gifFileContentJson[keyWord] = gif
        funcs.writeJson("giflist.json", gifFileContentJson)

    gifs = funcs.loadJson("giflist.json")


def remSpam(ctx):
    global gifs
    content = ctx.content.split(" ")
    content.pop(0)
    keyWord = content[0]
    gifFileContentJson = funcs.loadJson("giflist.json")

    if(keyWord in gifFileContentJson):
        del gifFileContentJson[keyWord]
    funcs.writeJson("giflist.json", gifFileContentJson)

    gifs = funcs.loadJson("giflist.json")


def antivirus(ctx):
    ctx.editMessage(
        "https://cdn.discordapp.com/attachments/862772809242509322/928032486880063499/796078795185717268-1.png")
    time.sleep(0.24)
    ctx.deleteMessage(priority=True)


def randreact(ctx):
    msg = ctx.content.split(" ")

    messageID = msg[1]

    all_emojis_key = list(emoji.EMOJI_UNICODE["en"].keys())
    decodation = []
    rand_emojis = []
    for i in range(0, len(all_emojis_key)):
        if("tone" not in all_emojis_key[i]):
            d = emoji.emojize(all_emojis_key[i])
            decodation.append(d)

    for i in range(10):
        rand_emojis.append(random.choice(decodation))

    num = 0
    while(num <= 10):
        try:
            resp = bot.addReaction(
                ctx.channel_id, messageID, random.choice(decodation))
            if(resp.status_code == 200):
                num += 1
            time.sleep(0.2)
        except Exception as ex:
            print(ex)


def statusCycleAdd(ctx):
    content = ctx.content.split(" ")
    content.pop(0)  # remove command word

    theEmoji = content[0]
    content.pop(0)

    text = ' '.join(content)

    newKey = {text: theEmoji}
    if not(os.path.exists("statuscycle.json")):
        funcs.writeJson("statuscycle.json", newKey)
    else:
        data = funcs.loadJson("statuscycle.json")
        if not (text in data):
            data[text] = theEmoji
        funcs.writeJson("statuscycle.json", data)


def statusCycleRemove(ctx):
    content = ctx.content.split(" ")
    num = int(content[1])

    statuses = funcs.loadJson("statuscycle.json")

    i = 0
    for status in list(statuses):
        if(i == num):
            statuses.pop(status)
            break
        i += 1

    funcs.writeJson("statuscycle.json", statuses)


def statusCycleClear(ctx):
    funcs.writeJson("statuscycle.json", {})


def statusCycleList(ctx):
    if not(os.path.exists("statuscycle.json")):
        return

    statuses = funcs.loadJson("statuscycle.json")
    text = "```\n"
    c = 0
    for i in statuses:
        text += f"{c}. {statuses[i]} {i}\n"
        c += 1
    text += "\n```"

    bot.sendMessage(ctx.channel_id, text)


def statusCycleStart(ctx):
    statusCycleThread.start()


def statusCycleStop(ctx):
    statuscycle.running = False
    statusCycleThread.join()
    print(">cyclethread stopped.")
