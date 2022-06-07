#!/usr/bin/python3
import discum, time, random, sys

import configs
import funcs
import commands
import ctx as context
import statuscycle

bot = discum.Client(token=configs.token, log=False)

#TODO: ?
context.bot = bot
statuscycle.bot = bot

funcs.loadData()

@bot.gateway.command
def engine(resp):
    if resp.event.ready_supplemental:  # ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(
            user['username'], user['discriminator']))
        configs.user_id = user['id']

@bot.gateway.command
def on_message(resp):
    if not resp.event.message:
        return

    ctx = context.ctx(resp.parsed.auto())

    if(ctx.author.id != configs.user_id):
        if(configs.logger):
            funcs.logger(ctx, bot)
        funcs.handleReactSpam(ctx)
        return

    if not ctx.content.startswith(configs.prefix):
        return

    ctx.content = ctx.content[len(configs.prefix):]
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

    elif command == "adduserreact":
        ctx.deleteMessage(priority=True)
        commands.addreactspam(ctx)
    elif command == "removeuserreact" or command == "remuserreact" or command == "rmuserreact":
        ctx.deleteMessage(priority=True)
        commands.removereactspam(ctx)
    elif command == "clearuserreact":
        ctx.deleteMessage(priority=True)
        commands.clearreactspam(ctx)
    elif command == "randreact":
        ctx.deleteMessage(priority=True)
        commands.randreact(ctx, bot)

    elif command == "addwordspam":
        ctx.deleteMessage(priority=True)
        commands.addkeyspam(ctx)
    elif command == "removewordspam" or command == "remwordspam" or command == "rmwordspam":
        ctx.deleteMessage(priority=True)
        commands.removekeyspam(ctx)
    elif command == "clearwordspam":
        ctx.deleteMessage(priority=True)
        commands.clearkeyspam(ctx)

    elif command == "slowprint":
        commands.slowPrint(ctx)
    elif command == "ascii":
        commands.ascii(ctx)
    elif command == "binary":
        commands.binary(ctx)
    elif command == "tochar":
        commands.tochar(ctx)

    elif command == "statuscyclelist":
        commands.statusCycleList(ctx, bot)
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
