# -------
# Imports
# -------
import codecs, json, math, os, time

# -----
# Paths
# -----
ScriptFolder       = os.path.realpath(os.path.dirname(__file__))
TextFolder         = os.path.join(ScriptFolder, "Text\\")

SessionFile        = os.path.join(ScriptFolder, "Session.json")
SettingsFile       = os.path.join(ScriptFolder, "Settings.json")

GoalFile           = os.path.join(TextFolder, "Goal.txt")
PointsFile         = os.path.join(TextFolder, "Points.txt")
PointsLeftFile     = os.path.join(TextFolder, "PointsLeft.txt")
StreakFile         = os.path.join(TextFolder, "Streak.txt")
TotalBitsFile      = os.path.join(TextFolder, "TotalBits.txt")
TotalSubsFile      = os.path.join(TextFolder, "TotalSubs.txt")
TotalDonationsFile = os.path.join(TextFolder, "TotalDonations.txt")

# ----------
# References
# ----------
import clr
clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(ScriptFolder, "Lib\\StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient


# -----------
# Script Info
# -----------
ScriptName  = "Twitch Streaker"
Website     = "https://github.com/BrainInBlack/TwitchStreaker"
Creator     = "BrainInBlack"
Version     = "2.6.1"
Description = "Tracker for new and gifted subscriptions with a streak mechanic."


# ----------------
# Global Variables
# ----------------
ChannelName   = None
EventReceiver = None
Session = {
	"CurrentGoal": 10,
	"CurrentPoints": 0,
	"CurrentPointsLeft": 10,
	"CurrentStreak": 1,
	"CurrentTotalSubs": 0,
	"CurrentTotalBits": 0,
	"CurrentTotalDonations": 0
}
Settings = {

	# General
	"Goal": 10,
	"GoalMin": 5,
	"GoalMax": 10,
	"GoalIncrement": 1,

	# Bits
	"BitsMinAmount": 500,
	"BitsPointValue": 1,
	"CountBits": False,
	"CountBitsOnce": False,
	"CountBitsCumulative": False,

	# Donations
	"DonationMinAmount": 5.0,
	"DonationPointValue": 1,
	"CountDonations": False,
	"CountDonationsOnce": False,
	"CountDonationsCumulative": False,

	# Subscriptions
	"CountReSubs": False,
	"Sub1": 1, "Sub2": 1, "Sub3": 1,
	"ReSub1": 1, "ReSub2": 1, "ReSub3": 1,
	"GiftSub1": 1, "GiftSub2": 1, "GiftSub3": 1,
	"GiftReSub1": 1, "GiftReSub2": 1, "GiftReSub3": 1,

	# Streamlabs
	"SocketToken": None
}


# ------------------
# Internal Variables
# ------------------
BitsTemp      = 0
DonationTemp  = 0.0
IsScriptReady = False
RefreshDelay  = 5    # InSeconds
RefreshStamp  = time.time()
SaveDelay     = 300  # InSeconds
SaveStamp     = time.time()
PointVars = [
	"Sub1", "Sub2", "Sub3",
	"ReSub1", "ReSub2", "ReSub3",
	"GiftSub1", "GiftSub2", "GiftSub3",
	"GiftReSub1", "GiftReSub2", "GiftReSub3",
	"BitsPointValue", "DonationsPointValue"
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

	StartUp()


# -------
# StartUp
# -------
def StartUp():
	global ChannelName, IsScriptReady, Settings

	IsScriptReady = False

	# Check Token
	if Settings["SocketToken"] is None or len(Settings["SocketToken"]) < 100:
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
	global BitsTemp, DonationTemp, ChannelName, Session, Settings

	data = args.Data

	# Twitch
	if data.For == "twitch_account":

		# ----
		# Bits
		# ----
		if data.Type == "bits" and Settings["CountBits"]:
			msg = data.Message[0]

			# Skip Repeat
			if msg.IsRepeat:
				Log("Ignored Repeat Bits by {}".format(msg.Name))
				return

			# Live Check, skip subs if streamer is not live (does not apply to test subscriptions)
			if not msg.IsLive and not msg.IsTest:
				Log("Ignored Bits, Stream is not Live")
				return

			# Ignore TestBits
			if not msg.IsTest:
				Session["CurrentTotalBits"] += msg.Amount

			# Bits are above MinAmount
			if msg.Amount > Settings["BitsMinAmount"]:

				if Settings["CountBitsOnce"]:
					Session["CurrentPoints"] += Settings["BitsPointValue"]
					Log("Added {} Point(s) for {} Bits from {}".format(Settings["BitsPointValue"], msg.Amount, msg.Name))
					return

				res = Settings["BitsPointValue"] * math.trunc(msg.Amount / Settings["BitsMinAmount"])
				BitsTemp += msg.Amount % Settings["BitsMinAmount"]  # Add remainder to BitsTemp

				if Settings["CountBitsCumulative"] and BitsTemp > Settings["BitsMinAmount"]:
					res += Settings["BitsPointValue"]
					BitsTemp -= Settings["BitsMinValue"]

				Session["CurrentPoints"] += res
				Log("Added {} Point(s) for {} Bits from {}".format(res, msg.Amount, msg.Name))
				return

			# Cumulative Donation
			elif Settings["CountBitsCumulative"]:

				BitsTemp += msg.Amount
				Log("Added {} Bit(s) from {} to the cumulative amount".format(msg.Amount, msg.Name))

				if BitsTemp > Settings["BitsMinAmount"]:

					Session["CurrentPoints"] += Settings["BitsPointValue"]
					DonationTemp             -= Settings["BitsMinAmount"]

					Log("Added {} Point(s), because the cumulative Bits amount exceeded the minimum Bits Amount.".format(Settings["BitsPointValue"]))
					return

			else:
				Log("Ignored {} Bits from {}, not above the Bits minimum.".format(msg.Amount, msg.Name))
			del msg
			return

		# -------------
		# Subscriptions
		# -------------
		if data.Type == "subscription":
			msg = data.Message[0]

			# Skip Repeat
			if msg.IsRepeat:
				Log("Ignored Repeat Subscription from {}".format(msg.Name))
				return

			# Live Check, skip subs if streamer is not live (does not apply to test subscriptions)
			if not msg.IsLive and not msg.IsTest:
				Log("Ignored Subscription from {}, Stream is not Live".format(msg.Name))
				return

			# GiftSub Check
			if msg.SubType == "subgift":

				# Ignore Gifted Subs by Streamer
				if msg.Gifter == ChannelName and not msg.IsTest:
					Log("Ignored StreamerGift from {}".format(msg.Gifter))
					return

				# Ignore Self-Gifted Subs
				if msg.Name == msg.Gifter and not msg.IsTest:
					Log("Ignored SelfGift from {}".format(msg.Gifter))
					return

			# ReSub Check, skip resubs if option is disabled
			if msg.SubType == "resub" and not Settings["CountReSubs"] and not msg.IsTest:
				Log("Ignored Resub by {}".format(msg.Name))
				return

			# Gifted Subs (includes anonymous subs)
			if msg.SubType == "subgift" or msg.SubType == "anonsubgift":

				# GiftedSubs (resubs)
				if msg.Months is not None:

					res = Settings["GiftReSub1"]

					if msg.SubPlan == "2000":
						res = Settings["GiftReSub2"]

					if msg.SubPlan == "3000":
						res = Settings["GiftReSub3"]

					Session["CurrentPoints"]    += res
					Session["CurrentTotalSubs"] += 1
					Log("Added {} Point(s) for a {} Subscription from {} to {}".format(res, msg.SubType, msg.Gifter, msg.Name))
					return
				# /GiftedSubs (resubs)

				# GiftedSubs (normal)
				else:

					res = Settings["GiftSub1"]

					if msg.SubPlan == "2000":
						res = Settings["GiftSub2"]

					if msg.SubPlan == "3000":
						res = Settings["GiftSub3"]

					Session["CurrentPoints"]    += res
					Session["CurrentTotalSubs"] += 1
					Log("Added {} Point(s) for a {} Subscription from {} to {}".format(res, msg.SubType, msg.Gifter, msg.Name))
					return
				# /GiftedSubs (normal)
			# GiftedSubs - END

			# ReSubs
			elif msg.SubType == "resub":

				res = Settings["ReSub1"]

				if msg.SubPlan == "2000":
					res = Settings["ReSub2"]

				if msg.SubPlan == "3000":
					res = Settings["ReSub3"]

				Session["CurrentPoints"]    += res
				Session["CurrentTotalSubs"] += 1
				Log("Added {} Point(s) for a {} Subscription from {}".format(res, msg.SubType, msg.Name))
				return
			# Resubs - END

			# Subs
			else:

				res = Settings["Sub1"]

				if msg.SubPlan == "2000":
					res = Settings["Sub2"]

				if msg.SubPlan == "3000":
					res = Settings["Sub3"]

				Session["CurrentPoints"]    += res
				Session["CurrentTotalSubs"] += 1
				Log("Added {} Point(s) for a {} Subscription from {}".format(res, msg.SubType, msg.Name))
				return
			# Subs - END

		return  # /Twitch

	# Mixer
	if data.For == "mixer_account":

		if data.Type == "subscription":
			msg = data.Message[0]

			# Skip Repeat
			if msg.IsRepeat:
				Log("Ignored Repeat Subscription from {} (Mixer)".format(msg.Name))
				return

			# Live Check, skip subs if streamer is not live (does not apply to test subscriptions)
			if not msg.IsLive and not msg.IsTest:
				Log("Ignored Subscription from {} (Mixer), Stream is not Live".format(msg.Name))
				return

			if msg.Months > 1 and not Settings["CountResubs"]:
				Log("Ignored Resub from {} (Mixer)".format(msg.Name))
				return

			Session["CurrentPoints"]    += Settings["Sub1"]
			Session["CurrentTotalSubs"] += 1
			Log("Added {} Point(s) by {} (Mixer)".format(Settings["Sub1"], msg.Name))
			return

		return  # /Mixer

	# Youtube
	if data.For == "youtube_account":

		if data.Type == "subscription":
			msg = data.Message[0]

			# Skip Repeat
			if msg.IsRepeat:
				Log("Ignored Repeat Sponsor from {} (YouTube)".format(msg.Name))
				return

			# Live Check, skip subs if streamer is not live (does not apply to test subscriptions)
			if not msg.IsLive and not msg.IsTest:
				Log("Ignored Sponsor from {}, Stream is not Live. (YouTube)".format(msg.Name))
				return

			if msg.Months > 1 and not Settings["CountResubs"]:
				Log("Ignored Re-Sponsor from {}. (YouTube)".format(msg.Name))
				return

			Session["CurrentPoints"]    += Settings["Sub1"]
			Session["CurrentTotalSubs"] += 1
			Log("Added {} Point(s) for a Sponsorship from {} (YouTube)".format(Settings["Sub1"], msg.Name))
			return

		return  # /Youtube

	# Streamlabs
	if data.For == "streamlabs":

		if data.Type == "donation" and Settings["CountDonations"]:
			msg = data.Message[0]

			# Skip Repeat
			if msg.IsRepeat:
				Log("Ignored Repeat Donation from {}".format(msg.FromName))
				return

			# Live Check, skip subs if streamer is not live (does not apply to test donations)
			if not msg.IsLive and not msg.IsTest:
				Log("Ignored Donation from {}, Stream is not Live.".format(msg.Name))
				return

			# Ignore test donations for the total amount
			if not msg.IsTest:
				Session["CurrentTotalDonations"] += msg.Amount

			# Donation is above MinAmount
			if msg.Amount > Settings["DonationMinAmount"]:

				if Settings["CountDonationsOnce"]:
					Session["CurrentPoints"] += Settings["DonationsPointValue"]
					Log("Added {} Point(s) for a {} {} Donation from {}.".format(Settings["DonationsPointValue"], msg.Amount, msg.Currency, msg.FromName))
					return

				res = Settings["DonationPointValue"] * math.trunc(msg.Amount / Settings["DonationMinAmount"])
				DonationTemp += msg.Amount % Settings["DonationMinAmount"]  # Add remainder to DonationTemp

				if Settings["CountDonationsCumulative"] and DonationTemp > Settings["DonationMinAmount"]:
					res += Settings["DonationPointValue"]
					DonationTemp -= Settings["DonationMinAmount"]

				Session["CurrentPoints"] += res
				Log("Added {} Point(s) for a {} {} Donation from {}.".format(res, msg.Amount, msg.Currency, msg.FromName))
				return

			# Cumulative Donation
			elif Settings["CountDonationsCumulative"]:

				DonationTemp += msg.Amount
				Log("Added Donation of {} {} from {} to the cumulative amount.".format(msg.Amount, msg.Currency, msg.FromName))

				if DonationTemp > Settings["DonationMinAmount"]:

					Session["CurrentPoints"] += Settings["DonationPointValue"]
					DonationTemp             -= Settings["DonationMinAmount"]

					Log("Added {} Point(s) because the cumulative Donation amount exceeded the minimum donation amount.".format(Settings["DonationPointValue"]))
					return

			else:
				Log("Ignored Donation of {} {} from {}, Donation is not above the Donation minimum.".format(msg.Amount, msg.Currency, msg.FromName))
				return

		return  # /Streamlabs

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


# ----
# Tick
# ----
def Tick():
	global EventReceiver, IsScriptReady, RefreshDelay, RefreshStamp, SaveDelay, SaveStamp

	# Fast Timer
	if (time.time() - RefreshStamp) > RefreshDelay:

		# Attempt Startup
		if not IsScriptReady:
			StartUp()

		# Reconnect
		if EventReceiver is None or not EventReceiver.IsConnected:
			Connect()

		# Update Everything
		UpdateTracker()

	# Slow Timer
	if (time.time() - SaveStamp) > SaveDelay:
		SaveSession()
		SaveStamp = time.time()


# --------------
# Update Tracker
# --------------
def UpdateTracker():  # ! Only call if a quick response is required
	global Session, Settings, RefreshStamp, GoalFile, PointsFile, StreakFile, PointsLeftFile, TotalSubsFile, TotalBitsFile, TotalDonationsFile

	# Calculate Streak
	Session["CurrentPointsLeft"] = Session["CurrentGoal"] - Session["CurrentPoints"]

	while Session["CurrentPoints"] >= Session["CurrentGoal"]:

		# Subtract Goal and Increment Streak
		Session["CurrentPoints"] -= Session["CurrentGoal"]
		Session["CurrentStreak"] += 1

		# Increment CurrentGoal
		if Session["CurrentGoal"]   < Settings["GoalMax"]:
			Session["CurrentGoal"] += Settings["GoalIncrement"]

			# Correct Goal if GoalIncrement is bigger than the gap from CurrentGoal to GoalMax
			if Session["CurrentGoal"]  > Settings["GoalMax"]:
				Session["CurrentGoal"] = Settings["GoalMax"]

	# Update Overlay
	Parent.BroadcastWsEvent("EVENT_UPDATE_OVERLAY", str(json.JSONEncoder().encode(Session)))

	# Update Text Files
	if not os.path.isdir(TextFolder):
		os.mkdir(TextFolder)

	try:
		f = open(GoalFile, "w")
		f.write(str(Session["CurrentGoal"]))
		f.close()

		f = open(PointsFile, "w")
		f.write(str(Session["CurrentPoints"]))
		f.close()

		f = open(PointsLeftFile, "w")
		f.write(str(Session["CurrentPointsLeft"]))
		f.close()

		f = open(StreakFile, "w")
		f.write(str(Session["CurrentStreak"]))
		f.close()

		f = open(TotalSubsFile, "w")
		f.write(str(Session["CurrentTotalSubs"]))
		f.close()

		f = open(TotalBitsFile, "w")
		f.write(str(Session["CurrentTotalBits"]))
		f.close()

		f = open(TotalDonationsFile, "w")
		f.write(str(Session["CurrentTotalDonations"]))
		f.close()
	except IOError as e:
		Log("Unable to update Text Files! ({})".format(e.message))

	# Update Refresh Stamp
	RefreshStamp = time.time()


# ------------
# Sanity Check
# ------------
def SanityCheck():
	global Session, Settings, PointVars

	is_session_dirty  = False
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

	# Prevent Points from being below 1
	for var in PointVars:
		if var < 1:
			Settings[var]     = 1
			is_settings_dirty = True

	# Prevent GoalIncrement from being less than 0
	if Settings["GoalIncrement"]  < 0:
		Settings["GoalIncrement"] = 0
		is_settings_dirty         = True

	# Prevent Totals from being less than 0
	if Session["CurrentTotalSubs"]  < 0:
		Session["CurrentTotalSubs"] = 0
		is_session_dirty            = True

	if Session["CurrentTotalBits"]  < 0:
		Session["CurrentTotalBits"] = 0
		is_session_dirty            = True

	if Session["CurrentTotalDonations"]  < 0:
		Session["CurrentTotalDonations"] = 0
		is_session_dirty                 = True

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

	# Make sure Settings are loaded
	if Settings is None:
		LoadSettings()
		SanityCheck()

	try:
		with codecs.open(SessionFile, encoding="utf-8-sig", mode="r") as f:
			new_session = json.load(f, encoding="utf-8-sig")
			f.close()
	except IOError:
		SaveSession()  # Save default Session
		return

	# Cleanup old session
	is_dirty = False
	diff = set(new_session) ^ set(Session)  # List options no longer present in the session
	if len(diff) > 0:
		for k in diff:
			if k in new_session:
				del new_session[k]
				is_dirty = True
	Session = new_session

	if is_dirty:
		SaveSession()


def SaveSession():
	global Session, SessionFile

	try:
		with codecs.open(SessionFile, encoding="utf-8-sig", mode="w") as f:
			json.dump(Session, f, encoding="utf-8-sig", sort_keys=True, indent=4)
			f.close()
	except IOError as e:
		Log("Unable to save Session! ({})".format(e.message))


def ResetSession():
	global Session, Settings

	if Settings is None:
		LoadSettings()
		SanityCheck()

	# Hard reset of the session
	del Session
	Session = {
		"CurrentGoal": Settings["Goal"],
		"CurrentPoints": 0,
		"CurrentPointsLeft": Settings["Goal"],
		"CurrentStreak": 1,
		"CurrentTotalSubs": 0,
		"CurrentTotalBits": 0,
		"CurrentTotalDonations": 0
	}

	SaveSession()
	UpdateTracker()
	Log("Session Reset!")


# ------------------
# Settings Functions
# ------------------
def LoadSettings():
	global EventReceiver, Settings, SettingsFile

	# Backup old token for comparison
	old_token = Settings["SocketToken"]

	try:
		with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as f:
			new_settings = json.load(f, encoding="utf-8-sig")
			f.close()
	except IOError:
		SaveSettings()  # Save default Settings
		return

	# Cleanup old options
	is_dirty = False
	diff = set(new_settings) ^ set(Settings)  # List options no longer present in the default settings
	if len(diff) > 0:
		for k in diff:
			if k in new_settings:
				del new_settings[k]
				is_dirty = True
	Settings = new_settings

	# Reconnect if Token changed
	if old_token and Settings["SocketToken"] != old_token:
		if EventReceiver:
			if EventReceiver.IsConnected: EventReceiver.Disconnect()
			EventReceiver = None
		Connect()

	if is_dirty:
		SaveSettings()


def SaveSettings():
	global Settings, SettingsFile

	try:
		with codecs.open(SettingsFile, encoding="utf-8-sig", mode="w") as f:
			json.dump(Settings, f, encoding="utf-8-sig", sort_keys=True, indent=4)
			f.close()
	except IOError as e:
		Log("Unable to save Settings! ({})".format(e.message))


def ReloadSettings(json_data):
	global EventReceiver, Settings

	# Backup old token for comparison
	old_token = Settings["SocketToken"]

	try:
		with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as f:
			Settings = json.load(f, encoding="utf-8-sig")
			f.close()
	except IOError:
		SaveSettings()  # Save default Settings
		return

	# Reconnect if Token changed
	if old_token is not None and Settings["SocketToken"] != old_token:
		if EventReceiver:
			if EventReceiver.IsConnected: EventReceiver.Disconnect()
			EventReceiver = None
		Connect()

	SanityCheck()
	Log("Settings saved!")


# -------------
# Sub Functions
# -------------
def AddPoint():
	global Session
	Session["CurrentPoints"] += 1


def SubtractPoint():
	global Session
	if Session["CurrentPoints"]   > 0:
		Session["CurrentPoints"] -= 1


# ----------------
# Streak Functions
# ----------------
def AddStreak():
	global Session
	Session["CurrentStreak"] += 1


def AddStreak5():
	global Session
	Session["CurrentStreak"] += 5


def AddStreak10():
	global Session
	Session["CurrentStreak"] += 10


def SubtractStreak():
	global Session
	if Session["CurrentStreak"]   > 1:
		Session["CurrentStreak"] -= 1


def SubtractStreak5():
	global Session
	if Session["CurrentStreak"]   > 1:
		Session["CurrentStreak"] -= 5


def SubtractStreak10():
	global Session
	if Session["CurrentStreak"]   > 1:
		Session["CurrentStreak"] -= 10


# --------------
# Goal Functions
# --------------
def AddToGoal():
	global Session
	if Session["CurrentGoal"]   < Settings["GoalMax"]:
		Session["CurrentGoal"] += 1


def SubtractFromGoal():
	global Session
	if Session["CurrentGoal"]   > Settings["GoalMin"]:
		Session["CurrentGoal"] -= 1


# ------
# Unload
# ------
def Unload():
	global EventReceiver
	if EventReceiver and EventReceiver.IsConnected:
		EventReceiver.Disconnect()
	EventReceiver = None
	UpdateTracker()
	SaveSession()


# ---------------
# Parse Parameter
# ---------------
def Parse(parse_string, user_id, username, target_id, target_name, message):
	global Session

	if "$tsGoal" in parse_string:
		parse_string = parse_string.replace("$tsGoal", str(Session["CurrentGoal"]))

	if "$tsStreak" in parse_string:
		parse_string = parse_string.replace("$tsStreak", str(Session["CurrentStreak"]))

	if "$tsPoints" in parse_string:
		parse_string = parse_string.replace("$tsPoints", str(Session["CurrentPoints"]))

	if "$tsPointsLeft" in parse_string:
		parse_string = parse_string.replace("$tsPointsLeft", str(Session["CurrentPointsLeft"]))

	if "$tsTotalSubs" in parse_string:
		parse_string = parse_string.replace("$tsTotalSubs", str(Session["CurrentTotalSubs"]))

	if "$tsTotalBits" in parse_string:
		parse_string = parse_string.replace("$tsTotalBits", str(Session["CurrentTotalBits"]))

	if "$tsTotalDonations" in parse_string:
		parse_string = parse_string.replace("$tsTotalDonations", str(Session["CurrentTotalDonations"]))

	return parse_string


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
