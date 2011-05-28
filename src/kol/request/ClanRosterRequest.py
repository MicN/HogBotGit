from GenericRequest import GenericRequest
from kol.manager import PatternManager

class ClanRosterRequest(GenericRequest):
    
    def __init__(self, session):
        super(ClanRosterRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_whitelist.php'
        
    def parseResponse(self):
        members = []
        whitelistMemberPattern = PatternManager.getOrCompilePattern('whitelistMember')
        reponse = self.responseText        
        snippedResponse = reponse[0:reponse.find("People Not In Your Clan")]
        for match in whitelistMemberPattern.finditer(snippedResponse):
            member = {}
            member["id"] = match.group(1)
            member["name"] = match.group(2)
            member["rank"] = match.group(3)
            members.append(member)
        if len(members) > 0:
            self.responseData["members"] = members