# -------
# Imports
# -------
import codecs, json, math, os, sys, time


# ----------
# References
# ----------
import clr
clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Lib/StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient

# -----------
# Script Info
# -----------
ScriptName  = "Twitch Streaker"
Website     = "https://github.com/BrainInBlack/TwitchStreaker"
Creator     = "BrainInBlack"
Version     = "2.5.2"
Description = "Tracker for new and gifted subscriptions with a streak mechanic."

# ----------------
# Global Variables
# ----------------
ScriptFolder = os.path.dirname(__file__)
TextFolder    = os.path.join(ScriptFolder, "Text/")

SessionFile  = os.path.join(ScriptFolder, "Session.json")
SettingsFile = os.path.join(ScriptFolder, "Settings.json")

GoalFile      = os.path.join(TextFolder, "Goal.txt")
SubsFile      = os.path.join(TextFolder, "Subs.txt")
SubsLeftFile  = os.path.join(TextFolder, "SubsLeft.txt")
StreakFile    = os.path.join(TextFolder, "Streak.txt")
TotalSubsFile = os.path.join(TextFolder, "TotalSubs.txt")

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
	"CountDonations": False,
	"CountDonationsOnce": False,
	"CountReSubs": False,
	"DonationMinAmount": 5.0,
	"Goal": 10,
	"GoalMin": 5,
	"GoalMax": 10,
	"GoalIncrement": 1,
	"SocketToken": None,
	"Sub1": 1, "Sub2": 1, "Sub3": 1,
	"ReSub1": 1, "ReSub2": 1, "ReSub3": 1,
	"GiftSub1": 1, "GiftSub2": 1, "GiftSub3": 1,
	"GiftReSub1": 1, "GiftReSub2": 1, "GiftReSub3": 1
}
RefreshDelay = 5
RefreshStamp = None
SaveDelay    = 300
SaveStamp    = None

TierArray = [
	"Sub1", "Sub2", "Sub3",
	"ReSub1", "ReSub2", "ReSub3",
	"GiftSub1", "GiftSub2", "GiftSub3",
	"GiftReSub1", "GiftReSub2", "GiftReSub3"
]


# ----------
# Initiation
# ----------
def Init():
	global ChannelName, EventReceiver, Settings, RefreshStamp, SaveStamp

	LoadSettings()
	LoadSession()
	SanityCheck()

	ChannelName  = Parent.GetChannelName()
	RefreshStamp = time.time()
	SaveStamp    = time.time()

	if Settings["SocketToken"] == "":
		Log("No SocketToken found! Please follow the instructions in the README.md and reload the script!")
		return

	if ChannelName is None:
		Log("Bot or Streamer Account are not connected, please check your connections and reload the script!")
		return
	ChannelName  = ChannelName.lower()

	EventReceiver                               = StreamlabsEventClient()
	EventReceiver.StreamlabsSocketConnected    += EventReceiverConnected
	EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
	EventReceiver.StreamlabsSocketEvent        += EventReceiverEvent
	EventReceiver.Connect(Settings["SocketToken"])


