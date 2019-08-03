# -------
# Imports
# -------
import os
import sys
import json
import clr
import codecs

sys.path.append(os.path.dirname(__file__))
clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib/StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient

# -----------
# Script Info
# -----------
ScriptName = 'Twitch Streaker'
Website = 'https://github.com/BrainInBlack/TwitchStreaker'
Creator = 'BrainInBlack'
Version = '2.0.0'
Description = 'Tracker for new and gifted subscriptions with a streak mechanic.'

# ----------------
# Global Variables
# ----------------
OSPath = os.path.dirname(__file__)
SettingsFile = os.path.join(OSPath, "Settings.json")
Settings = {}

EventReceiver = None



def EventReceiverConnected(sender, args):
	Parent.Log(ScriptName, "Connected")

def EventReceiverDisconnected(sender, args):
	Parent.Log(ScriptName, "Disconnected")

def EventReceiverEvent(sender, args):
	data = args.Data

	global Settings

	if not data.For == "twitch_account":
		Parent.Log(ScriptName, "Only Twitch is supported at this moment.")
		return

	Parent.Log(ScriptName, data.Type)

	if data.Type == "follow" and Settings["CountFollows"]:
		for message in data.Message:
			if not message.IsLive and not message.IsTest:
				continue
			Settings["Goal"] = Settings["Goal"] + 1

	if data.Type == "subscription":
		for message in data.Message:
			Parent.Log(ScriptName, message)
			if not message.IsLive and not message.IsTest:
				continue
			if not Settings["CountResubs"] and message.SubType == "resub":
				continue
			if message.Name == Settings["StreamerName"] or message.Name == message.Gifter:
				continue
			Parent.Log(ScriptName, message.Name)





def SanityCheck():

	# Import Globals
	global Settings

	if Settings["GoalMin"] < 1:
		Settings["GoalMin"] = 1
	if Settings["GoalMin"] > Settings["GoalInitial"]:
		Settings["GoalMin"] = Settings["GoalInitial"]
	if Settings["GoalMax"] < Settings["GoalInitial"]:
		Settings["GoalMax"] = Settings["GoalInitial"]
	if Settings["Goal"] > Settings["GoalMax"]:
		Settings["Goal"] = Settings["GoalMax"]
	if Settings["Tier1"] < 1:
		Settings["Tier1"] = 1
	if Settings["Tier2"] < 1:
		Settings["Tier2"] = 1
	if Settings["Tier3"] < 1:
		Settings["Tier3"] = 1

def Init():

	# Import Globals
	global EventReceiver
	global Settings
	global SettingsFile

	try:
		with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as file:
			Settings = json.load(file, encoding='utf-8-sig')
	except:
		Settings = {
			"StreamerName": Parent.GetChannelName(),
			"CurrentSubs": 0,
			"CurrentStreak": 1,
			"Goal": 10,
			"GoalMin": 5,
			"GoalMax": 10,
			"GoalIncrement": 1,
			"GoalInitial": 10,
			"Tier1": 1,
			"Tier2": 1,
			"Tier3": 1,
			"CountFollows": False,
			"CountResubs": True,
			"ManualMode": False,
			"SocketToken": ""
		}
		SaveSettings()

	SanityCheck()

	EventReceiver = StreamlabsEventClient()
	EventReceiver.StreamlabsSocketConnected += EventReceiverConnected
	EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
	EventReceiver.StreamlabsSocketEvent += EventReceiverEvent

	if not Settings["SocketToken"] == "":
		EventReceiver.Connect(Settings["SocketToken"])

def SaveSettings():
	file = open(SettingsFile, "w")
	file.write(str(json.JSONEncoder().encode(Settings)))
	file.close()

def LoadSettings():
	global Settings
	global SettingsFile

	Settings = None

	try:
		with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as file:
			Settings = json.load(file, encoding='utf-8-sig')
	except:
		Settings = {
			"StreamerName": Parent.GetChannelName(),
			"CurrentSubs": 0,
			"CurrentStreak": 1,
			"Goal": 10,
			"GoalMin": 5,
			"GoalMax": 10,
			"GoalIncrement": 1,
			"GoalInitial": 10,
			"Tier1": 1,
			"Tier2": 1,
			"Tier3": 1,
			"CountFollows": False,
			"CountResubs": True,
			"ManualMode": False,
			"SocketToken": ""
		}
		SaveSettings()

def Unload():
	global EventReceiver
	if EventReceiver and EventReceiver.IsConnected:
		EventReceiver.Disconnect()
	EventReceiver = None

def Execute(data):
	return

def Tick():
	return

def ReloadSettings(jsonData):
	LoadSettings()
	Parent.Log(ScriptName, "Settings Reloaded")
