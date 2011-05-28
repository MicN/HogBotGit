import re
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import Report

from datetime import datetime

STASH_PATTERN = re.compile(r'<b>Stash Activity:<\/b><\/center><table><tr><td><font size="?\d+"?>(?P<rows>.*?)<\/font><\/td><\/tr><\/table><\/center>')
STASH_ROW_ITEM_PATTERN = re.compile(r'(?P<month>\d{2})\/(?P<day>\d{2})\/(?P<year>\d{2}), (?P<hour>\d{2}):(?P<minute>\d{2})(?P<ampm>AM|PM): <a .*?>(?P<userName>[\w ]+) \(#(?P<userId>\d+)\)<\/a> (?P<direction>took|added) (?P<quantity>\d+) (?P<item>.+).')
STASH_ROW_MEAT_PATTERN = re.compile(r'(?P<month>\d{2})\/(?P<day>\d{2})\/(?P<year>\d{2}), (?P<hour>\d{2}):(?P<minute>\d{2})(?P<ampm>AM|PM): <a .*?>(?P<userName>[\w ]+) \(#(?P<userId>\d+)\)<\/a> contributed (?P<quantity>\d+) meat.')

class ClanStashLogRequest(GenericRequest):
	def __init__(self, session):
		super(ClanStashLogRequest, self).__init__(session)
		self.url = session.serverURL + "clan_log.php"

	def parseResponse(self):
		data = self.parseGeneral(self.responseText)
		if data: self.responseData["general"] = data
		data = self.parseStashActivity(self.responseText)
		if data: self.responseData["stashActivity"] = data

	def parseGeneral(self, clanLog):
		results = {}
		return results

	def parseStashActivity(self, clanLog):
		results = {}
		
		match = STASH_PATTERN.search(clanLog)
		if match:
			rows = match.group("rows").split("<br>")
			for row in rows:
				row = row.strip()
				if len(row) > 0:
					data = self.parseStashActivityRow(row)
					category = data["category"]
					if not category in results:
						results[category] = []
					results[category].append(data)
					del data["category"]
		else:
			Report.info("bot", "Stash activity not found in clan activity log")
			
		return results
	
		
	def parseStashActivityRow(self, row):
		data = {"category": "unknown", "text": row}
					
		match = STASH_ROW_ITEM_PATTERN.match(row)
		if match:
			data = self.getStashActivityItemData(match)
			data["category"] = "items"
		if not match:
			match = STASH_ROW_MEAT_PATTERN.match(row)
			if match:
				data = self.getStashActivityMeatData(match)
				data["category"] = "meat"

		return data
	
	def getStashActivityItemData(self, match):				
		data = {}
		data["dateString"] =  match.group("month") + "/" + match.group("day") + "/" + match.group("year") 
		data["timeString"] = match.group("hour") + ":" + match.group("minute") + match.group("ampm") 
		data["userName"] = match.group("userName")
		data["userId"] = int(match.group("userId"))
		data["direction"] = match.group("direction")
		data["quantity"] = int(match.group("quantity"))
		data["item"] = match.group("item")
		return data
	
	def getStashActivityMeatData(self, match):
		data = {}
		data["dateString"] =  match.group("month") + "/" + match.group("day") + "/" + match.group("year") 
		data["timeString"] = match.group("hour") + ":" + match.group("minute") + match.group("ampm") 
		data["userName"] = match.group("userName")
		data["userId"] = int(match.group("userId"))
		data["quantity"] = int(match.group("quantity"))
		return data
	