def ReInit():
	global ChannelName, EventReceiver, Settings

	if ChannelName is None: return
	ChannelName = ChannelName.lower()

	EventReceiver                               = StreamlabsEventClient()
	EventReceiver.StreamlabsSocketConnected    += EventReceiverConnected
	EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
	EventReceiver.StreamlabsSocketEvent        += EventReceiverEvent
	EventReceiver.Connect(Settings["SocketToken"])


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

				# Live Check
				if not message.IsLive and not message.IsTest:
					Log("Ignored Subscription, Stream is not Live")
					continue

				# GiftSub Check
				if message.SubType == "subgift":

					# Ignore Gifted Subs by Streamer
					if message.Gifter == ChannelName and not message.IsTest:
						Log("Ignored StreamerGift from {}".format(message.Gifter))
						continue

					# Ignore Self-Gifted Subs
					if message.Name == message.Gifter and not message.IsTest:
						Log("Ignored SelfGift from {}".format(message.Gifter))
						continue

				# ReSub Check
				if message.SubType == "resub" and not Settings["CountReSubs"] and not message.IsTest:
					Log("Ignored Resub by {}".format(message.Name))
					continue

				# Gifted Subs
				if message.SubType == "subgift":

					# GiftedSubs (normal)
					if message.Months is not None:

						if message.SubPlan == "Prime":
							Session["CurrentSubs"]      += Settings["GiftReSub1"]
							Session["CurrentTotalSubs"] += Settings["GiftReSub1"]

						elif message.SubPlan == "1000":
							Session["CurrentSubs"]      += Settings["GiftReSub1"]
							Session["CurrentTotalSubs"] += Settings["GiftReSub1"]

						elif message.SubPlan == "2000":
							Session["CurrentSubs"]      += Settings["GiftReSub2"]
							Session["CurrentTotalSubs"] += Settings["GiftReSub2"]

						elif message.SubPlan == "3000":
							Session["CurrentSubs"]      += Settings["GiftReSub3"]
							Session["CurrentTotalSubs"] += Settings["GiftReSub3"]

						else: # Skip if invalid plan
							Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
							continue

						Log("Counted {} for {}".format(message.SubType, message.Name))
						continue
					# /GiftedSubs (normal)

					# GiftedSubs (resubs)
					else:

						if message.SubPlan == "Prime":
							Session["CurrentSubs"]      += Settings["GiftSub1"]
							Session["CurrentTotalSubs"] += Settings["GiftSub1"]

						elif message.SubPlan == "1000":
							Session["CurrentSubs"]      += Settings["GiftSub1"]
							Session["CurrentTotalSubs"] += Settings["GiftSub1"]

						elif message.SubPlan == "2000":
							Session["CurrentSubs"]      += Settings["GiftSub2"]
							Session["CurrentTotalSubs"] += Settings["GiftSub2"]

						elif message.SubPlan == "3000":
							Session["CurrentSubs"]      += Settings["GiftSub3"]
							Session["CurrentTotalSubs"] += Settings["GiftSub3"]

						else: # Skip if invalid plan
							Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
							continue

						Log("Counted {} for {}".format(message.SubType, message.Name))
						continue
					# /GiftedSubs (resubs)
				# GiftedSubs - END

				# AnonGiftedSubs
				elif message.SubType == "anonsubgift":

					# AnonGiftedSubs (normal)
					if message.Months is not None:

						if message.SubPlan == "Prime":
							Session["CurrentSubs"]      += Settings["GiftReSub1"]
							Session["CurrentTotalSubs"] += Settings["GiftReSub1"]

						elif message.SubPlan == "1000":
							Session["CurrentSubs"]      += Settings["GiftReSub1"]
							Session["CurrentTotalSubs"] += Settings["GiftReSub1"]

						elif message.SubPlan == "2000":
							Session["CurrentSubs"]      += Settings["GiftReSub2"]
							Session["CurrentTotalSubs"] += Settings["GiftReSub2"]

						elif message.SubPlan == "3000":
							Session["CurrentSubs"]      += Settings["GiftReSub3"]
							Session["CurrentTotalSubs"] += Settings["GiftReSub3"]

						else: # Skip if invalid plan
							Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
							continue

						Log("Counted {} for {}".format(message.SubType, message.Name))
						continue
					# /AnonGiftedSubs (normal)

					# AnonGiftedSubs (resubs)
					else:

						if message.SubPlan == "Prime":
							Session["CurrentSubs"]      += Settings["GiftSub1"]
							Session["CurrentTotalSubs"] += Settings["GiftSub1"]

						elif message.SubPlan == "1000":
							Session["CurrentSubs"]      += Settings["GiftSub1"]
							Session["CurrentTotalSubs"] += Settings["GiftSub1"]

						elif message.SubPlan == "2000":
							Session["CurrentSubs"]      += Settings["GiftSub2"]
							Session["CurrentTotalSubs"] += Settings["GiftSub2"]

						elif message.SubPlan == "3000":
							Session["CurrentSubs"]      += Settings["GiftSub3"]
							Session["CurrentTotalSubs"] += Settings["GiftSub3"]

						else: # Skip if invalid plan
							Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
							continue

						Log("Counted {} for {}".format(message.SubType, message.Name))
						continue
					# /AnonGiftedSubs (resubs)
				# AnonGiftedSubs - END

				# ReSubs
				elif message.SubType == "resub":

					if message.SubPlan == "Prime":
						Session["CurrentSubs"]      += Settings["ReSub1"]
						Session["CurrentTotalSubs"] += Settings["ReSub1"]

					elif message.SubPlan == "1000":
						Session["CurrentSubs"]      += Settings["ReSub1"]
						Session["CurrentTotalSubs"] += Settings["ReSub1"]

					elif message.SubPlan == "2000":
						Session["CurrentSubs"]      += Settings["ReSub2"]
						Session["CurrentTotalSubs"] += Settings["ReSub2"]

					elif message.SubPlan == "3000":
						Session["CurrentSubs"]      += Settings["ReSub3"]
						Session["CurrentTotalSubs"] += Settings["ReSub3"]

					else: # Skip if invalid plan
						Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
						continue

					Log("Counted {} by {}".format(message.SubType, message.Name))
					continue
				# Resubs - END

				# Subs
				else:

					if message.SubPlan == "Prime":
						Session["CurrentSubs"]      += Settings["Sub1"]
						Session["CurrentTotalSubs"] += Settings["Sub1"]

					elif message.SubPlan == "1000":
						Session["CurrentSubs"]      += Settings["Sub1"]
						Session["CurrentTotalSubs"] += Settings["Sub1"]

					elif message.SubPlan == "2000":
						Session["CurrentSubs"]      += Settings["Sub2"]
						Session["CurrentTotalSubs"] += Settings["Sub2"]

					elif message.SubPlan == "3000":
						Session["CurrentSubs"]      += Settings["Sub3"]
						Session["CurrentTotalSubs"] += Settings["Sub3"]

					else: # Skip if invalid plan
						Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
						continue

					Log("Counted {} by {}".format(message.SubType, message.Name))
					continue
				# Subs - END

		return # /Twitch

	# Mixer
	if data.For == "mixer_account":

		if data.Type == "subscription":
			for message in data.Message:

				if not message.IsLive and not message.IsTest:
					Log("Ignored Subscription, Stream is not Live")
					continue

				if message.Months > 1 and not Settings["CountResubs"]:
					Log("Ignored Resub by {}".format(message.Name))
					continue

				Session["CurrentSubs"]      += Settings["Sub1"]
				Session["CurrentTotalSubs"] += Settings["Sub1"]
				Log("Counted Sub by {}".format(message.Name))

		return # /Mixer

	# Youtube
	if data.For == "youtube_account":

		if data.Type == "subscription":
			for message in data.Message:

				if not message.IsLive and not message.IsTest:
					Log("Ignored Sponsor, Stream is not Live. (YT)")
					continue

				if message.Months > 1 and not Settings["CountResubs"]:
					Log("Ignored Sponsor, Stream is not Live. (YT)")
					continue

				Session["CurrentSubs"]      += Settings["Sub1"]
				Session["CurrentTotalSubs"] += Settings["Sub1"]
				Log("Counted Sub by {}".format(message.Name))

		return # /Youtube

	# Streamlabs
	if data.For == "streamlabs":

		if data.Type == "donation" and Settings["CountDonations"]:
			for message in data.Message:

				if not message.IsLive and not message.IsTest:
					Log("Ignored Donation, Stream is not Live.")
					continue

				if message.Amount > Settings["DonationMinAmount"]:
					if Settings["CountDonationsOnce"]: res = 1
					else: res = math.trunc(message.Amount / Settings["DonationMinAmount"])
					Session["CurrentSubs"]      += res
					Session["CurrentTotalSubs"] += res
					Log("Added {} Sub(s) for a {} Donation by {}.".format(res, message.FormatedAmount, message.Name))

		return # /Streamlabs

	Log("Unknown/Unsupported Platform {}!".format(data.For))


