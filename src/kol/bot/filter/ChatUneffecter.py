from kol.Error import Error
from kol.manager import FilterManager
from kol.request.UneffectRequest import UneffectRequest
from kol.request.CharpaneRequest import CharpaneRequest
from kol.util import Report

def doFilter(eventName, context, **kwargs):
    bot = kwargs["bot"]
    charpaneRequest = CharpaneRequest(bot.session)
    response = charpaneRequest.doRequest()
    if len(response.get("effects", [])) > 0:
        for effect in response["effects"]:
            if effect["name"] == "B-b-brr!":
                uneffect(bot, 718)
            elif effect["name"] == "Bruised Jaw":
                uneffect(bot, 697)
        
    returnCode = FilterManager.FINISHED
    return returnCode

def uneffect(bot, id):
    r = UneffectRequest(bot.session, id)
    try:
        r.doRequest()
        resp = "Effect successfully removed!"
    except Error:
        resp = "Unable to remove effect for unknown reason."
    
    Report.info("bot", resp)    