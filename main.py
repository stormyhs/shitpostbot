#!/usr/bin/python3
import discum
import time
import random
import sys
import json
import configs as cfg

bot = discum.Client(
    token=cfg.token, log=False)


def organicMessage(channel, msg):  # sends a message in a natural looking way
    bot.typingAction(channel)
    for word in msg:
        time.sleep(round(random.uniform(0, 0.2), 1))
    bot.sendMessage(channel, msg)

def spamGif(ctx, gif, amount):
    for i in range(amount):
    # discreply is what discord sends back after we send the messagee
    discreply = bot.sendMessage(
    m['channel_id'], "https://media.discordapp.net/attachments/911923982821904427/924651985024720956/image0-16-1.gif")
    if "retry_after" in discreply.text:
        jdata = json.loads(discreply.text)
            print(f">{jdata['retry_after']} TIMEOUT")
            # wait as long as discord said + 0.5 so we dont get fucked for botting
            time.sleep(jdata['retry_after'] + 0.5)
                    time.sleep(0.1)


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

    m = resp.parsed.auto()
    if(m['author']['id'] != cfg.id):
        return

    if(m['content'].startswith(">nigger")):
        msg = m['content'].split(" ")
        try:
            amount = int(msg[1])
        except:
            amount = 5
               


while(True):
    print(">Connecting...")
    try:
        time.sleep(random.uniform(0.5, 2))
        bot.gateway.run(auto_reconnect=True)
    except KeyboardInterrupt:
        print(">Goodbye.")
        sys.exit(0)
