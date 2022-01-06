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
commands.loadReactions()


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
        funcs.handleReactSpam(ctx)
        return

    if not ctx.content.startswith(cpf):
        return

    msg = ctx.content.split(" ")
    msg[0] = msg[0][1:]

    if msg[0] == "spam":
        ctx.deleteMessage()
        commands.messageSpam(ctx, msg)

    elif msg[0] == "slowprint":
        commands.slowPrint(ctx, ctx.content)

    elif msg[0] == "ascii":
        commands.ascii(ctx, ctx.content)

    elif msg[0] == "binary":
        commands.binary(ctx, msg)

    elif msg[0] == "tochar":
        commands.tochar(ctx, msg)

    elif msg[0] == "addreactspam":
        commands.addreactspam(ctx, msg)
    elif msg[0] == "removereactspam" or msg[0] == "remreactspam" or msg[0] == "rmreactspam":
        commands.removereactspam(ctx, msg)
    elif msg[0] == "clearreactspam":
        commands.clearreactspam(ctx, msg)


while(True):
    print(">Connecting...")
    try:
        time.sleep(random.uniform(0.5, 2))
        bot.gateway.run(auto_reconnect=True)
    except KeyboardInterrupt:
        print(">Goodbye.")
        sys.exit(0)
