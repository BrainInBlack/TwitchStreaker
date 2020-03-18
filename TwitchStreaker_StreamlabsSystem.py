# -------
# Imports
# -------
import codecs, json, math, os, time


# -----
# Paths
# -----
ScriptFolder  = os.path.realpath(os.path.dirname(__file__))
TextFolder    = os.path.join(ScriptFolder, "Text/")

SessionFile   = os.path.join(ScriptFolder, "Session.json")
SettingsFile  = os.path.join(ScriptFolder, "Settings.json")

GoalFile      = os.path.join(TextFolder, "Goal.txt")
SubsFile      = os.path.join(TextFolder, "Subs.txt")
SubsLeftFile  = os.path.join(TextFolder, "SubsLeft.txt")
StreakFile    = os.path.join(TextFolder, "Streak.txt")
TotalSubsFile = os.path.join(TextFolder, "TotalSubs.txt")


# ----------
# References
# ----------
import clr
clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(ScriptFolder, "Lib/StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient


# -----------
# Script Info
# -----------
ScriptName  = "Twitch Streaker"
Website     = "https://github.com/BrainInBlack/TwitchStreaker"
Creator     = "BrainInBlack"
Version     = "2.5.7"
Description = "Tracker for new and gifted subscriptions with a streak mechanic."


# ----------------
# Global Variables
# ----------------
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
RefreshDelay = 5    # InSeconds
RefreshStamp = None
SaveDelay    = 300  # InSeconds
SaveStamp    = None


# ------------------
# Internal Variables
# ------------------
IsConnected   = False
IsScriptReady = False
Tiers = [
	"Sub1", "Sub2", "Sub3",
	"ReSub1", "ReSub2", "ReSub3",
	"GiftSub1", "GiftSub2", "GiftSub3",
	"GiftReSub1", "GiftReSub2", "GiftReSub3"
]


# ----------
# Initiation
# ----------
def Init():
	global RefreshStamp, SaveStamp

	# ! Preserve Order
	LoadSettings()
	LoadSession()
	SanityCheck()

	RefreshStamp = time.time()
	SaveStamp    = time.time()

	StartUp()


# -------
# StartUp
# -------
def StartUp():
	global ChannelName, IsScriptReady, Settings

	IsScriptReady = False

	# Check Token
	if len(Settings["SocketToken"]) < 100:
		Log("Socket Token is missing. Please read the README.md for further instructions.")
		return

	# Check Channel Name
	ChannelName = Parent.GetChannelName()
	if ChannelName is None:
		Log("Streamer or Bot Account are not connected. Please check the Account connections in the Chatbot.")
		return

	# Finish and Connect
	ChannelName = ChannelName.lower()
	IsScriptReady = True
	Connect()


# ---------------------
# Connect EventReceiver
# ---------------------
def Connect():
	global EventReceiver, Settings

	EventReceiver = StreamlabsEventClient()
	EventReceiver.StreamlabsSocketConnected    += EventReceiverConnected
	EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
	EventReceiver.StreamlabsSocketEvent        += EventReceiverEvent
	EventReceiver.Connect(Settings["SocketToken"])


# ---------
# Event Bus
# ---------
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

					# GiftedSubs (resubs)
					if message.Months is not None:

						if message.SubPlan == "Prime":
							Session["CurrentSubs"]      += Settings["GiftReSub1"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "1000":
							Session["CurrentSubs"]      += Settings["GiftReSub1"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "2000":
							Session["CurrentSubs"]      += Settings["GiftReSub2"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "3000":
							Session["CurrentSubs"]      += Settings["GiftReSub3"]
							Session["CurrentTotalSubs"] += 1

						else:  # Skip if invalid plan
							Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
							continue

						Log("Counted {} for {}".format(message.SubType, message.Name))
						continue
					# /GiftedSubs (resubs)

					# GiftedSubs (normal)
					else:

						if message.SubPlan == "Prime":
							Session["CurrentSubs"]      += Settings["GiftSub1"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "1000":
							Session["CurrentSubs"]      += Settings["GiftSub1"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "2000":
							Session["CurrentSubs"]      += Settings["GiftSub2"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "3000":
							Session["CurrentSubs"]      += Settings["GiftSub3"]
							Session["CurrentTotalSubs"] += 1

						else:  # Skip if invalid plan
							Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
							continue

						Log("Counted {} for {}".format(message.SubType, message.Name))
						continue
					# /GiftedSubs (normal)
				# GiftedSubs - END

				# AnonGiftedSubs
				elif message.SubType == "anonsubgift":

					# AnonGiftedSubs (resubs)
					if message.Months is not None:

						if message.SubPlan == "Prime":
							Session["CurrentSubs"]      += Settings["GiftReSub1"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "1000":
							Session["CurrentSubs"]      += Settings["GiftReSub1"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "2000":
							Session["CurrentSubs"]      += Settings["GiftReSub2"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "3000":
							Session["CurrentSubs"]      += Settings["GiftReSub3"]
							Session["CurrentTotalSubs"] += 1

						else:  # Skip if invalid plan
							Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
							continue

						Log("Counted {} for {}".format(message.SubType, message.Name))
						continue
					# /AnonGiftedSubs (resubs)

					# AnonGiftedSubs (normal)
					else:

						if message.SubPlan == "Prime":
							Session["CurrentSubs"]      += Settings["GiftSub1"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "1000":
							Session["CurrentSubs"]      += Settings["GiftSub1"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "2000":
							Session["CurrentSubs"]      += Settings["GiftSub2"]
							Session["CurrentTotalSubs"] += 1

						elif message.SubPlan == "3000":
							Session["CurrentSubs"]      += Settings["GiftSub3"]
							Session["CurrentTotalSubs"] += 1

						else:  # Skip if invalid plan
							Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
							continue

						Log("Counted {} for {}".format(message.SubType, message.Name))
						continue
					# /AnonGiftedSubs (normal)
				# AnonGiftedSubs - END

				# ReSubs
				elif message.SubType == "resub":

					if message.SubPlan == "Prime":
						Session["CurrentSubs"]      += Settings["ReSub1"]
						Session["CurrentTotalSubs"] += 1

					elif message.SubPlan == "1000":
						Session["CurrentSubs"]      += Settings["ReSub1"]
						Session["CurrentTotalSubs"] += 1

					elif message.SubPlan == "2000":
						Session["CurrentSubs"]      += Settings["ReSub2"]
						Session["CurrentTotalSubs"] += 1

					elif message.SubPlan == "3000":
						Session["CurrentSubs"]      += Settings["ReSub3"]
						Session["CurrentTotalSubs"] += 1

					else:  # Skip if invalid plan
						Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
						continue

					Log("Counted {} by {}".format(message.SubType, message.Name))
					continue
				# Resubs - END

				# Subs
				else:

					if message.SubPlan == "Prime":
						Session["CurrentSubs"]      += Settings["Sub1"]
						Session["CurrentTotalSubs"] += 1

					elif message.SubPlan == "1000":
						Session["CurrentSubs"]      += Settings["Sub1"]
						Session["CurrentTotalSubs"] += 1

					elif message.SubPlan == "2000":
						Session["CurrentSubs"]      += Settings["Sub2"]
						Session["CurrentTotalSubs"] += 1

					elif message.SubPlan == "3000":
						Session["CurrentSubs"]      += Settings["Sub3"]
						Session["CurrentTotalSubs"] += 1

					else:  # Skip if invalid plan
						Log("Invalid or Unknown SubPlan {}".format(message.SubPlan))
						continue

					Log("Counted {} by {}".format(message.SubType, message.Name))
					continue
				# Subs - END

		return  # /Twitch

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
				Session["CurrentTotalSubs"] += 1
				Log("Counted Sub by {}".format(message.Name))

		return  # /Mixer

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
				Session["CurrentTotalSubs"] += 1
				Log("Counted Sub by {}".format(message.Name))

		return  # /Youtube

	# Streamlabs
	if data.For == "streamlabs":

		if data.Type == "donation" and Settings["CountDonations"]:
			for message in data.Message:

				if not message.IsLive and not message.IsTest:
					Log("Ignored Donation, Stream is not Live.")
					continue

				if message.Amount > Settings["DonationMinAmount"]:
					res = 1
					if not Settings["CountDonationsOnce"]:
						res = math.trunc(message.Amount / Settings["DonationMinAmount"])
					Session["CurrentSubs"] += res
					Log("Added {} Sub(s) for a {} Donation by {}.".format(res, message.FormatedAmount, message.Name))

		return  # /Streamlabs

	Log("Unknown/Unsupported Platform {}!".format(data.For))


# ---------------
# Event Connected
# ---------------
def EventReceiverConnected(sender, args):
	global IsConnected

	IsConnected = True
	Log("Connected")


# ------------------
# Event Disconnected
# ------------------
def EventReceiverDisconnected(sender, args):
	global IsConnected

	IsConnected = False
	Log("Disconnected")


# ----
# Tick
# ----
def Tick():
	global IsConnected, IsScriptReady, RefreshDelay, RefreshStamp, SaveDelay, SaveStamp

	# Fast Timer
	if (time.time() - RefreshStamp) > RefreshDelay:

		# Attempt Startup
		if not IsScriptReady:
			StartUp()

		# Reconnect
		if not IsConnected:
			Connect()

		# Update Everything
		UpdateTracker()

	# Slow Timer
	if (time.time() - SaveStamp) > SaveDelay:
		SaveSession()
		SaveStamp = time.time()


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
# Update Tracker
# --------------
def UpdateTracker():  # ! Should be called only if a quick response is required
	global Session, Settings, RefreshStamp, TextFolder, GoalFile, SubsFile, StreakFile, SubsLeftFile, StreakFile, TotalSubsFile

	# ----------------
	# Calculate Streak
	# ----------------
	Session["CurrentSubsLeft"] = Session["CurrentGoal"] - Session["CurrentSubs"]

	while Session["CurrentSubs"] >= Session["CurrentGoal"]:

		# Subtract Goal and Increment Streak
		Session["CurrentSubs"]   -= Session["CurrentGoal"]
		Session["CurrentStreak"] += 1

		# Increment CurrentGoal
		if Session["CurrentGoal"]   < Settings["GoalMax"]:
			Session["CurrentGoal"] += Settings["GoalIncrement"]

			# Correct Goal if GoalIncrement is bigger than the gap from CurrentGoal to GoalMax
			if Session["CurrentGoal"]  > Settings["GoalMax"]:
				Session["CurrentGoal"] = Settings["GoalMax"]

	# --------------
	# Update Overlay
	# --------------
	Parent.BroadcastWsEvent("EVENT_UPDATE_OVERLAY", str(json.JSONEncoder().encode(Session)))

	# -----------------
	# Update Text Files
	# -----------------
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

	# --------------------
	# Update Refresh Stamp
	# --------------------
	RefreshStamp = time.time()  # * Delay the refresh in the Tick() function


# ------------
# Sanity Check
# ------------
def SanityCheck():
	global Session, Settings, Tiers

	is_session_dirty = False
	is_settings_dirty = False

	# Load Session/Settings if not loaded
	if Settings is None:  # ! Has to be loaded first
		LoadSettings()
	if Session is None:
		LoadSession()

	# Prevent GoalMin from being Zero
	if Settings["GoalMin"]  < 1:
		Settings["GoalMin"] = 1
		is_settings_dirty   = True

	# Prevent GoalMin from being higher than the Goal
	if Settings["GoalMin"]  > Settings["Goal"]:
		Settings["GoalMin"] = Settings["Goal"]
		is_settings_dirty   = True

	# Prevent GoalMax from being lower than the Goal
	if Settings["GoalMax"]  < Settings["Goal"]:
		Settings["GoalMax"] = Settings["Goal"]
		is_settings_dirty   = True

	# Prevent CurrentGoal from being lower than GoalMin
	if Session["CurrentGoal"]  < Settings["GoalMin"]:
		Session["CurrentGoal"] = Settings["GoalMin"]
		is_session_dirty       = True

	# Prevent CurrentGoal from being higher than GoalMax
	if Session["CurrentGoal"]  > Settings["GoalMax"]:
		Session["CurrentGoal"] = Settings["GoalMax"]
		is_session_dirty       = True

	# Tier Validation
	for tier in Tiers:
		if tier < 1:
			Settings[tier]    = 1
			is_settings_dirty = True

	# Prevent GoalIncrement from being less than 0
	if Settings["GoalIncrement"]  < 0:
		Settings["GoalIncrement"] = 0
		is_settings_dirty         = True

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
			f.close()
	except:
		SaveSession()


def SaveSession():
	global Session, SessionFile

	with codecs.open(SessionFile, encoding="utf-8-sig", mode="w") as f:
		json.dump(Session, f, encoding="utf-8-sig", sort_keys=True, indent=4)
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
	UpdateTracker()
	Log("Session Reset!")


# ------------------
# Settings Functions
# ------------------
def LoadSettings():
	global EventReceiver, IsConnected, Settings, SettingsFile

	old_token = Settings["SocketToken"]

	try:
		with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as f:
			new_settings = json.load(f, encoding="utf-8-sig")
			f.close()
	except:
		SaveSettings()

	# Reconnect if Token changed
	if Settings["SocketToken"] != old_token:
		if EventReceiver and EventReceiver.IsConnected:
			EventReceiver.Disconnect()
		EventReceiver = None
		Connect()

	# Cleanup
	is_dirty = False
	diff = set(new_settings) ^ set(Settings)
	if len(diff) > 0:
		for k in diff:
			if k in new_settings:
				del new_settings[k]
				is_dirty = True
	Settings = new_settings

	if is_dirty:
		SaveSettings()


def SaveSettings():
	global Settings, SettingsFile

	with codecs.open(SettingsFile, encoding="utf-8-sig", mode="w") as f:
		json.dump(Settings, f, encoding="utf-8-sig", sort_keys=True, indent=4)
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
	CalculateStreak()
	UpdateTracker()


def SubtractSub():
	global Session
	if Session["CurrentSubs"] > 0:
		Session["CurrentSubs"] -= 1
		CalculateStreak()
		UpdateTracker()


# ----------------
# Streak Functions
# ----------------
def AddStreak():
	global Session
	Session["CurrentStreak"] += 1
	CalculateStreak()
	UpdateTracker()


def AddStreak5():
	global Session
	Session["CurrentStreak"] += 5
	CalculateStreak()
	UpdateTracker()


def AddStreak10():
	global Session
	Session["CurrentStreak"] += 10
	CalculateStreak()
	UpdateTracker()


def SubtractStreak():
	global Session
	if Session["CurrentStreak"] > 1:
		Session["CurrentStreak"] -= 1
		CalculateStreak()
		UpdateTracker()


def SubtractStreak5():
	global Session
	if Session["CurrentStreak"] > 1:
		Session["CurrentStreak"] -= 5
		CalculateStreak()
		UpdateTracker()


def SubtractStreak10():
	global Session
	if Session["CurrentStreak"] > 1:
		Session["CurrentStreak"] -= 10
		CalculateStreak()
		UpdateTracker()


# --------------
# Goal Functions
# --------------
def AddToGoal():
	global Session
	if Session["CurrentGoal"] < Settings["GoalMax"]:
		Session["CurrentGoal"] += 1
		CalculateStreak()
		UpdateTracker()


def SubtractFromGoal():
	global Session
	if Session["CurrentGoal"] > Settings["GoalMin"]:
		Session["CurrentGoal"] -= 1
		CalculateStreak()
		UpdateTracker()


# ------
# Unload
# ------
def Unload():
	global EventReceiver
	if EventReceiver and EventReceiver.IsConnected:
		EventReceiver.Disconnect()
	EventReceiver = None
	SaveSession()
	SaveText()


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
