# -------
# Imports
# -------
import codecs, json, math, os, time

# -----
# Paths
# -----
SCRIPT_FOLDER        = os.path.realpath(os.path.dirname(__file__))
TEXT_FOLDER          = os.path.join(SCRIPT_FOLDER, "Text\\")

LOG_FILE             = os.path.join(SCRIPT_FOLDER, "TwitchStreaker.log")
SESSION_FILE         = os.path.join(SCRIPT_FOLDER, "Session.json")
SETTINGS_FILE        = os.path.join(SCRIPT_FOLDER, "Settings.json")

BITS_LEFT_FILE       = os.path.join(TEXT_FOLDER, "BitsLeft.txt")
GOAL_FILE            = os.path.join(TEXT_FOLDER, "Goal.txt")
POINTS_FILE          = os.path.join(TEXT_FOLDER, "Points.txt")
POINTS_LEFT_FILE     = os.path.join(TEXT_FOLDER, "PointsLeft.txt")
STREAK_FILE          = os.path.join(TEXT_FOLDER, "Streak.txt")
TOTAL_BITS_FILE      = os.path.join(TEXT_FOLDER, "TotalBits.txt")
TOTAL_SUBS_FILE      = os.path.join(TEXT_FOLDER, "TotalSubs.txt")
TOTAL_DONATIONS_FILE = os.path.join(TEXT_FOLDER, "TotalDonations.txt")

