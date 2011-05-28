from GenericRequest import GenericRequest
from kol.manager import PatternManager

class ShowPlayerRequest(GenericRequest):
    
    def __init__(self, session, playerId):
        super(ShowPlayerRequest, self).__init__(session)
        self.url = session.serverURL + "showplayer.php?who=%s" % playerId
        
    def parseResponse(self):
        playerNamePattern = PatternManager.getOrCompilePattern('profileUserName')
        match = playerNamePattern.search(self.responseText)
        if match:
            self.responseData["playerName"] = match.group(1)        
                
        playerClanPattern = PatternManager.getOrCompilePattern('playerClan')
        match = playerClanPattern.search(self.responseText)
        if match:
            self.responseData["playerClan"] = match.group(2)
        else:
            self.responseData["playerClan"] = ""
            
        numberAscensionsPattern = PatternManager.getOrCompilePattern('numberAscensions')
        match = numberAscensionsPattern.search(self.responseText)
        if match:
            self.responseData["numberAscensions"] = int(match.group(1))
        else:
            self.responseData["numberAscensions"] = 0
            
        numberTrophiesPattern = PatternManager.getOrCompilePattern('numberTrophies')
        match = numberTrophiesPattern.search(self.responseText)
        if match:
            self.responseData["numberTrophies"] = int(match.group(1))
        else:
            self.responseData["numberTrophies"] = 0                    

        numberTattoosPattern = PatternManager.getOrCompilePattern('numberTattoos')
        match = numberTattoosPattern.search(self.responseText)
        if match:
            self.responseData["numberTattoos"] = int(match.group(1))
        else:
            self.responseData["numberTattoos"] = 0                           