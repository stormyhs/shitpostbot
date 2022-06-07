import threading, time
import funcs

bot = None
working = False

class SendMessageTask:
    def execute(self):
        discreply = bot.sendMessage(self.channel, self.content)
        funcs.preventRatelimit(discreply)
        time.sleep(0.4)

    def __init__(self, channel, content):
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
            time.sleep(0.4)
            
    def addTask(self, task, priority):
        if(priority):
            self.tasks.insert(0, task)
            return

        self.tasks.append(task)

    def __init__(self):
        threading.Thread(target = self.handler).start()

handler = Taskhandler()

class ctxSubclass:
    def __init__(self, ctxDict):
        for key in ctxDict:
            setattr(self, key, ctxDict[key])

class ctx:
    def __init__(self, ctxDict):
        for key in ctxDict:
            if(key == "author" or key == "message_reference"):
                setattr(self, key, ctxSubclass(ctxDict[key]))
                continue

            setattr(self, key, ctxDict[key])

    def sendMessage(self, content, priority = False):
        handler.addTask(SendMessageTask(self.channel_id, content), priority)

    def editMessage(self, content, priority = False):
        handler.addTask(EditMessageTask(self.channel_id, self.id, content), priority)
    
    def addReaction(self, content, priority = False):
        handler.addTask(AddReactionTask(self.channel_id, self.id, content), priority)

    def deleteMessage(self, priority = False):
        handler.addTask(DeleteMessageTask(self.channel_id, self.id), priority)
