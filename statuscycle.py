import time
import funcs
import configs

running = True
bot = None


def cycle():
    print(">cyclethread started.")
    currentStatus = 0
    while(running):
        # Absolutely horrendous way of letting the thread check if it should keep running.
        # Unfortunately, I don't care.
        # TODO: wtf
        waited = 0
        while(waited < configs.statusCycleTimer):
            time.sleep(1)
            waited += 1

        statuses = funcs.loadJson("statuscycle.json")
        done = False

        if(currentStatus == len(list(statuses)) - 1):
            bot.gateway.setCustomStatus(
                list(statuses)[0], statuses[list(statuses)[0]])
            currentStatus = 0
            done = True
        else:
            for i in range(len(list(statuses))):
                if(i == currentStatus):
                    bot.gateway.setCustomStatus(
                        list(statuses)[i+1], statuses[list(statuses)[i+1]])
                    currentStatus += 1
                    done = True
                    break

        if not(done):
            bot.gateway.setCustomStatus(
                list(statuses)[0], statuses[list(statuses)[0]])
            currentStatus = 0