# ---------------
# Event Connected
# ---------------
def EventReceiverConnected(sender, args):
	Log("Connected")


# ------------------
# Event Disconnected
# ------------------
def EventReceiverDisconnected(sender, args):
	Log("Disconnected")


# ---------------
# Parse Parameter
# ---------------
def Parse(parse_string, user_id, username, target_id, target_name, message):
	global Session

	if "$tsGoal" in parse_string:
		parse_string = parse_string.replace("$tsGoal", str(Session["CurrentGoal"]))

	if "$tsStreak" in parse_string:
		parse_string = parse_string.replace("$tsStreak", str(Session["CurrentStreak"]))

	if "$tsSubs" in parse_string:
		parse_string = parse_string.replace("$tsSubs", str(Session["CurrentSubs"]))

	if "$tsSubsLeft" in parse_string:
		parse_string = parse_string.replace("$tsSubsLeft", str(Session["CurrentSubsLeft"]))

	if "$tsTotalSubs" in parse_string:
		parse_string = parse_string.replace("$tsSubsLeft", str(Session["CurrentTotalSubs"]))

	return parse_string


# --------------
# Update Overlay
# --------------
def UpdateOverlay():
	global Session, Settings, RefreshStamp

	Session["CurrentSubsLeft"] = Session["CurrentGoal"] - Session["CurrentSubs"]

	# Streak Calculations
	while Session["CurrentSubs"] >= Session["CurrentGoal"]:
		Session["CurrentSubs"]   -= Session["CurrentGoal"]

		# Increment CurrentGoal
		if Session["CurrentGoal"]   < Settings["GoalMax"]:
			Session["CurrentGoal"] += Settings["GoalIncrement"]

			# Goal Correction
			if Session["CurrentGoal"]  > Settings["GoalMax"]:
				Session["CurrentGoal"] = Settings["GoalMax"]

		# Increment Streak
		Session["CurrentStreak"] += 1

	# Send Update and refresh Timestamp
	Parent.BroadcastWsEvent("EVENT_UPDATE_OVERLAY", str(json.JSONEncoder().encode(Session)))
	RefreshStamp = time.time()


