#!/usr/bin/python3
import discum
import time
import random
import sys

import configs

cfg = configs.config  # fuck you i dont care

bot = discum.Client(
    token=cfg.token, log=False)


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

    if resp.event.message:
        m = resp.parsed.auto()
        if(m['author']['id'] == cfg.id):
            print(m['content'])


while(True):
    print(">Connecting...")
    try:
        time.sleep(random.uniform(0.5, 2))
        bot.gateway.run(auto_reconnect=True)
    except KeyboardInterrupt:
        print(">Goodbye.")
        sys.exit(0)
