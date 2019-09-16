# -------
# Imports
# -------
import codecs
import json
import os
import sys
import time


# ----------
# References
# ----------
import clr
sys.path.append(os.path.dirname(__file__))
clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Lib/StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient

# -----------
# Script Info
# -----------
ScriptName  = "Twitch Streaker"
Website     = "https://github.com/BrainInBlack/TwitchStreaker"
Creator     = "BrainInBlack"
Version     = "2.2.1"
Description = "Tracker for new and gifted subscriptions with a streak mechanic."

# ----------------
# Global Variables
# ----------------
SessionFile   = os.path.join(os.path.dirname(__file__), "Session.json")
SettingsFile  = os.path.join(os.path.dirname(__file__), "Settings.json")

ChannelName   = None
EventReceiver = None
Session = {
	"CurrentGoal": 10,
	"CurrentSubs": 0,
	"CurrentSubsLeft": 10,
	"CurrentStreak": 1,
	"CurrentTotalSubs": 0
}
Settings = {
	"Goal": 10,
	"GoalMin": 5,
	"GoalMax": 10,
	"GoalIncrement": 1,
	"CountResubs": False,
	"SocketToken": None,
	"Tier1": 1,
	"Tier2": 1,
	"Tier3": 1
}
TimerDelay    = 5
TimerStamp    = None


# ----------
# Initiation
# ----------
def Init():
	global ChannelName, EventReceiver, Settings, TimerStamp

	LoadSettings()
	LoadSession()
	SanityCheck()

	EventReceiver                               = StreamlabsEventClient()
	EventReceiver.StreamlabsSocketConnected    += EventReceiverConnected
	EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
	EventReceiver.StreamlabsSocketEvent        += EventReceiverEvent

	if not Settings["SocketToken"] == "":
		EventReceiver.Connect(Settings["SocketToken"])
	else:
		Parent.Log(ScriptName, "No SocketToken! Please follow the instructions in the README.md")

	TimerStamp  = time.time()
	ChannelName = Parent.GetChannelName().lower()


# ----------
# Event Main
# ----------
def EventReceiverEvent(sender, args):
	global ChannelName, Session, Settings

	data = args.Data

	# Twitch
	if data.For == "twitch_account":

		if data.Type == "subscription":
			for message in data.Message:

				if not message.IsLive and not message.IsTest:
					Parent.Log(ScriptName, "Ignored Subscription, Stream is not Live")
					continue

				# GiftSub and Resub Checks
				if message.Gifter is not None:
					if message.Gifter.lower() == ChannelName and not message.IsTest:
						Parent.Log(ScriptName, "Ignored StreamerGift from " + message.Gifter)
						continue
					if message.Name.lower() == message.Gifter.lower() and not message.IsTest:
						Parent.Log(ScriptName, "Ignored SelfGift from " + message.Gifter)
						continue
				else:
					if message.SubType == "resub" and not Settings["CountResubs"] and not message.IsTest:
						Parent.Log(ScriptName, "Ignored Resub by " + message.Name)
						continue

				if message.SubPlan == "1000" or message.SubPlan == "Prime":
					Session["CurrentSubs"]      += Settings["Tier1"]
					Session["CurrentTotalSubs"] += Settings["Tier1"]
				elif message.SubPlan == "2000":
					Session["CurrentSubs"]      += Settings["Tier2"]
					Session["CurrentTotalSubs"] += Settings["Tier2"]
				elif message.SubPlan == "3000":
					Session["CurrentSubs"]      += Settings["Tier3"]
					Session["CurrentTotalSubs"] += Settings["Tier3"]
				Parent.Log("Counted Sub by {}".format(message.Name))

			UpdateOverlay()

	# Mixer
	if data.For == "mixer_account":

		if data.Type == "subscription":
			for message in data.Message:

				if not message.IsLive and not message.IsTest:
					Parent.Log(ScriptName, "Ignored Subscription, Stream is not Live")
					continue

				if message.Months > 1 and not Settings["CountResubs"]:
					Parent.Log("Ignored Resub by " + message.Name)
					continue

				Session["CurrentSubs"]      += 1
				Session["CurrentTotalSubs"] += 1
				Parent.Log("Counted Sub by {}".format(message.Name))

			UpdateOverlay()

	# Youtube
	if data.For == "youtube_account":

		if data.Type == "subscription":
			for message in data.Message:

				if not message.IsLive and not message.IsTest:
					Parent.Log(ScriptName, "Ignored Sponsor, Stream is not Live. (YT)")
					continue

				if message.Months > 1 and not Settings["CountResubs"]:
					Parent.Log(ScriptName, "Ignored Sponsor, Stream is not Live. (YT)")
					continue

				Session["CurrentSubs"]      += 1
				Session["CurrentTotalSubs"] += 1
				Parent.Log("Counted Sub by {}".format(message.Name))

			UpdateOverlay()

	Parent.Log(ScriptName, "Unknown/Unsupported Platform {}!".format(data.For))


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


