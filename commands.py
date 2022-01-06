import os
import json
import requests
import emoji
import funcs

gifs = {}
bot = None
data = []


def loadReactions():
    global data
    print(">Loading Reacts...")
    if not (os.path.isfile("reactspam.json")):
        print(">Reacts list does not exist. Creating...")
        with open("reactspam.json", "w") as f:
            f.write("{}")
    else:
        with open("reactspam.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())


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


def addreactspam(ctx, msg):
    global data
    msg.pop(0)  # remove command word
    id = ""
    theEmoji = ""
    for word in list(msg):
        if(word[0:3] == "<@!" and word[len(word)-1] == ">"):
            id = word[3:len(word)-1]
            msg.remove(word)

    # TODO: unless the retarded user gave more than 3 arguments
    theEmoji = msg[0]

    newKey = {id: theEmoji}
    if not(os.path.exists("reactspam.json")):
        with open("reactspam.json", "w", encoding="utf-8") as f:
            json.dump(newKey, f, indent=4, ensure_ascii=False)
    else:
        with open("reactspam.json", "r+", encoding="utf-8") as f:
            data = json.loads(f.read())
            data[id] = theEmoji
            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4, ensure_ascii=False)


def removereactspam(ctx, msg):
    global data
    id = msg[1]
    id = id[3:len(id)-1]
    try:
        with open("reactspam.json", "r+", encoding="utf-8") as f:
            data = json.loads(f.read())
            if(id in data):
                del data[id]
            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        return


def clearreactspam(ctx, msg):
    global data
    data = {}
    try:
        with open("reactspam.json", "r+", encoding="utf-8") as f:
            f.seek(0)
            f.truncate(0)
            f.write("{}")
    except Exception as e:
        return
