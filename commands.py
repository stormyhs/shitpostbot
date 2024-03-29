import os, pyfiglet, funcs, time, emoji, random, threading, statuscycle

data = {'userid': {}, 'keyword': {}}
statusCycleThread = threading.Thread(target=statuscycle.cycle)

def messageSpam(ctx):
    gifsData = funcs.loadJson("giflist.json")
    content = ctx.content[5:]
    content = content.split(" ")
    try:
        amount = int(content[1])
    except:
        amount = 5
    if not content[0] in gifsData:
        content = content[0]
    else:
        content = gifsData[content[0]]

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
    art = pyfiglet.figlet_format(originalMessage)
    ctx.editMessage(f"```\n{art}\n```")

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
    reactSpamData = funcs.loadJson("reactspam.json")
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
        if not (userId in reactSpamData):
            data[userId] = content
        else:
            data[userId] += content
        funcs.writeJson("reactspam.json", data)

def removereactspam(ctx):
    reactSpamData = funcs.loadJson("reactspam.json")

    if not (len(ctx.mentions) > 0):
        return

    userId = ctx.mentions[0]['id']

    if(userId in reactSpamData):
        del reactSpamData[userId]

    funcs.writeJson("reactspam.json", reactSpamData)

def clearreactspam(ctx):
    funcs.writeJson("reactspam.json", {})

def addkeyspam(ctx):
    wordReactSpamData = funcs.loadJson("wordreactspam.json")
    content = ctx.content.split(" ")
    content.pop(0)  # remove command word
    keyWord = content[0]
    theEmoji = content[1]

    if not (keyWord in wordReactSpamData):
        wordReactSpamData[keyWord] = [theEmoji]
    else:
        wordReactSpamData[keyWord].append(theEmoji)

    funcs.writeJson("wordreactspam.json", wordReactSpamData)

def removekeyspam(ctx):
    wordReactSpamData = funcs.loadJson("wordreactspam.json")
    msg = ctx.content.split(" ")
    keyWord = msg[1]

    if(keyWord in wordReactSpamData):
        del wordReactSpamData[keyWord]

    funcs.writeJson("wordreactspam.json", {})

def clearkeyspam(ctx):
    funcs.writeJson("wordreactspam.json", {})

def addSpam(ctx):
    gifsData = funcs.loadJson("giflist.json")
    content = ctx.content.split(" ")
    content.pop(0)
    keyWord = content[0]
    gif = content[1]

    gifsData = funcs.loadJson("giflist.json")
    gifsData[keyWord] = gif
    funcs.writeJson("giflist.json", gifsData)

def remSpam(ctx):
    gifsData = funcs.loadJson("giflist.json")
    content = ctx.content.split(" ")
    content.pop(0)
    keyWord = content[0]

    if(keyWord in gifsData):
        del gifsData[keyWord]

    funcs.writeJson("giflist.json", gifsData)

def randreact(ctx, bot):
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
            if(resp.status_code == 204):
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

def statusCycleList(ctx, bot):
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
