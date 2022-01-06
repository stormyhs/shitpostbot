import os
import json
import requests

gifs = {}
bot = None

def loadGifs():
    global gifs
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


def messageSpam(ctx, msg):
    try:
        amount = int(msg[0])
    except:
        amount = 5
    if not msg[1] in gifs:
        return

    content = gifs[msg[1]]
    for i in range(amount):
        ctx.sendMessage(content)

def slowPrint(ctx, msg):
    originalMessage = msg[10:]
    print(originalMessage)
    currentMessage = ""
    for i in originalMessage:
        currentMessage += i
        ctx.editMessage(currentMessage)


def ascii(ctx, msg):
    originalMessage = msg[6:]
    originalMessage = originalMessage.replace(" ", "+")
    request = requests.get(
        "https://artii.herokuapp.com/make?text=" + originalMessage.upper())
    ctx.editMessage(f"```{request.text}```")


def binary(ctx, msg):
    res = ""
    msg.pop(0)
    for word in msg:
        for char in word:
            res += str(format(ord(char), '08b'))
            res += " "
        res += "\n"
    ctx.editMessage(res)

def tochar(ctx, msg):
    res = ""
    msg.pop(0)
    for word in msg:
        res += chr(int(word, 2))
    ctx.editMessage(res)


