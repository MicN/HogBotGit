from GenericRequest import GenericRequest
from kol.manager import PatternManager

class ClanWhitelistRequest(GenericRequest):
	
	def __init__(self, session):
		super(ClanWhitelistRequest, self).__init__(session)
		self.url = session.serverURL + 'clan_whitelist.php'
		
	def parseResponse(self):
		members = []
		whitelistMemberPattern = PatternManager.getOrCompilePattern('whitelistMember')
		for match in whitelistMemberPattern.finditer(self.responseText):
			member = {}
			member["id"] = match.group(1)
			member["name"] = match.group(2)
			member["rank"] = match.group(3)
			members.append(member)
		if len(members) > 0:
			self.responseData["members"] = members