# ----------
# References
# ----------
import clr
clr.AddReferenceToFileAndPath(os.path.join(SCRIPT_FOLDER, "Lib\\StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient


# -----------
# Script Info
# -----------
ScriptName  = "Twitch Streaker"
Website     = "https://github.com/BrainInBlack/TwitchStreaker"
Creator     = "BrainInBlack"
Version     = "2.8.1"
Description = "Tracker for new and gifted subscriptions with a streak mechanic."


# -------------
# Session Class
# -------------
class ScriptSession(object):

	CurrentBitsLeft       = 0
	CurrentGoal           = 10
	CurrentPoints         = 0
	CurrentPointsLeft     = 10
	CurrentStreak         = 1
	CurrentTotalSubs      = 0
	CurrentTotalBits      = 0
	CurrentTotalDonations = 0

	def __init__(self):
		self.__dict__ = self.DefaultSession()
		self.Load()

	def Load(self):
		try:
			with codecs.open(SESSION_FILE, encoding="utf-8-sig", mode="r") as f:
				_new = json.load(f, encoding="utf-8-sig")
				f.close()
		except:
			self.Save()
			return

		# Cleanup
		_dirty = False
		diff = set(_new) ^ set(self.__dict__)
		if len(diff) > 0:
			for k in diff:
				if k in _new:
					del _new[k]
					_dirty = True
		self.__dict__ = _new
		if _dirty: self.Save()

	def Save(self):
		try:
			with codecs.open(SESSION_FILE, encoding="utf-8-sig", mode="w") as f:
				json.dump(self.__dict__, f, encoding="utf-8-sig", sort_keys=True, indent=4)
				f.close()
		except IOError as e:
			raise Exception("Unable to save Session ({})".format(e.message))
		except:
			raise Exception("Unable to save Session (Unknown Error)")

	@staticmethod
	def DefaultSession():
		return {
			"CurrentBitsLeft": 0,
			"CurrentGoal": 10,
			"CurrentPoints": 0,
			"CurrentPointsLeft": 10,
			"CurrentStreak": 1,
			"CurrentTotalSubs": 0,
			"CurrentTotalBits": 0,
			"CurrentTotalDonations": 0
		}


# --------------
# Settings Class
# --------------
class ScriptSettings(object):

	# General
	Goal = 10
	GoalMin = 5
	GoalMax = 10
	GoalIncrement = 1

	# Bits
	BitsMinAmount = 500
	BitsPointValue = 1
	CountBits = False
	CountBitsOnce = False
	CountBitsCumulative = False

	# Donations
	DonationMinAmount = 5.0
	DonationPointValue = 1
	CountDonations = False
	CountDonationsOnce = False
	CountDonationsCumulative = False

	# Subscriptions
	CountReSubs = False
	Sub1 = 1
	Sub2 = 1
	Sub3 = 1
	ReSub1 = 1
	ReSub2 = 1
	ReSub3 = 1
	GiftSub1 = 1
	GiftSub2 = 1
	GiftSub3 = 1
	GiftReSub1 = 1
	GiftReSub2 = 1
	GiftReSub3 = 1

	# Streamlabs
	SocketToken = None

	def __init__(self):
		self.__dict__ = self.DefaultSettings()
		self.Load()

	def Load(self):
		try:
			with codecs.open(SETTINGS_FILE, encoding="utf-8-sig", mode="r") as f:
				_new = json.load(f, encoding="utf-8-sig")
				f.close()
		except:
			self.Save()
			return

		# Cleanup
		_dirty = False
		diff = set(_new) ^ set(self.__dict__)
		if len(diff) > 0:
			for k in diff:
				if k in _new:
					del _new[k]
					_dirty = True
		self.__dict__ = _new
		if _dirty: self.Save()

	def Save(self):
		try:
			with codecs.open(SETTINGS_FILE, encoding="utf-8-sig", mode="w") as f:
				json.dump(self.__dict__, f, encoding="utf-8-sig", sort_keys=True, indent=4)
				f.close()
		except IOError as e:
			raise Exception("Unable to save Settings ({})".format(e.message))
		except:
			raise Exception("Unable to save Settings (Unknown error)")

	@staticmethod
	def DefaultSettings():
		return {
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


# ----------------
# Global Variables
# ----------------
ChannelName   = None
EventReceiver = None
Session       = None
Settings      = None


# ------------------
# Internal Variables
# ------------------
BitsTemp      = 0
DonationTemp  = 0.0
IsScriptReady = False
RefreshStamp  = time.time()
SaveStamp     = time.time()
FlushStamp    = time.time()
EventIDs      = []


# ---------
# Constants
# ---------
FLUSH_DELAY   = 5    # InSeconds
REFRESH_DELAY = 5    # InSeconds
SAVE_DELAY    = 300  # InSeconds
POINT_VARS    = [
	"Sub1", "Sub2", "Sub3",
	"ReSub1", "ReSub2", "ReSub3",
	"GiftSub1", "GiftSub2", "GiftSub3",
	"GiftReSub1", "GiftReSub2", "GiftReSub3",
	"BitsPointValue", "DonationsPointValue"
]
PARSE_PARAMETERS = {
	"$tsBitsLeft":       "CurrentBitsLeft",
	"$tsGoal":           "CurrentGoal",
	"$tsStreak":         "CurrentStreak",
	"$tsPoints":         "CurrentPoints",
	"$tsPointsLeft":     "CurrentPointsLeft",
	"$tsTotalSubs":      "CurrentTotalSubs",
	"$tsTotalBits":      "CurrentTotalBits",
	"$tsTotalDonations": "CurrentTotalDonations"
}


# ----------
# Initiation
# ----------
def Init():
	global Session, Settings
	Session  = ScriptSession()
	Settings = ScriptSettings()
	SanityCheck()
	StartUp()


# -------
# StartUp
# -------
def StartUp():
	global ChannelName, IsScriptReady

	IsScriptReady = False

	# Check Token
	if Settings.SocketToken is None or len(Settings.SocketToken) < 50:
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
	global EventReceiver

	EventReceiver = StreamlabsEventClient()
	EventReceiver.StreamlabsSocketConnected    += EventReceiverConnected
	EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
	EventReceiver.StreamlabsSocketEvent        += EventReceiverEvent
	EventReceiver.Connect(Settings.SocketToken)


# ---------
# Event Bus
# ---------
def EventReceiverEvent(sender, args):
	global BitsTemp, DonationTemp, EventIDs, FlushStamp

	# Get Data
	dat = args.Data
	msg = dat.Message[0]

	# Event Filtering
	FlushStamp = time.time()
	if msg.Id in EventIDs: return
	EventIDs.append(msg.Id)

	# Skip on Repeat and NotLive
	if msg.IsRepeat: return
	if not msg.IsLive and not msg.IsTest: return

	# Twitch
	if dat.For == "twitch_account":

		# ----
		# Bits
		# ----
		if dat.Type == "bits" and Settings.CountBits:

			# Ignore TestBits
			if not msg.IsTest:
				Session.CurrentTotalBits += msg.Amount

			# Bits are above MinAmount
			if msg.Amount >= Settings.BitsMinAmount:

				if Settings.CountBitsOnce:
					Session.CurrentPoints += Settings.BitsPointValue
					Log("Added {} Point(s) for {} Bits from {}".format(Settings.BitsPointValue, msg.Amount, msg.Name))
					return

				res = Settings.BitsPointValue * math.trunc(msg.Amount / Settings.BitsMinAmount)
				BitsTemp += msg.Amount % Settings.BitsMinAmount  # Add remainder to BitsTemp

				Session.CurrentPoints += res
				Log("Added {} Point(s) for {} Bits from {}".format(res, msg.Amount, msg.Name))
				return

			# Cumulative Bits
			elif Settings.CountBitsCumulative:

				BitsTemp += msg.Amount
				Log("Added {} Bit(s) from {} to the cumulative amount".format(msg.Amount, msg.Name))

			else:
				Log("Ignored {} Bits from {}, not above the Bits minimum.".format(msg.Amount, msg.Name))
			return

		# -------------
		# Subscriptions
		# -------------
		if dat.Type == "subscription":

			# GiftSub Check
			if msg.SubType == "subgift":

				# Ignore Gifted Subs by Streamer
				if msg.Gifter == ChannelName and not msg.IsTest: return

				# Ignore Self-Gifted Subs
				if msg.Name == msg.Gifter and not msg.IsTest: return

			# Gifted Subs (includes anonymous subs)
			if msg.SubType == "subgift" or msg.SubType == "anonsubgift":

				# GiftedSubs (resubs)
				if msg.Months is not None:

					res = Settings.GiftReSub1

					if msg.SubPlan == "2000":
						res = Settings.GiftReSub2

					if msg.SubPlan == "3000":
						res = Settings.GiftReSub3

					Session.CurrentPoints    += res
					Session.CurrentTotalSubs += 1
					Log("Added {} Point(s) for a {} Subscription from {} to {}".format(res, msg.SubType, msg.Gifter, msg.Name))
					return
				# /GiftedSubs (resubs)

				# GiftedSubs (normal)
				else:

					res = Settings.GiftSub1

					if msg.SubPlan == "2000":
						res = Settings.GiftSub2

					if msg.SubPlan == "3000":
						res = Settings.GiftSub3

					Session.CurrentPoints    += res
					Session.CurrentTotalSubs += 1
					Log("Added {} Point(s) for a {} Subscription from {} to {}".format(res, msg.SubType, msg.Gifter, msg.Name))
					return
				# /GiftedSubs (normal)
			# GiftedSubs - END

			# ReSubs
			elif msg.SubType == "resub":

				# Skip resubs if option is disabled
				if not Settings.CountReSubs and not msg.IsTest: return

				res = Settings.ReSub1

				if msg.SubPlan == "2000":
					res = Settings.ReSub2

				if msg.SubPlan == "3000":
					res = Settings.ReSub3

				Session.CurrentPoints    += res
				Session.CurrentTotalSubs += 1
				Log("Added {} Point(s) for a {} Subscription from {}".format(res, msg.SubType, msg.Name))
				return
			# Resubs - END

			# Subs
			else:

				res = Settings.Sub1

				if msg.SubPlan == "2000":
					res = Settings.Sub2

				if msg.SubPlan == "3000":
					res = Settings.Sub3

				Session.CurrentPoints    += res
				Session.CurrentTotalSubs += 1
				Log("Added {} Point(s) for a {} Subscription from {}".format(res, msg.SubType, msg.Name))
				return
			# Subs - END

		return  # /Twitch

	# Youtube
	if dat.For == "youtube_account":

		if dat.Type == "subscription":

			if msg.Months > 1 and not Settings.CountResubs: return

			Session.CurrentPoints    += Settings.Sub1
			Session.CurrentTotalSubs += 1
			Log("Added {} Point(s) for a Sponsorship from {} (YouTube)".format(Settings.Sub1, msg.Name))
			return

		if dat.Type == 'superchat':

			if not msg.IsTest: Session.CurrentTotalDonations += msg.Amount

			if msg.Amount >= Settings.DonationMinAmount:

				if Settings.CountDonationsOnce:
					Session.CurrentPoints += Settings.DonationPointValue
					Log("Added {} Point(s) for a {} {} Superchat from {}".format(Settings.DonationPointValue, msg.Amount, msg.Currency, msg.Name))
					return

				res = Settings.DonationPointValue * math.trunc(msg.Amount / Settings.DonationMinAmount)
				DonationTemp += msg.Amount % Settings.DonationMinAmount  # Add remainder to DonationTemp

				Session.CurrentPoints += res
				Log("Added {} Point(s) for a {} {} Superchat from {}".format(res, msg.Amount, msg.Currency, msg.Name))
				return

			elif Settings.CountDonationsCumulative:

				DonationTemp += msg.Amount
				Log("Added Superchat of {} {} from {} to the cumulative Amount.".format())
				return

			else:
				Log("Ignored Superchat of {} {} from {}, Donation is not above the Donation minimum.".format(msg.Amount, msg.Currency, msg.Name))
				return

		return  # /Youtube

	# Streamlabs
	if dat.For == "streamlabs":

		if dat.Type == "donation" and Settings.CountDonations:

			# Ignore test donations for the total amount
			if not msg.IsTest: Session.CurrentTotalDonations += msg.Amount

			# Donation is above MinAmount
			if msg.Amount >= Settings.DonationMinAmount:

				if Settings.CountDonationsOnce:
					Session.CurrentPoints += Settings.DonationPointValue
					Log("Added {} Point(s) for a {} {} Donation from {}.".format(Settings.DonationPointValue, msg.Amount, msg.Currency, msg.FromName))
					return

				res = Settings.DonationPointValue * math.trunc(msg.Amount / Settings.DonationMinAmount)
				DonationTemp += msg.Amount % Settings.DonationMinAmount  # Add remainder to DonationTemp

				Session.CurrentPoints += res
				Log("Added {} Point(s) for a {} {} Donation from {}.".format(res, msg.Amount, msg.Currency, msg.FromName))
				return

			# Cumulative Donation
			elif Settings.CountDonationsCumulative:

				DonationTemp += msg.Amount
				Log("Added Donation of {} {} from {} to the cumulative Amount.".format(msg.Amount, msg.Currency, msg.FromName))
				return

			else:
				Log("Ignored Donation of {} {} from {}, Donation is not above the Donation minimum.".format(msg.Amount, msg.Currency, msg.FromName))
				return

		return  # /Streamlabs

	Log("Unknown/Unsupported Platform {}!".format(dat.For))


# ---------------
# Event Connected
# ---------------
def EventReceiverConnected(sender, args): Log("Connected")


# ------------------
# Event Disconnected
# ------------------
def EventReceiverDisconnected(sender, args): Log("Disconnected")


# ----
# Tick
# ----
def Tick():
	global EventIDs, FlushStamp, SaveStamp

	now = time.time()

	# Event Filter Flush
	if(now - FlushStamp) > FLUSH_DELAY and len(EventIDs) > 0:
		EventIDs = []
		FlushStamp = now

	# Fast Timer
	if (now - RefreshStamp) > REFRESH_DELAY:

		# Attempt Startup
		if not IsScriptReady:
			StartUp()

		# Reconnect
		if EventReceiver is None or not EventReceiver.IsConnected:
			Connect()
			return

		UpdateTracker()
		# RefreshStamp = now  # ! updated by UpdateTracker

	# Save Timer
	if (now - SaveStamp) > SAVE_DELAY:
		if not IsScriptReady: return
		Session.Save()
		SaveStamp = now


# --------------
# Update Tracker
# --------------
def UpdateTracker():  # ! Only call if a quick response is required
	global BitsTemp, DonationTemp, RefreshStamp

	# Calculate Bits
	if Settings.CountBitsCumulative and BitsTemp >= Settings.BitsMinAmount:
		res = math.trunc(BitsTemp / Settings.BitsMinAmount)
		Session.CurrentPoints += Settings.BitsPointValue * res
		BitsTemp -= Settings.BitsMinAmount * res
		Log("Added {} Point(s), because the cumulative Bits amount exceeded the minimum Bits Amount.".format(Settings.BitsPointValue * res))
		del res
	Session.CurrentBitsLeft = Settings.BitsMinAmount - BitsTemp

	# Calculate Donations
	if Settings.CountDonationsCumulative and DonationTemp >= Settings.DonationMinAmount:
		res = math.trunc(DonationTemp / Settings.DonationMinAmount)
		Session.CurrentPoints += Settings.DonationPointValue
		DonationTemp -= Settings.DonationMinAmount * res
		Log("Added {} Point(s) because the cumulative Donation amount exceeded the minimum donation amount.".format(Settings.DonationPointValue * res))
		del res

	# Calculate Streak
	while Session.CurrentPoints >= Session.CurrentGoal:

		# Subtract Goal and Increment Streak
		Session.CurrentPoints -= Session.CurrentGoal
		Session.CurrentStreak += 1

		# Increment CurrentGoal
		if Session.CurrentGoal   < Settings.GoalMax:
			Session.CurrentGoal += Settings.GoalIncrement

			# Correct Goal if GoalIncrement is bigger than the gap from CurrentGoal to GoalMax
			if Session.CurrentGoal  > Settings.GoalMax:
				Session.CurrentGoal = Settings.GoalMax
	Session.CurrentPointsLeft = Session.CurrentGoal - Session.CurrentPoints

	# Update Overlay
	Parent.BroadcastWsEvent("EVENT_UPDATE_OVERLAY", str(json.dumps(Session.__dict__)))

	# Update Text Files
	if not os.path.isdir(TEXT_FOLDER): os.mkdir(TEXT_FOLDER)

	SimpleWrite(BITS_LEFT_FILE,       Session.CurrentBitsLeft)
	SimpleWrite(GOAL_FILE,            Session.CurrentGoal)
	SimpleWrite(POINTS_FILE,          Session.CurrentPoints)
	SimpleWrite(POINTS_LEFT_FILE,     Session.CurrentPointsLeft)
	SimpleWrite(STREAK_FILE,          Session.CurrentStreak)
	SimpleWrite(TOTAL_SUBS_FILE,      Session.CurrentTotalSubs)
	SimpleWrite(TOTAL_BITS_FILE,      Session.CurrentTotalBits)
	SimpleWrite(TOTAL_DONATIONS_FILE, Session.CurrentTotalDonations)

	# Update Refresh Stamp
	RefreshStamp = time.time()


# ------------
# Sanity Check
# ------------
def SanityCheck():

	is_session_dirty  = False
	is_settings_dirty = False

	# Prevent GoalMin from being Zero
	if Settings.GoalMin   < 1:
		Settings.GoalMin  = 1
		is_settings_dirty = True

	# Prevent GoalMin from being higher than the Goal
	if Settings.GoalMin   > Settings.Goal:
		Settings.GoalMin  = Settings.Goal
		is_settings_dirty = True

	# Prevent GoalMax from being lower than the Goal
	if Settings.GoalMax   < Settings.Goal:
		Settings.GoalMax  = Settings.Goal
		is_settings_dirty = True

	# Prevent CurrentGoal from being lower than GoalMin
	if Session.CurrentGoal  < Settings.GoalMin:
		Session.CurrentGoal = Settings.GoalMin
		is_session_dirty    = True

	# Prevent CurrentGoal from being higher than GoalMax
	if Session.CurrentGoal  > Settings.GoalMax:
		Session.CurrentGoal = Settings.GoalMax
		is_session_dirty    = True

	# Prevent CurrentPointsLeft de-sync
	if Session.CurrentGoal != (Session.CurrentPointsLeft + Session.CurrentPoints):
		Session.CurrentPointsLeft = Session.CurrentGoal - Session.CurrentPoints
		is_session_dirty = True

	# Prevent Points from being below 1
	for var in POINT_VARS:
		if var < 1:
			Settings[var]     = 1
			is_settings_dirty = True

	# Prevent GoalIncrement from being less than 0
	if Settings.GoalIncrement  < 0:
		Settings.GoalIncrement = 0
		is_settings_dirty      = True

	# Prevent Totals from being less than 0
	if Session.CurrentTotalSubs  < 0:
		Session.CurrentTotalSubs = 0
		is_session_dirty         = True

	if Session.CurrentTotalBits  < 0:
		Session.CurrentTotalBits = 0
		is_session_dirty         = True

	if Session.CurrentTotalDonations  < 0:
		Session.CurrentTotalDonations = 0
		is_session_dirty              = True

	# Save Session/Settings if dirty
	if is_session_dirty:  Session.Save()
	if is_settings_dirty: Settings.Save()


# -----------------
# Session Functions
# -----------------
def ResetSession():
	Session.__dict__          = Session.DefaultSession()
	Session.CurrentBitsLeft   = Settings.BitsMinAmount
	Session.CurrentGoal       = Settings.Goal
	Session.CurrentPointsLeft = Settings.Goal

	SanityCheck()
	UpdateTracker()
	Log("Session Reset!")


# ------------------
# Settings Functions
# ------------------
def ReloadSettings(json_data):  # Triggered by the bot on Save Settings
	global EventReceiver, IsScriptReady

	# Backup old token for comparison
	old_token = Settings.SocketToken
	Settings.Load()

	# Reconnect if Token changed
	if old_token is None or Settings.SocketToken != old_token:
		if EventReceiver:
			if EventReceiver.IsConnected: EventReceiver.Disconnect()
			EventReceiver = None
		Connect()
		if not IsScriptReady: IsScriptReady = True

	SanityCheck()
	Log("Settings saved!")


# -------------
# Sub Functions
# -------------
def AddPoint():
	Session.CurrentPoints += 1


def SubtractPoint():
	if Session.CurrentPoints   > 0:
		Session.CurrentPoints -= 1


# ----------------
# Streak Functions
# ----------------
def AddStreak():
	Session.CurrentStreak += 1


def AddStreak5():
	Session.CurrentStreak += 5


def AddStreak10():
	Session.CurrentStreak += 10


def SubtractStreak():
	if Session.CurrentStreak   > 1:
		Session.CurrentStreak -= 1


def SubtractStreak5():
	if Session.CurrentStreak   > 1:
		Session.CurrentStreak -= 5


def SubtractStreak10():
	if Session.CurrentStreak   > 1:
		Session.CurrentStreak -= 10


# --------------
# Goal Functions
# --------------
def AddToGoal():
	if Session.CurrentGoal   < Settings.GoalMax:
		Session.CurrentGoal += 1


def SubtractFromGoal():
	if Session.CurrentGoal   > Settings.GoalMin:
		Session.CurrentGoal -= 1


# ------
# Unload
# ------
def Unload():
	global EventReceiver, IsScriptReady
	if EventReceiver and EventReceiver.IsConnected:
		EventReceiver.Disconnect()
	EventReceiver = None
	IsScriptReady = False
	UpdateTracker()
	Session.Save()


# ---------------
# Parse Parameter
# ---------------
def Parse(parse_string, user_id, username, target_id, target_name, message):
	for key in PARSE_PARAMETERS:
		if key in parse_string:
			parse_string = parse_string.replace(key, getattr(Session, PARSE_PARAMETERS[key]))
			pass
	return parse_string


# -------
# Execute
# -------
def Execute(data):
	pass


# -----------
# Log Wrapper
# -----------
def Log(message):
	try:
		# Open/Create logfile and write the log-message
		with codecs.open(LOG_FILE, encoding="utf-8", mode="a+") as f:
			f.write("{} - {}\n".format(time.strftime("%m/%d/%y - %H:%M:%S"), message))
			f.close()
	except IOError as e:
		# Dump to bot-console if write failed
		Parent.Log(ScriptName, "Unable to open or write to logfile. ({})".format(e.message))

	Parent.Log(ScriptName, message)


# ------------
# Simple Write
# ------------
def SimpleWrite(path, content):
	try:
		f = open(path, "w")
		f.write(str(content))
		f.close()
	except IOError as e:
		Log("Unable to write file \"{}\" ({})".format(path, e.message))
	except:
		Log("Unable to write file \"{}\"".format(path))
