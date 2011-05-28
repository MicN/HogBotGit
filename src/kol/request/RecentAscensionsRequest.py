import re
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import Report

from datetime import datetime

class RecentAscensionsRequest(GenericRequest):
	def __init__(self, session, boardId):
		super(RecentAscensionsRequest, self).__init__(session)
		self.url = session.serverURL + "museum.php?floor=1&place=leaderboards&whichboard=%s" % boardId
		self.boardId = boardId

	def parseResponse(self):
		txt = self.responseText
		stripText = txt.replace("&nbsp;", "")
		
		index = stripText.find('(updated live):')
		if index > 0:
			stripText = stripText[index:]
		
		ascensions = []
		recentAscensionPattern = PatternManager.getOrCompilePattern('recentAscension')
		for match in recentAscensionPattern.finditer(stripText):
			m = {}
			m["userId"] = int(match.group(1))
			m["userName"] = match.group(2)
			m["level"] = match.group(3)
			m["class"] = match.group(4)
			m["path"] = match.group(5)
			if self.boardId == 1:
				m["type"] = "Softcore"
			else:
				m["type"] = "Hardcore"
			ascensions.append(m)
		self.responseData["ascensions"] = ascensions
	