# ---------------
# Parse Parameter
# ---------------
def Parse(parse_string, user_id, username, target_id, target_name, message):
	global Session

	if "$tsGoal" in parse_string:
		return parse_string.replace("$tsGoal", str(Session["CurrentGoal"]))

	if "$tsStreak" in parse_string:
		return parse_string.replace("$tsStreak", str(Session["CurrentStreak"]))

	if "$tsSubs" in parse_string:
		return parse_string.replace("$tsSubs", str(Session["CurrentSubs"]))

	if "$tsSubsLeft" in parse_string:
		return parse_string.replace("$tsSubsLeft", str(Session["CurrentSubsLeft"]))

	if "$tsTotalSubs" in parse_string:
		return parse_string.replace("$tsSubsLeft", str(Session["CurrentTotalSubs"]))

	return parse_string


# --------------
# Update Overlay
# --------------
def UpdateOverlay():
	global Session, Settings, TimerStamp

	Session["CurrentSubsLeft"] = Session["CurrentGoal"] - Session["CurrentSubs"]

	while Session["CurrentSubs"] >= Session["CurrentGoal"]:
		Session["CurrentSubs"]   -= Session["CurrentGoal"]

		# Increment CurrentGoal
		if Session["CurrentGoal"]   < Settings["GoalMax"]:
			Session["CurrentGoal"] += Settings["GoalIncrement"]

			# Limit CurrentGoal to GoalMax
			if Session["CurrentGoal"]  > Settings["GoalMax"]:
				Session["CurrentGoal"] = Settings["GoalMax"]

		Session["CurrentStreak"] += 1
	Parent.BroadcastWsEvent("EVENT_UPDATE_OVERLAY", str(json.JSONEncoder().encode(Session)))
	TimerStamp = time.time()


# ----
# Tick
# ----
def Tick():
	global TimerDelay, TimerStamp

	if (time.time() - TimerStamp) > TimerDelay:
		UpdateOverlay()
		SaveSession()


# ------------
# Sanity Check
# ------------
def SanityCheck():
	global Session, Settings

	is_session_dirty = False
	is_settings_dirty = False

	if Session is None:
		LoadSession()

	# Prevent GoalMin from being Zero
	if Settings["GoalMin"]  < 1:
		Settings["GoalMin"] = 1
		is_settings_dirty = True

	# Prevent GoalMin from being higher than the Goal
	if Settings["GoalMin"]  > Settings["Goal"]:
		Settings["GoalMin"] = Settings["Goal"]
		is_settings_dirty = True

	# Prevent GoalMax from being lower than the Goal
	if Settings["GoalMax"]  < Settings["Goal"]:
		Settings["GoalMax"] = Settings["Goal"]
		is_settings_dirty = True

	# Prevent CurrentGoal from being lower than GoalMin
	if Session["CurrentGoal"]  < Settings["GoalMin"]:
		Session["CurrentGoal"] = Settings["GoalMin"]
		is_session_dirty = True

	# Prevent CurrentGoal from being higher than GoalMax
	if Session["CurrentGoal"]  > Settings["GoalMax"]:
		Session["CurrentGoal"] = Settings["GoalMax"]
		is_session_dirty = True

	# Prevent Tier1 from being less than 1
	if Settings["Tier1"]  < 1:
		Settings["Tier1"] = 1
		is_settings_dirty = True

	# Prevent Tier2 from being less than 1
	if Settings["Tier2"]  < 1:
		Settings["Tier2"] = 1
		is_settings_dirty = True

	# Prevent Tier3 from being less than 1
	if Settings["Tier3"]  < 1:
		Settings["Tier3"] = 1
		is_settings_dirty = True

	# Prevent GoalIncrement from being less than 0
	if Settings["GoalIncrement"] < 0:
		Settings["GoalIncrement"] = 0
		is_settings_dirty = True

	if is_session_dirty:
		SaveSession()

	if is_settings_dirty:
		SaveSettings()


