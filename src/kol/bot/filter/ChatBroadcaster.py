# $Id: ChatBroadcaster.py 116 2009-12-09 14:43:26Z scelis $

"""
This module implements a FilterManager filter to allow bots to broadcast their /clan chat
to other bots being run in this process. Users may prefix their chats with 'PRIVATE:' to
tell the bot to not broadcast that particular message. In addition, users with sufficient
privileges may tell the bot to stop or start broadcasting at any time by sending a private
message with the text 'squelch' or 'unsquelch'. Finally, players may also send a private
message with the text 'who' to see which players are in the same channel as the bot.
"""

from kol.bot import BotManager
from kol.bot import BotUtils
from kol.manager import FilterManager
from kol.util import DataUtils
from kol.util import Report
from kol.database import HogDatabase

def doFilter(eventName, context, **kwargs):
    returnCode = FilterManager.CONTINUE
    if eventName == "botProcessChat":
        returnCode = botProcessChat(context, **kwargs)
    elif eventName == "botPostLogin":
        returnCode = botPostLogin(context, **kwargs)
    return returnCode

def botProcessChat(context, **kwargs):
    returnCode = FilterManager.CONTINUE
    chat = kwargs["chat"]
    
    if chat["type"] in ["normal", "emote"] and chat["channel"] == "clan":
        returnCode = handleClanChat(context, **kwargs)
    elif chat["type"] in ["private"]:
        returnCode = handlePrivateChat(context, **kwargs)
    elif chat["type"] in ["logonNotification"] and DataUtils.getBoolean(kwargs["bot"].params, "doWork:doRosterAnnouncements", False):
        returnCode = handleLogonNotification(context, **kwargs)
    elif chat["type"] in ["logoffNotification"] and DataUtils.getBoolean(kwargs["bot"].params, "doWork:doRosterAnnouncements", False):
        returnCode = handleLogoffNotification(context, **kwargs)
    return returnCode

def handleLogonNotification(context, **kwargs):
    returnCode = FilterManager.CONTINUE
    chat = kwargs["chat"]
    bot = kwargs["bot"]
    globalState = bot.states["global"]        
    bot.sendChatMessage(HogDatabase.getEnterMessage(chat["userId"], chat["userName"]))
    if HogDatabase.getAutolog(chat["userId"]) == 1:        
        sendLatestLog(bot, chat["userId"], bot.params["userClan"])
    return returnCode

def handleLogoffNotification(context, **kwargs):
    returnCode = FilterManager.CONTINUE
    chat = kwargs["chat"]
    bot = kwargs["bot"]
    globalState = bot.states["global"]
    bot.sendChatMessage(HogDatabase.getExitMessage(chat["userId"], chat["userName"]))    
    return returnCode

def handleClanChat(context, **kwargs):
    chat = kwargs["chat"]
    bot = kwargs["bot"]
    globalState = bot.states["global"]
    
    # Do nothing if the text is prefixed by PRIVATE:
    lowerText = chat["text"].lower()
    if lowerText.find("private:") == 0 or lowerText[0:2] == "p:":
        return FilterManager.CONTINUE
    
    if DataUtils.getBoolean(kwargs["bot"].params, "doWork:doLogChat", False):
        HogDatabase.logChat(chat["userId"], chat["userName"], bot.params["userClan"], chat["text"])
    
    #Do nothing if the bot is squelched.
    if DataUtils.getBoolean(globalState, "isSquelched", False):
        return FilterManager.CONTINUE
    
    # Do nothing for broadcasted messages.
    if chat["userName"] == "System Message":
        return FilterManager.CONTINUE
    
    # Construct the message to send to the other bots.
    msg = None
    if "chatBroadcastDelimiters" in bot.params:
        chars = bot.params["chatBroadcastDelimiters"]
        if chat["type"] == "normal":
            msg = "%s%s%s %s" % (chars[0], chat["userName"], chars[1], chat["text"])
        elif chat["type"] == "emote":
            msg = "/me %s%s%s %s" % (chars[0], chat["userName"], chars[1], chat["text"])
    else:
        if chat["type"] == "normal":
            msg = "[%s] %s" % (chat["userName"], chat["text"])
        elif chat["type"] == "emote":
            msg = "/me [%s] %s" % (chat["userName"], chat["text"])
    
    # Send the message to the other bots.
    if msg != None:
        thisBot = kwargs["bot"]
        for bot in BotManager._bots:
            if bot.id != thisBot.id:
                if bot.session != None and bot.session.isConnected and hasattr(bot.session, "chatManager"):
                    try:
                        bot.sendChatMessage(msg)
                    except AttributeError, inst:
                        Report.error("chat", "Could not broadcast message.", inst)
    
    return FilterManager.CONTINUE

