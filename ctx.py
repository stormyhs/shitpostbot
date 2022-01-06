import threading, time


import funcs

bot = None
working = False

class SendMessageTask:
    def execute(self):
        print("sending message in guild " + self.guild + " in channel " + self.channel + " with content " + self.content)
        discreply = bot.sendMessage(self.channel, self.content)
        funcs.preventRatelimit(discreply)

    def __init__(self, guild, channel, content):
        self.guild = guild
        self.channel = channel
        self.content = content

class EditMessageTask:
    def execute(self):  
        discreply = bot.editMessage(self.channel, self.messageId, self.content)
        funcs.preventRatelimit(discreply)

    def __init__(self, channel, messageId, content):
        self.channel = channel
        self.messageId = messageId
        self.content = content

class AddReactionTask(EditMessageTask):
    def execute(self):  
        discreply = bot.addReaction(self.channel, self.messageId, self.content)
        funcs.preventRatelimit(discreply)

class DeleteMessageTask:
    def execute(self):
        discreply = bot.deleteMessage(self.channel, self.messageId)
        funcs.preventRatelimit(discreply)

    def __init__(self, channel, messageId):
        self.channel = channel
        self.messageId = messageId



class Taskhandler:    

    tasks = [] 
    def handler(self):
        while True:
            if(len(self.tasks) > 0):
                task = self.tasks.pop(0)
                task.execute()
            else:
                time.sleep(0.1)

    def addTask(self, task, priority):
        if(priority):
            self.tasks.insert(0, task)
            return

        self.tasks.append(task)

    def __init__(self):
        threading.Thread(target = self.handler).start()

handler = Taskhandler()

class ctx:
    
    def __init__(self, ctxDict):
        for key in ctxDict:
            setattr(self, key, ctxDict[key])

    def sendMessage(self, content, priority = False):
        print("added task")
        handler.addTask(SendMessageTask(self.guild_id, self.channel_id, content), priority)

    def editMessage(self, content, priority = False):
        handler.addTask(EditMessageTask(self.channel_id, self.id, content), priority)
    
    def addReaction(self, content, priority = False):
        handler.addTask(AddReactionTask(self.channel_id, self.id, content), priority)

    def deleteMessage(self, priority = False):
        handler.addTask(DeleteMessageTask(self.channel_id, self.id), priority)
