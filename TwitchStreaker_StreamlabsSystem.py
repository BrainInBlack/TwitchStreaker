ScriptName = "Twitch Streaker"
Website = "https://github.com/BrainInBlack/TwitchStreaker"
Creator = "BrainInBlack"
Version = "1.1.0"
Description = "Tracks new/gift subs to a user defined amount."

def Init():
	return

def Execute(data):
	return

def Tick():
	return

def ReloadSettings(jsonData):
	Parent.BroadcastWsEvent("EVENT_UPDATE_SETTINGS", jsonData)
	return