# ----
# Tick
# ----
def Tick():
	global ChannelName, RefreshDelay, RefreshStamp, SaveDelay, SaveStamp

	# Timed Overlay Update
	if (time.time() - RefreshStamp) > RefreshDelay:
		if ChannelName is None: ReInit()
		UpdateOverlay() #! Needs to be before SaveText (refactor soon)
		SaveText()

	# Timed Session Save
	if (time.time() - SaveStamp) > SaveDelay:
		SaveSession()
		SaveStamp = time.time()


# --------
# SaveText
# --------
def SaveText():
	global Session, GoalFile, SubsFile, SubsLeftFile, StreakFile, TotalSubsFile, TextFolder

	if not os.path.isdir(TextFolder):
		os.mkdir(TextFolder)

	with open(GoalFile, "w") as f:
		f.write(str(Session["CurrentGoal"]))
		f.close()

	with open(SubsFile, "w") as f:
		f.write(str(Session["CurrentSubs"]))
		f.close()

	with open(SubsLeftFile, "w") as f:
		f.write(str(Session["CurrentSubsLeft"]))
		f.close()

	with open(StreakFile, "w") as f:
		f.write(str(Session["CurrentStreak"]))
		f.close()

	with open(TotalSubsFile, "w") as f:
		f.write(str(Session["CurrentTotalSubs"]))
		f.close()


# ------------
# Sanity Check
# ------------
def SanityCheck():
	global Session, Settings, TierArray

	is_session_dirty = False
	is_settings_dirty = False

	# Load Session/Settings if not loaded
	if Session is None:
		LoadSession()
	if Settings is None:
		LoadSettings()

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

	# Tier Validation
	for tier in TierArray:
		if tier < 1:
			Settings[tier] = 1
			is_settings_dirty = True

	# Prevent GoalIncrement from being less than 0
	if Settings["GoalIncrement"] < 0:
		Settings["GoalIncrement"] = 0
		is_settings_dirty = True

	# Save Session/Settings if dirty
	if is_session_dirty:
		SaveSession()
	if is_settings_dirty:
		SaveSettings()


# -----------------
# Session Functions
# -----------------
def LoadSession():
	global Session, SessionFile, Settings

	if Settings is None:
		LoadSettings()

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

	if Settings is None:
		LoadSettings()

	Session["CurrentGoal"]      = Settings["Goal"]
	Session["CurrentSubs"]      = 0
	Session["CurrentSubsLeft"]  = Session["CurrentGoal"]
	Session["CurrentStreak"]    = 1
	Session["CurrentTotalSubs"] = 0
	SaveSession()
	UpdateOverlay()
	Log("Session Reset!")


# ------------------
# Settings Functions
# ------------------
def LoadSettings():
	global Settings, SettingsFile

	try:
		with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as f:
			Settings = json.load(f, encoding="utf-8-sig")
	except:
		SaveSettings()


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

# -----------
# Log Wrapper
# -----------
def Log(message):
	Parent.Log(ScriptName, message)