def handlePrivateChat(context, **kwargs):
    returnCode = FilterManager.CONTINUE
    chat = kwargs["chat"]
    bot = kwargs["bot"]
    globalState = bot.states["global"]
    
    arr = chat["text"].split()
    
    if chat["text"] == "squelch":
        if BotUtils.canUserPerformAction(chat["userId"], "squelch", bot):
            globalState["isSquelched"] = True
            bot.writeState("global")
            bot.sendChatMessage("No longer broadcasting /clan to the other clan channels.")
        else:
            bot.sendChatMessage("/w %s You do not have permission to perform this action." % chat["userId"])
        returnCode = FilterManager.FINISHED
    elif chat["text"] == "unsquelch":
        if BotUtils.canUserPerformAction(chat["userId"], "squelch", bot):
            globalState["isSquelched"] = False
            bot.writeState("global")
            bot.sendChatMessage("Now broadcasting /clan to the other clan channels.")
        else:
            bot.sendChatMessage("/w %s You do not have permission to perform this action." % chat["userId"])
        returnCode = FilterManager.FINISHED
    elif chat["text"] == "muteall":
        if BotUtils.canUserPerformAction(chat["userId"], "muteall", bot):
            for aBot in BotManager._bots:
                aBot.states["global"]["isSquelched"] = True
                aBot.writeState("global")
                aBot.sendChatMessage("All bots have been muted.")
        else:
            bot.sendChatMessage("/w %s You do not have permission to perform this action." % chat["userId"])
        returnCode = FilterManager.FINISHED
    elif chat["text"] == "unmuteall":
        if BotUtils.canUserPerformAction(chat["userId"], "muteall", bot):
            for aBot in BotManager._bots:
                aBot.states["global"]["isSquelched"] = False
                aBot.writeState("global")
                aBot.sendChatMessage("All bots have been unmuted.")
        else:
            bot.sendChatMessage("/w %s You do not have permission to perform this action." % chat["userId"])
        returnCode = FilterManager.FINISHED
    elif chat["text"] == "who":
        response = bot.sendChatMessage("/who")
        whoChat = response[0]
        str = ""
        for user in whoChat["users"]:
            if user["userName"] != bot.id:
                if len(str) > 0:
                    str += ", "
                str += user["userName"]
        if len(str) > 0:
            bot.sendChatMessage("/w %s %s" % (chat["userId"], str))
        else:
            bot.sendChatMessage("/w %s There is no one else in my clan channel." % chat["userId"])
        returnCode = FilterManager.FINISHED    
    elif chat["text"] == "help":
        m = {}
        m["userId"] = chat["userId"]
        m["text"] = generateHelpText(bot.params["userName"]) 
        bot.sendKmail(m)
        returnCode = FilterManager.FINISHED
    elif chat["text"] == "mymsgs":
        m = {}
        m["userId"] = chat["userId"]
        message = "Enter Message: " + HogDatabase.getEnterMessage(chat["userId"], chat["userName"]) + "\n" + "Exit Message: " + HogDatabase.getExitMessage(chat["userId"], chat["userName"])        
        m["text"] = message
        bot.sendKmail(m)
        returnCode = FilterManager.FINISHED
    elif chat["text"] == "autolog":
        toggle = HogDatabase.toggleAutolog(chat["userId"], chat["userName"])
        if toggle == 1:            
            bot.sendChatMessage("/w %s autolog enabled." % (chat["userId"]))
        else:            
            bot.sendChatMessage("/w %s autolog disabled." % (chat["userId"]))    
        returnCode = FilterManager.FINISHED
    elif chat["text"] == "log":
        sendLatestLog(bot, chat["userId"], bot.params["userClan"])
        returnCode = FilterManager.FINISHED
                
    if len(arr) > 0 and arr[0] == "entermsg":
        enterMsg = chat["text"].replace('entermsg ', '', 1)
        HogDatabase.setEnterMessage(chat["userId"], chat["userName"], enterMsg)
        bot.sendChatMessage("/w %s Enter message changed to: %s" % (chat["userId"], enterMsg))
        returnCode = FilterManager.FINISHED
    elif len(arr) > 0 and arr[0] == "exitmsg":    
        exitMsg = chat["text"].replace('exitmsg ', '', 1)
        HogDatabase.setExitMessage(chat["userId"], chat["userName"], exitMsg)
        bot.sendChatMessage("/w %s Exit message changed to: %s" % (chat["userId"], exitMsg))
        returnCode = FilterManager.FINISHED        
    elif len(arr) > 0 and arr[0] == "seen":    
        user = chat["text"].replace('seen ', '', 1)
        lastSeen = HogDatabase.getLastSeen(user)
        if lastSeen == None or lastSeen[0] == None:
            bot.sendChatMessage("/w %s %s hasn't been seen by the bot" % (chat["userId"], user))
        else:            
            bot.sendChatMessage("/w %s %s last seen on %s" % (chat["userId"], user, lastSeen[0]))
        returnCode = FilterManager.FINISHED    
    
    return returnCode

def botPostLogin(context, **kwargs):
    bot = kwargs["bot"]
    bot.sendChatMessage("/channel clan")
    return FilterManager.CONTINUE

def generateHelpText(userName):
    returnText = "Send me a command: \n\n"
    returnText += "/w " + userName + " entermsg Thing to say when you log on\n"
    returnText += "/w " + userName + " exitmsg Thing to say when you log off\n"
    returnText += "/w " + userName + " mymsgs - find out what (if any) you custom enter/exit messages are\n"
    returnText += "/w " + userName + " log - get a list of recent messages in /clan\n"
    returnText += "/w " + userName + " autolog - Toggle whether or not the bot kmails you a /clan log when you sign on\n"
    returnText += "/w " + userName + " seen username - find out when username last spoke in /clan\n"

    return returnText

def sendLatestLog(bot, userId, clanName):
    m = {}
    m["userId"] = userId
    logs =  HogDatabase.getLatestLog(clanName)
    message = ""
    for log in logs:
        message += log[2] + ": " + log[3] + "\n"
    m["text"] = message
    bot.sendKmail(m)
