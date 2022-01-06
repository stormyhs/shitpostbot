import os
import json
import requests
import funcs

gifs = {}
bot = None
data = {}


def loadReactions():
    global data
    print(">Loading Reacts...")
    if not (os.path.isfile("reactspam.json")):
        print(">Reacts list does not exist. Creating...")
        funcs.writeJson("reactspam.json", data)
    else:
        data = funcs.loadJson("reactspam.json")


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
    content.pop(0)  # remove command word
    id = ""
    theEmoji = ""
    for word in list(content):
        if(word[0:3] == "<@!" and word[len(word)-1] == ">"):
            id = word[3:len(word)-1]
            content.remove(word)

    # TODO: unless the retarded user gave more than 3 arguments
    theEmoji = content[0]

    newKey = {id: theEmoji}
    if not(os.path.exists("reactspam.json")):
        funcs.writeJson("reactspam.json", newKey)
    else:
        data = funcs.loadJson("reactspam.json")
        if not (id in data):
            data[id] = [theEmoji]
        else:
            data[id].append(theEmoji)
        funcs.writeJson("reactspam.json", data)


def removereactspam(ctx):
    msg = ctx.content.split(" ")
    global data
    id = msg[1]
    id = id[3:len(id)-1]
    data = funcs.loadJson("reactspam.json")
    if(id in data):
        del data[id]
    funcs.writeJson("reactspam.json", data)


def clearreactspam():
    global data
    data = {}
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
            data[keyWord] = [theEmoji]
        else:
            data[keyWord].append(theEmoji)
        funcs.writeJson("reactspam.json", data)


def removekeyspam(ctx):
    msg = ctx.content.split(" ")
    global data
    keyWord = msg[1]
    data = funcs.loadJson("reactspam.json")
    if(keyWord in data):
        del data[keyWord]
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
        print(gifFileContentJson)
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
