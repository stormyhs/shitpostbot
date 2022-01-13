#!/usr/bin/python3
import discum
import time
import random
import sys

import configs as cfg
import funcs
import commands
import ctx as context
import statuscycle

cpf = cfg.prefix

bot = discum.Client(
    token=cfg.token, log=False)
userID = ""

commands.bot = bot
funcs.bot = bot
context.bot = bot
statuscycle.bot = bot

funcs.loadData()


@bot.gateway.command
def engine(resp):
    global userID
    if resp.event.ready_supplemental:  # ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(
            user['username'], user['discriminator']))
        userID = user['id']


@bot.gateway.command
def on_message(resp):
    if not resp.event.message:
        return

    ctx = context.ctx(resp.parsed.auto())

    if(ctx.author.id != userID):
        if(cfg.logger):
            funcs.logger(ctx)
        funcs.handleReactSpam(ctx)
        return

    if not ctx.content.startswith(cpf):
        return

    ctx.content = ctx.content[len(cpf):]
    command = ctx.content.split(" ")[0]

    if command == "spam":
        ctx.deleteMessage(priority=True)
        commands.messageSpam(ctx)
    elif command == "addspam":
        ctx.deleteMessage(priority=True)
        commands.addSpam(ctx)
    elif command == "removespam" or command == "remspam" or command == "rmspam":
        ctx.deleteMessage(priority=True)
        commands.remSpam(ctx)

    elif command == "addreactspam":
        ctx.deleteMessage(priority=True)
        commands.addreactspam(ctx)
    elif command == "removereactspam" or command == "remreactspam" or command == "rmreactspam":
        ctx.deleteMessage(priority=True)
        commands.removereactspam(ctx)
    elif command == "clearreactspam":
        ctx.deleteMessage(priority=True)
        commands.clearreactspam()
    elif command == "randreact":
        ctx.deleteMessage(priority=True)
        commands.randreact(ctx)

    elif command == "slowprint":
        commands.slowPrint(ctx)
    elif command == "ascii":
        commands.ascii(ctx)
    elif command == "binary":
        commands.binary(ctx)
    elif command == "tochar":
        commands.tochar(ctx)

    elif command == "statuscyclelist":
        commands.statusCycleList(ctx)
        ctx.deleteMessage(priority=True)
    elif command == "statuscycleadd":
        commands.statusCycleAdd(ctx)
        ctx.deleteMessage(priority=True)
    elif command == "statuscycleremove":
        commands.statusCycleRemove(ctx)
        ctx.deleteMessage(priority=True)
    elif command == "statuscycleclear":
        commands.statusCycleClear(ctx)
        ctx.deleteMessage(priority=True)
    elif command == "statuscyclestart":
        commands.statusCycleStart(ctx)
        ctx.deleteMessage(priority=True)
    elif command == "statuscyclestop":
        commands.statusCycleStop(ctx)
        ctx.deleteMessage(priority=True)


while(True):
    print(">Connecting...")
    try:
        time.sleep(random.uniform(0.5, 2))
        bot.gateway.run(auto_reconnect=True)
    except KeyboardInterrupt:
        print(">Goodbye.")
        sys.exit(0)
