from kol.database import HogDatabase
from kol.util import Report

def logClanStash(responseData, clanName, session):
    if "stashActivity" in responseData and "items" in responseData["stashActivity"]:
        exactMatches = 0
        for data in responseData["stashActivity"]["items"]:                        
            if HogDatabase.insertClanStashRecordIfNew(data["dateString"], data["timeString"], data["userName"], data["userId"], clanName, data["direction"], data["quantity"], data["item"]) == False:
                exactMatches = exactMatches + 1
                
            if exactMatches > 10:
                break
    
    return True
