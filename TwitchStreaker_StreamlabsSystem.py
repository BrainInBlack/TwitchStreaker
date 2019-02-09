ScriptName = 'Twitch Streaker'
Website = 'https://github.com/BrainInBlack/TwitchStreaker'
Creator = 'BrainInBlack'
Version = '1.5.6'
Description = 'Tracker for new and gifted subscriptions with a streak mechanic.'

def Init():
	return

def Execute(data):
	return

def Tick():
	return

def ReloadSettings(jsonData):
	Parent.BroadcastWsEvent('EVENT_UPDATE_SETTINGS', jsonData)
	return
