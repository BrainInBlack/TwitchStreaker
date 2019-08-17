# -------
# Imports
# -------
import os
import sys
import json
import clr
import codecs
import time

# ----------
# References
# ----------
sys.path.append(os.path.dirname(__file__))
clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Lib/StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient

# -----------
# Script Info
# -----------
ScriptName = "Twitch Streaker"
Website = "https://github.com/BrainInBlack/TwitchStreaker"
Creator = "BrainInBlack"
Version = "2.0.1"
Description = "Tracker for new and gifted subscriptions with a streak mechanic."

# ----------------
# Global Variables
# ----------------
Session = {}
Settings = {}
SessionFile = os.path.join(os.path.dirname(__file__), "Session.json")
SettingsFile = os.path.join(os.path.dirname(__file__), "Settings.json")

ChannelName = None
EventReceiver = None
TimerDelay = 2
TimerStamp = None


# ----------
# Initiation
# ----------
def Init():
	global EventReceiver
	global Session
	global Settings
	global TimerStamp
	global ChannelName

	LoadSettings()
	LoadSession()
	SanityCheck()

	EventReceiver = StreamlabsEventClient()
	EventReceiver.StreamlabsSocketConnected += EventReceiverConnected
	EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
	EventReceiver.StreamlabsSocketEvent += EventReceiverEvent

	if not Settings["SocketToken"] == "":
		EventReceiver.Connect(Settings["SocketToken"])
	else:
		Parent.Log(ScriptName, "No SocketToken! Please follow the instructions in the README.md")

	TimerStamp = time.time()
	ChannelName = Parent.GetChannelName().lower()

	return


# ----------
# Event Main
# ----------
def EventReceiverEvent(sender, args):
	global Session
	global Settings
	global ChannelName

	data = args.Data

	if not data.For == "twitch_account":
		Parent.Log(ScriptName, "Only Twitch is supported at this moment.")
		return

	if data.Type == "follow" and Settings["CountFollows"]:
		for message in data.Message:
			if not message.IsLive and not message.IsTest:
				Parent.Log(ScriptName, "Ignored Follow, Stream is not Live")
				continue
			Settings["CurrentSubs"] += 1
		SaveSession()

	if data.Type == "subscription":
		for message in data.Message:

			if not message.IsLive and not message.IsTest:
				Parent.Log(ScriptName, "Ignored Subscription, Stream is not Live")
				continue

			if not message.Gifter == None:
				if message.Gifter.lower() == ChannelName and not message.IsTest:
					Parent.Log(ScriptName, "Ignored StreamerGift from " + message.Gifter)
					continue
				if message.Name.lower() == message.Gifter.lower() and not message.IsTest:
					Parent.Log(ScriptName, "Ignored SelfGift from " + message.Gifter)
					continue

			if message.SubType == "resub" and not Settings["CountResubs"] and not message.IsTest:
				Parent.Log(ScriptName, "Ignored Resub by " + message.Name)
				continue

			if message.SubPlan == "1000" or message.SubPlan == "Prime":
				Session["CurrentSubs"] += Settings["Tier1"]
			elif message.SubPlan == "2000":
				Session["CurrentSubs"] += Settings["Tier2"]
			elif message.SubPlan == "3000":
				Session["CurrentSubs"] += Settings["Tier3"]
		SaveSession()
	return


# ---------------
# Event Connected
# ---------------
def EventReceiverConnected(sender, args):
	Parent.Log(ScriptName, "Connected")
	return


# ------------------
# Event Disconnected
# ------------------
def EventReceiverDisconnected(sender, args):
	Parent.Log(ScriptName, "Disconnected")
	return


# ----
# Tick
# ----
def Tick():
	global Session
	global Settings
	global TimerDelay
	global TimerStamp

	if (time.time() - TimerStamp) > TimerDelay:
		TimerStamp = time.time()

		while Session["CurrentSubs"] >= Session["CurrentGoal"]:
			Session["CurrentSubs"] -= Session["CurrentGoal"]
			if Session["CurrentGoal"] < Settings["GoalMax"]:
				Session["CurrentGoal"] += Settings["GoalIncrement"]
			Session["CurrentStreak"] += 1
			SaveSession()

		Parent.BroadcastWsEvent("EVENT_UPDATE_OVERLAY", str(json.JSONEncoder().encode(Session)))
	return


