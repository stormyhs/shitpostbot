#!/usr/bin/python3
import discum
import time
import random
import sys

import configs as cfg
import funcs
import commands
import ctx as context

cpf = cfg.prefix

bot = discum.Client(
    token=cfg.token, log=False)

commands.bot = bot
funcs.bot = bot
context.bot = bot

commands.loadGifs()

def organicMessage(channel, msg):  # sends a message in a natural looking way
    bot.typingAction(channel)
    for word in msg:
        time.sleep(round(random.uniform(0, 0.2), 1))
    bot.sendMessage(channel, msg)


@bot.gateway.command
def engine(resp):
    if resp.event.ready_supplemental:  # ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(
            user['username'], user['discriminator']))


@bot.gateway.command
def on_message(resp):
    if not resp.event.message:
        return


    ctx = context.ctx(resp.parsed.auto())

    if(ctx.author['id'] != cfg.id):
        if(cfg.logger):
            funcs.logger(ctx)
        return

    if not ctx.content.startswith(cpf):
        return
    
    ctx.content = ctx.content[len(cpf):]
    command = ctx.content.split(" ")[0]

    if command == "spam":
        commands.messageSpam(ctx)

    elif command == "slowprint":
        commands.slowPrint(ctx)

    elif command == "ascii":
        commands.ascii(ctx)

    elif command == "binary":
        commands.binary(ctx)

    elif command == "tochar":
        commands.tochar(ctx)

while(True):
    print(">Connecting...")
    try:
        time.sleep(random.uniform(0.5, 2))
        bot.gateway.run(auto_reconnect=True)
    except KeyboardInterrupt:
        print(">Goodbye.")
        sys.exit(0)