# -----------------
# Session Functions
# -----------------
def LoadSession():
	global Session, SessionFile, Settings

	try:
		with codecs.open(SessionFile, encoding="utf-8-sig", mode="r") as f:
			Session = json.load(f, encoding="utf-8-sig")
			Session["CurrentGoal"] = Settings["Goal"]
	except:
		SaveSession()

def SaveSession():
	global Session, SessionFile

	with open(SessionFile, "w") as f:
		json.dump(Session, f, sort_keys=True, indent=4)
		f.close()


def ResetSession():
	global Session, Settings

	Session["CurrentGoal"]      = Settings["Goal"]
	Session["CurrentSubs"]      = 0
	Session["CurrentSubsLeft"]  = Session["CurrentGoal"]
	Session["CurrentStreak"]    = 1
	Session["CurrentTotalSubs"] = 0
	SaveSession()


# ------------------
# Settings Functions
# ------------------
def LoadSettings():
	global Settings, SettingsFile

	try:
		with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as f:
			Settings = json.load(f, encoding="utf-8-sig")
	except:
		Parent.Log(ScriptName, "Unable to load Settings, please Save the Settings at least once!")


def SaveSettings():
	global Settings, SettingsFile

	with codecs.open(SettingsFile, "w") as f:
		json.dump(Settings, f, sort_keys=True, indent=4)
		f.close()


def ReloadSettings(json_data):
	LoadSettings()
	SanityCheck()


# -------------
# Sub Functions
# -------------
def AddSub():
	global Session
	Session["CurrentSubs"] += 1
	UpdateOverlay()


def SubtractSub():
	global Session
	if Session["CurrentSubs"] > 0:
		Session["CurrentSubs"] -= 1
		UpdateOverlay()


# ----------------
# Streak Functions
# ----------------
def AddStreak():
	global Session
	Session["CurrentStreak"] += 1
	UpdateOverlay()


def AddStreak5():
	global Session
	Session["CurrentStreak"] += 5
	UpdateOverlay()


def AddStreak10():
	global Session
	Session["CurrentStreak"] += 10
	UpdateOverlay()


def SubtractStreak():
	global Session
	if Session["CurrentStreak"] > 1:
		Session["CurrentStreak"] -= 1
		UpdateOverlay()


def SubtractStreak5():
	global Session
	if Session["CurrentStreak"] > 1:
		Session["CurrentStreak"] -= 5
		UpdateOverlay()


def SubtractStreak10():
	global Session
	if Session["CurrentStreak"] > 1:
		Session["CurrentStreak"] -= 10
		UpdateOverlay()


# --------------
# Goal Functions
# --------------
def AddToGoal():
	global Session
	if Session["CurrentGoal"] < Settings["GoalMax"]:
		Session["CurrentGoal"] += 1
		UpdateOverlay()


def SubtractFromGoal():
	global Session
	if Session["CurrentGoal"] > Settings["GoalMin"]:
		Session["CurrentGoal"] -= 1
		UpdateOverlay()


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