# ------------
# Sanity Check
# ------------
def SanityCheck():
	global Session
	global Settings

	if Session == None:
		LoadSession()

	if Settings["GoalMin"] < 1:
		Settings["GoalMin"] = 1
	if Settings["GoalMin"] > Settings["Goal"]:
		Settings["GoalMin"] = Settings["Goal"]
	if Settings["GoalMax"] < Settings["Goal"]:
		Settings["GoalMax"] = Settings["Goal"]
	if Session["CurrentGoal"] < Settings["GoalMin"]:
		Session["CurrentGoal"] = Settings["GoalMin"]
	if Session["CurrentGoal"] > Settings["GoalMax"]:
		Session["CurrentGoal"] = Settings["GoalMax"]
	if Settings["Tier1"] < 1:
		Settings["Tier1"] = 1
	if Settings["Tier2"] < 1:
		Settings["Tier2"] = 1
	if Settings["Tier3"] < 1:
		Settings["Tier3"] = 1
	return


# ------------
# Load Session
# ------------
def LoadSession():
	global Session
	global SessionFile
	global Settings

	if Settings == None:
		LoadSettings()

	try:
		with codecs.open(SessionFile, encoding="utf-8-sig", mode="r") as file:
			Session = json.load(file, encoding="utf-8-sig")
	except:
		Session = {
			# Default
			"CurrentSubs": 0,
			"CurrentStreak": 1,
			"CurrentGoal": Settings["Goal"]
		}
		SaveSession()
	return


# ------------
# Save Session
# ------------
def SaveSession():
	global Session
	global SessionFile

	file = open(SessionFile, "w")
	file.write(str(json.JSONEncoder().encode(Session)))
	file.close()

	return


# -------------
# Reset Session
# -------------
def ResetSession():
	global Session
	global Settings

	Session["CurrentSubs"] = 0
	Session["CurrentStreak"] = 1
	Session["CurrentGoal"] = Settings["Goal"]
	SaveSession()

	return


# -------------
# Load Settings
# -------------
def LoadSettings():
	global Settings
	global SettingsFile

	Settings = None

	try:
		with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as file:
			Settings = json.load(file, encoding="utf-8-sig")
	except:
		Parent.Log(ScriptName, "Unable to load Settings, please Save the Settings at least once!")
	return


# ---------------
# Reload Settings
# ---------------
def ReloadSettings(jsonData):
	LoadSettings()
	SanityCheck()
	return


# -------------
# Sub Functions
# -------------
def AddSub():
	global Session
	Session["CurrentSubs"] += 1
	return

def SubtractSub():
	global Session
	if Session["CurrentSubs"] > 0:
		Session["CurrentSubs"] -= 1
	return


# ----------------
# Streak Functions
# ----------------
def AddStreak():
	global Session
	Session["CurrentStreak"] += 1
	return

def AddStreak5():
	global Session
	Session["CurrentStreak"] += 5
	return

def AddStreak10():
	global Session
	Session["CurrentStreak"] += 10
	return

def SubtractStreak():
	global Session
	if Session["CurrentStreak"] > 1:
		Session["CurrentStreak"] -= 1
	return

def SubtractStreak5():
	global Session
	if Session["CurrentStreak"] > 1:
		Session["CurrentStreak"] -= 5
	return

def SubtractStreak10():
	global Session
	if Session["CurrentStreak"] > 1:
		Session["CurrentStreak"] -= 10
	return


# -------------
# Goal Function
# -------------
def AddToGoal():
	global Session
	if Session["CurrentGoal"] < Settings["GoalMax"]:
		Session["CurrentGoal"] += 1
	return

def SubtractFromGoal():
	global Session
	if Session["CurrentGoal"] > Settings["GoalMin"]:
		Session["CurrentGoal"] -= 1
	return


# ------
# Unload
# ------
def Unload():
	global EventReceiver
	if EventReceiver and EventReceiver.IsConnected:
		EventReceiver.Disconnect()
	EventReceiver = None
	SaveSession()
	return


# -------
# Execute
# -------
def Execute(data):
	return
