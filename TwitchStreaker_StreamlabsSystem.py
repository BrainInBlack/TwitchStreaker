#---------------------------------------
#	Script Information
#---------------------------------------
ScriptName = "Twitch Streaker"
Website = "http://www.twitch.tv/BrainInBlack"
Creator = "BrainInBlack"
Version = "1.0.7"
Description = "Tracks new/gift subs to a certain amount."

import time

TimeStamp = None

def Init():
	global TimeStamp
	TimeStamp = time.time()
	return

def Execute(data):
	return

def Tick():
	global TimeStamp
	if time.time() - TimeStamp >= 5:
		TimeStamp = time.time()
		Parent.BroadcastWsEvent("EVENT_REFRESH_OVERLAY", None)
	return

def ReloadSettings(jsonData):
	Parent.BroadcastWsEvent("EVENT_UPDATE_SETTINGS", jsonData)
	return
