import os
import json
import requests
import funcs

gifs = {}
bot = None

print(">Loading Gifs...")
if not (os.path.isfile("giflist.json")):
    print(">Gif list does not exist. Creating...")
    with open("giflist.json", "w") as gifFile:
        gifDictionary = {
            "nigger": "https://media.discordapp.net/attachments/911923982821904427/924651985024720956/image0-16-1.gif"}
        json.dump(gifDictionary, gifFile)
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
        # discreply is what discord sends back after we send the messagee
        discreply = bot.sendMessage(
            ctx['channel_id'], content)

        funcs.preventRatelimit(discreply)


def slowPrint(ctx, msg):
    originalMessage = msg[10:]
    print(originalMessage)
    currentMessage = ""
    for i in originalMessage:
        currentMessage += i
        discreply = bot.editMessage(
            ctx['channel_id'], ctx['id'], currentMessage)
        funcs.preventRatelimit(discreply)


def ascii(ctx, msg):
    originalMessage = msg[6:]
    originalMessage = originalMessage.replace(" ", "+")
    request = requests.get(
        "https://artii.herokuapp.com/make?text=" + originalMessage.upper())
    bot.editMessage(ctx['channel_id'], ctx['id'], f"```{request.text}```")


def binary(ctx, msg):
    res = ""
    msg.pop(0)
    for word in msg:
        for char in word:
            res += str(format(ord(char), '08b'))
            res += " "
        res += "\n"
    bot.editMessage(ctx['channel_id'], ctx['id'], res)

def tochar(ctx, msg):
    res = ""
    msg.pop(0)
    for word in msg:
        res += chr(int(word, 2))
    bot.editMessage(ctx['channel_id'], ctx['id'], res)


