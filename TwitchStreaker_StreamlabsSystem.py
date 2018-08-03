ScriptName = "Twitch Streaker"
Website = "https://github.com/BrainInBlack/TwitchStreaker"
Creator = "BrainInBlack"
Version = "1.0.9"
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
	return

def ReloadSettings(jsonData):
	Parent.BroadcastWsEvent("EVENT_UPDATE_SETTINGS", jsonData)
	return
