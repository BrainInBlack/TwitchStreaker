# -------
# Imports
# -------
import os
import sys
import json
import clr
import codecs

# ----------
# References
# ----------
sys.path.append(os.path.dirname(__file__))
clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib/StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient

# -----------
# Script Info
# -----------
ScriptName = "Twitch Streaker"
Website = "https://github.com/BrainInBlack/TwitchStreaker"
Creator = "BrainInBlack"
Version = "2.0.0"
Description = "Tracker for new and gifted subscriptions with a streak mechanic."

# ----------------
# Global Variables
# ----------------
OSPath = os.path.dirname(__file__)
SessionFile = os.path.join(OSPath, "Session.json")
Session = {}
SettingsFile = os.path.join(OSPath, "Settings.json")
Settings = {}

EventReceiver = None

# ----------
# Initiation
# ----------
def Init():
	global EventReceiver
	global Session
	global Settings

	LoadSession()
	LoadSettings()

	if Session["CurrentSubs"] == 0:
		Session["CurrentGoal"] = Settings["Goal"]
	SanityCheck()

	EventReceiver = StreamlabsEventClient()
	EventReceiver.StreamlabsSocketConnected += EventReceiverConnected
	EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
	EventReceiver.StreamlabsSocketEvent += EventReceiverEvent

	if not Settings["SocketToken"] == "":
		EventReceiver.Connect(Settings["SocketToken"])

# ---------------
# Event Connected
# ---------------
def EventReceiverConnected(sender, args):
	Parent.Log(ScriptName, "Connected")

# ------------------
# Event Disconnected
# ------------------
def EventReceiverDisconnected(sender, args):
	Parent.Log(ScriptName, "Disconnected")

# ----------
# Event Main
# ----------
def EventReceiverEvent(sender, args):
	global Session
	global Settings

	data = args.Data

	if not data.For == "twitch_account":
		Parent.Log(ScriptName, "Only Twitch is supported at this moment.")
		return

	if data.Type == "follow" and Settings["CountFollows"]:
		for message in data.Message:
			if not message.IsLive and not message.IsTest:
				continue
			Settings["CurrentSubs"] += 1

	if data.Type == "subscription":
		for message in data.Message:
			if not message.IsLive and not message.IsTest:
				continue
			#if not Settings["CountResubs"] and message.SubType == "resub":
			#	continue
			#if message.Name == Parent.GetChannelName() or message.Name == message.Gifter:
			#	continue
			if message.SubPlan == "1000" or message.SubPlan == "Prime":
				Session["CurrentSubs"] += Settings["Tier1"]
			elif message.SubPlan == "2000":
				Session["CurrentSubs"] += Settings["Tier2"]
			elif message.SubPlan == "3000":
				Session["CurrentSubs"] += Settings["Tier3"]

	while Session["CurrentSubs"] >= Settings["Goal"]:
		Session["CurrentSubs"] -= Settings["Goal"]
		if Session["CurrentGoal"] < Settings["GoalMax"]:
			Session["CurrentGoal"] += Session["GoalIncrement"]
		Session["CurrentStreak"] += 1

	UpdateOverlay()

# --------------
# Update Overlay
# --------------
def UpdateOverlay():
	return

# ------------
# Sanity Check
# ------------
def SanityCheck():
	global Session
	global Settings

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

# ------------
# Save Session
# ------------
def SaveSession():
	global Session
	global SessionFile
	file = open(SessionFile, "w")
	file.write(str(json.JSONEncoder().encode(Session)))
	file.close()

# ------------
# Load Session
# ------------
def LoadSession():
	global Session
	global SessionFile

	try:
		with codecs.open(SessionFile, encoding="utf-8-sig", mode="r") as file:
			Session = json.load(file, encoding="utf-8-sig")
	except:
		Session = {
			# Default
			"CurrentSubs": 0,
			"CurrentStreak": 1,
			"CurrentGoal": 10,
		}
		SaveSession()

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

# -------------
# Save Settings
# -------------
def SaveSettings():
	global Settings
	global SettingsFile
	file = open(SettingsFile, "w")
	file.write(str(json.JSONEncoder().encode(Settings)))
	file.close()

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
		Settings = {
			# Default
			"Goal": 10,
			"GoalMin": 5,
			"GoalMax": 10,
			"GoalIncrement": 1,
			"Tier1": 1,
			"Tier2": 1,
			"Tier3": 1,
			"CountFollows": False,
			"CountResubs": True,
			"SocketToken": ""
		}
		SaveSettings()

# ---------------
# Reload Settings
# ---------------
def ReloadSettings(jsonData):
	LoadSettings()
	Parent.Log(ScriptName, "Settings Reloaded")

# ------
# Unload
# ------
def Unload():
	global EventReceiver
	if EventReceiver and EventReceiver.IsConnected:
		EventReceiver.Disconnect()
	EventReceiver = None
	SaveSession()

# -------
# Execute
# -------
def Execute(data):
	return

# ----
# Tick
# ----
def Tick():
	return
