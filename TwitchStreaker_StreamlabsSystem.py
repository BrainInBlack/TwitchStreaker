# === Imports ===
import codecs, json, math, os, time

# === Paths ===
SCRIPT_FOLDER           = os.path.realpath(os.path.dirname(__file__))
LOG_FOLDER              = os.path.join(SCRIPT_FOLDER, "Logs\\")
SOUNDS_FOLDER           = os.path.join(SCRIPT_FOLDER, "Sounds\\")
TEXT_FOLDER             = os.path.join(SCRIPT_FOLDER, "Text\\")

# === System Files ===
SESSION_FILE            = os.path.join(SCRIPT_FOLDER, "Session.json")
SETTINGS_FILE           = os.path.join(SCRIPT_FOLDER, "Settings.json")

# === External References ===
import clr
clr.AddReference("SocketIOClientDotNet.dll")
clr.AddReference("Newtonsoft.Json.dll")
from System import Uri, Action
from Quobject.SocketIoClientDotNet import Client as SocketIO
from Newtonsoft.Json.JsonConvert import SerializeObject as JSONDump

# === Script Info ===
ScriptName  = "Twitch Streaker"
Website     = "https://github.com/BrainInBlack/TwitchStreaker"
Creator     = "BrainInBlack"
Version     = "3.1.0"
Description = "Tracker for new and gifted subscriptions with a streak mechanic."


# === Session Class ===
class ScriptSession(object):

	# Base Values
	BitsLeft    = 500
	FollowsLeft = 10
	Goal        = 10
	Points      = 0
	PointsLeft  = 10
	Streak      = 1

	# Point Values
	BitPoints         = 0
	DonationPoints    = 0
	FollowPoints      = 0
	SubPoints         = 0

	# Bar Values
	BarGoal              = 100
	BarGoalCompleted     = False
	BarPointsLeft        = 100
	BarSegmentPointsLeft = 0
	BarSegmentsCompleted = 0

	# Totals Values
	TotalBits      = 0
	TotalFollows   = 0
	TotalSubs      = 0
	TotalDonations = 0

	# Internal
	LogFile = None

	def __init__(self):
		self.__dict__.update(self.DefaultValues())

	def Load(self):
		try:
			with codecs.open(SESSION_FILE, encoding="utf-8-sig", mode="r") as f:
				self.__dict__.update(json.load(f, encoding="utf-8-sig"))
				f.close()
		except:
			Log("Unable to load settings, using default values instead.", no_console = True)
			self.Save()
			return

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
	def DefaultValues():
		return {
			# Base Values
			"BitsLeft": 500,
			"FollowsLeft": 10,
			"Goal": 10,
			"Points": 0,
			"PointsLeft": 10,
			"Streak": 1,

			# Point Values
			"BitPoints" : 0,
			"DonationPoints": 0,
			"FollowPoints": 0,
			"SubPoints": 0,

			# Bar Values
			"BarGoal": 100,
			"BarGoalCompleted": False,
			"BarPointsLeft": 100,
			"BarSegmentPointsLeft": 0,
			"BarSegmentsCompleted": 0,

			# Totals Values
			"TotalBits": 0,
			"TotalFollows": 0,
			"TotalSubs": 0,
			"TotalDonations": 0,

			# Internal
			"LogFile": "{}.log".format(time.strftime("%m-%d-%y_%H-%M-%S"))
		}


# === Settings Class ===
class ScriptSettings(object):

	# General
	Goal          = 10
	GoalMin       = 5
	GoalMax       = 10
	GoalIncrement = 1

	# Bits
	BitsMinAmount       = 500
	BitsPointValue      = 1
	CountBits           = False
	CountBitsOnce       = False
	CountBitsCumulative = False

	# Donations
	DonationMinAmount        = 5.00
	DonationPointValue       = 1
	CountDonations           = False
	CountDonationsOnce       = False
	CountDonationsCumulative = False

	# Follows
	CountFollows     = False
	FollowsRequired  = 10
	FollowPointValue = 1

	# Subscriptions
	CountReSubs = False
	Sub1        = 1
	Sub2        = 2
	Sub3        = 3
	ReSub1      = 1
	ReSub2      = 2
	ReSub3      = 3
	GiftSub1    = 1
	GiftSub2    = 2
	GiftSub3    = 3
	GiftReSub1  = 1
	GiftReSub2  = 2
	GiftReSub3  = 3

	# Progressbar
	BarGoal             = 100
	BarSegmentCount     = 4
	BarBitsEnabled      = True
	BarDonationsEnabled = True
	BarFollowsEnabled   = True
	BarSubsEnabled      = True

	# Sounds
	SoundEnabled               = False
	GoalCompletedSound         = None
	GoalCompletedSoundDelay    = 0
	SegmentCompletedSound      = None
	SegmentCompletedSoundDelay = 0

	# Streamlabs
	SocketToken = None

	def __init__(self):
		self.__dict__.update(self.DefaultValues())

	def Load(self):
		try:
			with codecs.open(SETTINGS_FILE, encoding="utf-8-sig", mode="r") as f:
				self.__dict__.update(json.load(f, encoding="utf-8-sig"))
				f.close()
		except:
			self.Save()
			return

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
	def DefaultValues():
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
			"DonationMinAmount": 5.00,
			"DonationPointValue": 1,
			"CountDonations": False,
			"CountDonationsOnce": False,
			"CountDonationsCumulative": False,

			# Follows
			"CountFollows": False,
			"FollowsRequired": 10,
			"FollowPointValue": 1,

			# Subscriptions
			"CountReSubs": False,
			"Sub1": 1, "Sub2": 2, "Sub3": 3,
			"ReSub1": 1, "ReSub2": 2, "ReSub3": 3,
			"GiftSub1": 1, "GiftSub2": 2, "GiftSub3": 3,
			"GiftReSub1": 1, "GiftReSub2": 2, "GiftReSub3": 3,

			# Progressbar
			"BarGoal": 100,
			"BarSegmentCount": 4,
			"BarBitsEnabled": True,
			"BarDonationsEnabled": True,
			"BarFollowsEnabled": True,
			"BarSubsEnabled": True,

			# Sounds
			"SoundEnabled": False,
			"GoalCompletedSound": None,
			"GoalCompletedSoundDelay": 0,
			"SegmentCompletedSound": None,
			"SegmentCompletedSoundDelay": 0
		}


# === Internal Class ===
class ScriptInternals(object):
	
	# BaseVars
	ScriptReady = False
	EventIDs    = []

	# SoundVars
	GoalSoundCued    = False
	SegmentSoundCued = False

	# StampVars
	FlushStamp        = time.time()
	RefreshStamp      = time.time()
	SaveStamp         = time.time()
	GoalSoundStamp    = time.time()
	SegmentSoundStamp = time.time()

	# TempVars
	TempBits      = 0
	TempDonations = 0.0
	TempFollows   = 0


# === Event Data ===
class EventData(object):
	For      = None
	IsRepeat = False
	IsTest   = False
	Type     = None


# === Bits Data ===
class BitsData(EventData):
	Name   = None
	Amount = 0


# === Donation Data ===
class DonationData(EventData):
	Name     = None
	Amount   = 0
	Currency = None


# === Follow Data ===
class FollowData(EventData):
	Name = None


# === Subscription Data ===
class SubscriptionData(EventData):
	Name    = None
	Gifter  = None
	Months  = None
	SubPlan = None
	SubType = None


# === Global Variables ===
ChannelName   = None
Internal      = ScriptInternals()
Socket        = None
Session       = ScriptSession()
Settings      = ScriptSettings()


# === Constants ===
FLUSH_DELAY   = 5
REFRESH_DELAY = 5
SAVE_DELAY    = 300
POINT_VARS    = [
	"Sub1", "Sub2", "Sub3",
	"ReSub1", "ReSub2", "ReSub3",
	"GiftSub1", "GiftSub2", "GiftSub3",
	"GiftReSub1", "GiftReSub2", "GiftReSub3",
	"BitsPointValue", "DonationsPointValue", "FollowPointValue"
]
TEXT_PARAMETERS = [
	"BitsLeft", "FollowsLeft", "Goal", "Points", "PointsLeft", "Streak",
	"BitPoints", "DonationPoints", "FollowPoints", "SubPoints",
	"BarGoal", "BarPointsLeft", "BarSegmentPointsLeft", "BarSegmentsCompleted",
	"TotalBits", "TotalDonations", "TotalFollows", "TotalSubs"
]
PARSE_PARAMETERS = {
	# Base Values
	"$tsBitsLeft":       "BitsLeft",
	"$tsFollowsLeft":    "FollowsLeft",
	"$tsGoal":           "Goal",
	"$tsStreak":         "Streak",
	"$tsPoints":         "Points",
	"$tsPointsLeft":     "PointsLeft",

	# Point Values
	"$tsBitPoints":      "BitPoints",
	"$tsDonationPoints": "DonationPoints",
	"$tsFollowPoints":   "FollowPoints",
	"$tsSubPoints":      "SubPoints",

	# BarValues
	"$tsBarGoal":              "BarGoal",
	"$tsBarPointsLeft":        "BarPointsLeft",
	"$tsBarSegmentPointsLeft": "BarSegmentPointsLeft",
	"$tsBarSegmentsCompleted": "BarSegmentsCompleted",

	# Totals Values
	"$tsTotalBits":      "TotalBits",
	"$tsTotalFollows":   "TotalFollows",
	"$tsTotalSubs":      "TotalSubs",
	"$tsTotalDonations": "TotalDonations"
}


# === Initiation ===
def Init():

	# Create missing folders
	if not os.path.exists(LOG_FOLDER):    os.mkdir(LOG_FOLDER)
	if not os.path.exists(SOUNDS_FOLDER): os.mkdir(SOUNDS_FOLDER)
	if not os.path.exists(TEXT_FOLDER):   os.mkdir(TEXT_FOLDER)

	# Load Session and Settings
	try:
		Session.Load()
		Settings.Load()
	except Exception as e:
		Log(e.message)
		return
	Session.BarGoal = Settings.BarGoal
	Session.Goal    = Settings.Goal

	SanityCheck()
	StartUp()


# === StartUp ===
def StartUp():
	global ChannelName

	Internal.ScriptReady = False

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
	Internal.ScriptReady = True
	Connect()


# === Connect Socket ===
def Connect():
	global Socket

	Socket = SocketIO.IO.Socket(Uri("https://sockets.streamlabs.com"), SocketIO.IO.Options(AutoConnect=False, QueryString="token={}".format(Settings.SocketToken)))
	Socket.On("event", Action[object](SocketEvent))
	Socket.On(SocketIO.Socket.EVENT_CONNECT,          Action[object](SocketConnected))
	Socket.On(SocketIO.Socket.EVENT_CONNECT_ERROR,    Action[object](SocketError))
	Socket.On(SocketIO.Socket.EVENT_CONNECT_TIMEOUT,  Action[object](SocketError))
	Socket.On(SocketIO.Socket.EVENT_DISCONNECT,       Action[object](SocketDisconnected))
	Socket.On(SocketIO.Socket.EVENT_ERROR,            Action[object](SocketError))
	Socket.On(SocketIO.Socket.EVENT_RECONNECT_ERROR,  Action[object](SocketError))
	Socket.On(SocketIO.Socket.EVENT_RECONNECT_FAILED, Action[object](SocketError))
	Socket.Connect()


# === Event Bus ===
def SocketEvent(data):

	# Decode Data
	event = json.loads(JSONDump(data).encode(encoding="UTF-8", errors="backslashreplace"))
	
	# Validate Message
	if "message" not in event:
		Log("No message in Event: {}".format(json.dumps(event)), no_console = True)
		return
	
	# Fix Streamlabs Donation
	if "for" not in event and "type" in event and event["type"] == "donation":
		event["for"] = "streamlabs"

	# Fix Message Format
	if isinstance(event["message"], dict):
		event["message"] = json.loads("[ {} ]".format(json.dumps(event["message"])))
	msg = event["message"][0]  # Messages come in as single events, a loop is not needed

	# Event Filter
	Internal.FlushStamp = time.time()
	if msg["_id"] in Internal.EventIDs:
		return
	Internal.EventIDs.append(msg["_id"])

	event_for    = event["for"]
	event_type   = event["type"]
	event_repeat = msg["repeat"] if "repeat" in msg else False
	event_test   = msg["isTest"] if "isTest" in msg else False

	# === Twitch ===
	if event_for == "twitch_account":

		# === Bits ===
		if event_type == "bits":

			payload = BitsData()
			payload.Name     = msg["name"]
			payload.Amount   = int(msg["amount"])
			payload.For      = event_for
			payload.Type     = event_type
			payload.IsTest   = event_test
			payload.IsRepeat = event_repeat
			HandleBits(payload)

		# === Follows ===
		if event_type == "follow":

			payload = FollowData()
			payload.Name     = msg["name"]
			payload.For      = event_for
			payload.Type     = event_type
			payload.IsTest   = event_test
			payload.IsRepeat = event_repeat
			HandleFollow(payload)
		
		# === Subscriptions ===
		if event_type == "subscription":

			# Fix SubType
			if "sub_type" not in msg and "type" in msg:
				sub_type = msg["type"]
			elif "sub_type" in msg:
				sub_type = msg["sub_type"]
			elif "months" in msg and int(msg["months"]) > 0:
				sub_type = "resub"
			else:
				sub_type = "sub"
			
			# Fix SubPlan
			if "plan" in msg:
				sub_plan = msg["plan"]
			elif "subPlan" in msg:
				sub_plan = msg["subPlan"]
			else:
				sub_plan = msg["sub_plan"]

			payload = SubscriptionData()
			payload.Name     = msg["name"]
			payload.Gifter   = msg["gifter"] if sub_type in ["subgift", "anonsubgift"] else None
			payload.Months   = int(msg["months"]) if "months" in msg else None
			payload.SubPlan  = sub_plan
			payload.SubType  = sub_type
			payload.For      = event_for
			payload.Type     = event_type
			payload.IsTest   = event_test
			payload.IsRepeat = event_repeat
			HandleTwitchSub(payload)

	# === Youtube ===
	elif event_for == "youtube_account":

		# === Follows aka Subscriptions ===
		if event_type == "follow":

			payload = FollowData()
			payload.Name     = msg["name"]
			payload.For      = event_for
			payload.Type     = event_type
			payload.IsTest   = event_test
			payload.IsRepeat = event_repeat
			HandleFollow(payload)

		# === Subscriptions aka Memberships ===
		if event_type == "subscription":

			payload = SubscriptionData()
			payload.Name     = msg["name"]
			payload.Gifter   = None
			payload.Months   = None
			payload.SubPlan  = "1000"
			payload.SubType  = "sub"
			payload.For      = event_for
			payload.Type     = event_type
			payload.IsTest   = event_test
			payload.IsRepeat = event_repeat
			HandleTwitchSub(payload)

	# === Streamlabs ===
	elif event_for == "streamlabs":

		# === Donations ===
		if event_type == "donation":

			payload = DonationData()
			payload.Name     = msg["from"]
			payload.Amount   = float(msg["amount"])
			payload.Currency = msg["currency"]
			payload.For      = event_for
			payload.Type     = event_type
			payload.IsTest   = event_test
			payload.IsRepeat = event_repeat
			HandleDonation(payload)

	else:
		Log("Unknown/Unsupported Platform {}!".format(event_for))


# === Handle Bits ===
def HandleBits(data):
	if not Settings.CountBits:
		return

	if not data.IsTest:
		Session.TotalBits += data.Amount

	if data.Amount >= Settings.BitsMinAmount:
		if Settings.CountBitsOnce:
			res = Settings.BitsPointValue
		else:
			res = int(Settings.BitsPointValue * math.floor(data.Amount / Settings.BitsMinAmount))
			if Settings.CountBitsCumulative:
				Internal.TempBits += data.Amount % Settings.BitsMinAmount
		Session.Points    += res
		Session.BitPoints += res
		Log("Added {} Point(s) for {} Bits from {}".format(res, data.Amount, data.Name))
		return
	elif Settings.CountBitsCumulative:
		Internal.TempBits += data.Amount
		Log("Added {} Bit(s) from {} to the cumulative amount".format(data.Amount, data.Name))
	else:
		Log("Ignored {} Bits from {}, not above the Bits minimum.".format(data.Amount, data.Name))


# === Handle Donation ===
def HandleDonation(data):
	if not Settings.CountDonations:
		return

	if not data.IsTest:
		Session.TotalDonations += data.Amount

	if data.Amount >= Settings.DonationMinAmount:
		if Settings.CountDonationsOnce:
			res = Settings.DonationPointValue
		else:
			res = int(Settings.DonationPointValue * data.Amount / Settings.DonationMinAmount)
			if Settings.CountDonationsCumulative:
				Internal.TempDonations += data.Amount % Settings.DonationMinAmount
		Session.Points         += res
		Session.DonationPoints += res
		Log("Added {} Point(s) for a {} {} Donation from {}.".format(res, data.Amount, data.Currency, data.Name))
	elif Settings.CountDonationsCumulative:
		Internal.TempDonations += data.Amount
		Log("Added Donation of {} {} from {} to the cumulative Amount.".format(data.Amount, data.Currency, data.Name))
	else:
		Log("Ignored Donation of {} {} from {}, Donation is not above the Donation minimum.".format(data.Amount, data.Currency, data.Name))


# === Handle Follow ===
def HandleFollow(data):
	if not Settings.CountFollows:
		return

	if not data.IsTest:
		Session.TotalFollows += 1

	Internal.TempFollows += 1

	if Internal.TempFollows >= Settings.FollowsRequired:
		Session.Points       += Settings.FollowPointValue
		Session.FollowPoints += Settings.FollowPointValue
		Internal.TempFollows -= Settings.FollowsRequired
		Log("Added {} Point(s) for the follow from {}".format(Settings.FollowPointValue, data.Name))


# === Handle Twitch Subscription ===
def HandleTwitchSub(data):

	# GiftedSub
	if data.SubType in ["subgift", "anonsubgift"]:
		if data.Gifter == ChannelName and not data.IsTest:
			return
		if data.Gifter == data.Name and not data.IsTest:
			return

		if data.Months > 0:
			res = Settings.GiftReSub1
			if data.SubPlan == "2000":
				res = Settings.GiftReSub2
			elif data.SubPlan == "3000":
				res = Settings.GiftReSub3
		else:
			res = Settings.GiftSub1
			if data.SubPlan == "2000":
				res = Settings.GiftSub2
			elif data.SubPlan == "3000":
				res = Settings.GiftSub3
		msg = "Added {} Point(s) for a gifted Sub from {} to {}".format(res, data.Gifter, data.Name)

	# ReSub
	elif data.Months > 0:
		if not Settings.CountReSubs and not data.IsTest:
			return
		res = Settings.ReSub1
		if data.SubPlan == "2000":
			res = Settings.ReSub2
		elif data.SubPlan == "3000":
			res = Settings.ReSub3
		msg = "Added {} Point(s) for a ReSub from {}".format(res, data.Name)

	# Sub
	else:
		res = Settings.Sub1
		if data.SubPlan == "2000":
			res = Settings.Sub2
		elif data.SubPlan == "3000":
			res = Settings.Sub3
		msg = "Added {} Point(s) for a Sub from {}".format(res, data.Name)
	Session.Points += res
	Session.SubPoints += res
	Log(msg)


# === Handle YouTube Subscription ===
def HandleYouTubeSubscription(data):
	# TODO: Implementation
	# * Uses the same object as the Twitch variant,
	# * only that the SubPlan member is adjusted to
	# * the Youtube system
	pass


# === Event Connected ===
def SocketConnected(data):
	Log("Connected")


# === Event Disconnected ===
def SocketDisconnected(data):
	Log("Disconnected: {}".format(data), no_console = True)
	Log("Disconnected", no_write = True)


# === Event Error ===
def SocketError(data):
	Log("SocketError: {}".format(data.Message), no_console = True)
	Log("SocketError", no_write = True)


# === Tick ===
def Tick():
	now = time.time()

	# Flush EventIDs
	if (now - Internal.FlushStamp) >= FLUSH_DELAY and Internal.EventIDs:
		Internal.EventIDs = []
		Internal.FlushStamp = now

	# Main Refresh
	if (now - Internal.RefreshStamp) >= REFRESH_DELAY:

		# Attempt Startup
		if not Internal.ScriptReady:
			StartUp()
			Internal.RefreshStamp = now
			return

		# Reconnect
		if not Socket:
			Connect()
			Internal.RefreshStamp = now
			return

		UpdateTracker()
		Internal.RefreshStamp = now

	# Save Timer
	if (now - Internal.SaveStamp) >= SAVE_DELAY:
		if not Internal.ScriptReady:
			return
		try:
			Session.Save()
		except Exception as e:
			Log("Unable to save current session!", no_write = True)
			Log(e.message, no_console = True)
		Internal.SaveStamp = now

	# Sound System
	if Settings.SoundEnabled and (Internal.GoalSoundCued or Internal.SegmentSoundCued):
		PlaySound()


# === SoundSystem ===
def PlaySound():
	now = time.time()
	if not Internal.ScriptReady: return

	if Internal.GoalSoundCued and Internal.SegmentSoundCued:  # ! Only play goal sound
		Internal.SegmentSoundCued = False

	# Goal Sound
	if Internal.GoalSoundCued and (now - Internal.GoalSoundStamp) >= Settings.GoalCompletedSoundDelay:
		try:
			Play(Settings.GoalCompletedSound)
		except Exception as e:
			Log('Unable to play Goal Completion Sound.', no_write = True)
			Log('Unable to play Goal Completion Sound: {}.'.format(e.message), no_console = True)
		Internal.GoalSoundStamp = now
		Internal.GoalSoundCued = False

	# Segment Sound
	if Internal.SegmentSoundCued and (now - Internal.SegmentSoundStamp) >= Settings.SegmentCompletedSoundDelay:
		try:
			Play(Settings.SegmentCompletedSound)
		except Exception as e:
			Log('Unable to play Segment Completion Sound.', no_write = True)
			Log('Unable to play Segment Completion Sound: {}.'.format(e.message), no_console = True)
		Internal.SegmentSoundStamp = now
		Internal.SegmentSoundCued = False


# === Update Tracker ===
def UpdateTracker():  # ! Only call if a quick response is required

	# Calculate Bits
	if Settings.CountBitsCumulative and Internal.TempBits >= Settings.BitsMinAmount:
		res = math.floor(Internal.TempBits / Settings.BitsMinAmount)
		Session.Points    += Settings.BitsPointValue * res
		Session.BitPoints += Settings.BitsPointValue
		Internal.TempBits -= Settings.BitsMinAmount * res
		Log("Added {} Point(s), because the cumulative Bits amount exceeded the minimum Bits Amount.".format(Settings.BitsPointValue * res))
		Session.BitsLeft = Settings.BitsMinAmount - Internal.TempBits
		del res

	# Calculate Donations
	if Settings.CountDonationsCumulative and Internal.TempDonations >= Settings.DonationMinAmount:
		res = math.floor(Internal.TempDonations / Settings.DonationMinAmount)
		Session.Points         += Settings.DonationPointValue
		Session.DonationPoints += Settings.DonationPointValue
		Internal.TempDonations -= Settings.DonationMinAmount * res
		Log("Added {} Point(s) because the cumulative Donation amount exceeded the minimum donation amount.".format(Settings.DonationPointValue * res))
		del res

	# Calculate Streak
	while Session.Points >= Session.Goal:  # A loop is used in case the Goal gets incremented for each completed Streak

		# Subtract Goal and Increment Streak
		Session.Points -= Session.Goal
		Session.Streak += 1

		# Increment CurrentGoal
		if Session.Goal   < Settings.GoalMax:
			Session.Goal += Settings.GoalIncrement

			# Correct Goal if GoalIncrement is bigger than the gap from CurrentGoal to GoalMax
			Session.Goal = min(Session.Goal, Settings.GoalMax)

	Session.PointsLeft  = Session.Goal - Session.Points
	Session.FollowsLeft = Settings.FollowsRequired - Internal.TempFollows

	# Updates
	UpdateProgressbar()
	UpdateText()

	# Update Overlay
	payload = Session.__dict__
	payload["BitsEnabled"]      = Settings.BarBitsEnabled
	payload["DonationsEnabled"] = Settings.BarDonationsEnabled
	payload["FollowsEnabled"]   = Settings.BarFollowsEnabled
	payload["SubsEnabled"]      = Settings.BarSubsEnabled
	payload["SegmentCount"]     = Settings.BarSegmentCount
	Parent.BroadcastWsEvent("EVENT_UPDATE_OVERLAY", str(json.dumps(payload)))


# === Update Progressbar ===
def UpdateProgressbar():  # ! Do not call this directly, instead use UpdateTracker()
	pointsSum = 0
	now = time.time()
	if Settings.BarBitsEnabled:      pointsSum += Session.BitPoints
	if Settings.BarDonationsEnabled: pointsSum += Session.DonationPoints
	if Settings.BarFollowsEnabled:   pointsSum += Session.FollowPoints
	if Settings.BarSubsEnabled:      pointsSum += Session.SubPoints
	segmentSize = math.trunc(Settings.BarGoal / Settings.BarSegmentCount)

	Session.BarPointsLeft = Settings.BarGoal - pointsSum
	Session.BarPointsLeft = max(Session.BarPointsLeft, 0)

	Session.BarSegmentPointsLeft = (segmentSize * (Session.BarSegmentsCompleted + 1)) - pointsSum
	if Session.BarSegmentPointsLeft < 0: Session.SegmentPointsLeft = 0

	# Cue Sounds
	if not Session.BarGoalCompleted:
		if pointsSum >= Settings.BarGoal:
			Session.BarGoalCompleted = True
			Internal.GoalSoundCued   = True
			Internal.GoalSoundStamp  = now
		elif pointsSum >= segmentSize and Session.BarSegmentsCompleted < math.floor(pointsSum / segmentSize):
			Session.BarSegmentsCompleted += 1
			Internal.SegmentSoundCued     = True
			Internal.SegmentSoundStamp    = now


# === Update Text ===
def UpdateText():  # ! Do not call this directly, instead use UpdateTracker()
	for var in TEXT_PARAMETERS:
		try:
			with open(os.path.join(TEXT_FOLDER, "{}.txt".format(var)), "w") as f:
				f.write(str(Session.__getattribute__(var)))
				f.close()
		except:
			Log("Unable to write textfile for: {}".format(var), no_write = True)


# === Sanity Check ===
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

	# Prevent Goal from being lower than GoalMin
	if Session.Goal      < Settings.GoalMin:
		Session.Goal     = Settings.GoalMin
		is_session_dirty = True

	# Prevent Goal from being higher than GoalMax
	if Session.Goal      > Settings.GoalMax:
		Session.Goal     = Settings.GoalMax
		is_session_dirty = True

	# Prevent PointsLeft de-sync
	if Session.Goal != (Session.PointsLeft + Session.Points):
		Session.PointsLeft = Session.Goal - Session.Points
		is_session_dirty   = True

	if Session.BarGoal != Settings.BarGoal:
		Session.BarGoal = Settings.BarGoal

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
	if Session.TotalBits  < 0:
		Session.TotalBits = 0
		is_session_dirty  = True

	if Session.TotalFollows  < 0:
		Session.TotalFollows = 0
		is_session_dirty     = True

	if Session.TotalSubs  < 0:
		Session.TotalSubs = 0
		is_session_dirty  = True

	if Session.TotalDonations  < 0:
		Session.TotalDonations = 0
		is_session_dirty       = True

	# Check Bar Settings
	if Settings.BarGoal   < Settings.Goal:
		Settings.BarGoal  = Settings.Goal
		is_settings_dirty = True

	if Settings.BarSegmentCount  > Settings.BarGoal:
		Settings.BarSegmentCount = 1
		is_settings_dirty        = True

	# Check Follow Settings
	if Settings.FollowPointValue  < 1:
		Settings.FollowPointValue = 1
		is_settings_dirty         = True

	if Settings.FollowsRequired  < 1:
		Settings.FollowsRequired = 1
		is_settings_dirty        = True

	# Save Session/Settings if dirty
	try:
		if is_session_dirty:
			Session.Save()
		if is_settings_dirty:
			Settings.Save()
	except Exception as e:
		Log(e.message)


# === Reset Session ===
def ResetSession():
	global Session

	Log("Session End", no_console = True)
	Internal.TempBits      = 0
	Internal.TempDonations = 0
	Internal.TempFollows   = 0

	Session.__dict__.update(ScriptSession.DefaultValues())
	Session.BarGoal       = Settings.BarGoal
	Session.BarPointsLeft = Settings.BarGoal
	Session.BitsLeft      = Settings.BitsMinAmount
	Session.FollowsLeft   = Settings.FollowsRequired
	Session.Goal          = Settings.Goal
	Session.PointsLeft    = Settings.Goal

	SanityCheck()
	UpdateTracker()
	Session.Save()
	Log("New Session", no_console = True)
	Log("Session Reset", no_write = True)


# === Reload Settings ===
def ReloadSettings(json_data):
	global Socket

	# Backup old token for comparison
	old_token = Settings.SocketToken
	Settings.__dict__.update(json.loads(json_data))

	# Reconnect if Token changed
	if old_token is None or Settings.SocketToken != old_token:
		if Socket:
			Socket.Close()
			Socket = None
		Connect()
		Internal.ScriptReady = True

	Session.BarGoal = Settings.BarGoal
	Session.Goal    = Settings.Goal

	SanityCheck()
	UpdateTracker()
	Session.Save()
	Log("Settings saved!")


# === UI Sub Functions ===
def AddPoint():
	Session.Points += 1


def SubtractPoint():
	if Session.Points   > 0:
		Session.Points -= 1


# === UI Streak Functions ===
def AddStreak():
	Session.Streak += 1


def AddStreak5():
	Session.Streak += 5


def AddStreak10():
	Session.Streak += 10


def SubtractStreak():
	if Session.Streak   > 1:
		Session.Streak -= 1


def SubtractStreak5():
	if Session.Streak   > 1:
		Session.Streak -= 5


def SubtractStreak10():
	if Session.Streak   > 1:
		Session.Streak -= 10


# === UI Goal Functions ===
def AddToGoal():
	if Session.Goal   < Settings.GoalMax:
		Session.Goal += 1


def SubtractFromGoal():
	if Session.Goal   > Settings.GoalMin:
		Session.Goal -= 1


# === Unload ===
def Unload():
	global Socket
	if Socket:
		Socket.Close()
	Socket = None
	Internal.ScriptReady = False
	UpdateTracker()
	try:
		Session.Save()
	except Exception as e:
		Log(e.message)


# === Parse Parameters ===
def Parse(parse_string, user_id, username, target_id, target_name, message):
	if parse_string.contains("$ts"):
		for key, val in PARSE_PARAMETERS:
			if key in parse_string:
				parse_string = parse_string.replace(key, getattr(Session, val))
	return parse_string


# === Execute ===
def Execute(data): pass


# === Log Wrapper ===
def Log(message, no_console = False, no_write = False):
	if not no_write:
		try:
			with codecs.open(os.path.join(LOG_FOLDER, Session.LogFile), encoding="utf-8", mode="a+") as f:
				f.write("{} - {}\n".format(time.strftime("%m/%d/%y - %H:%M:%S"), message))
				f.close()
		except IOError as e:
			Parent.Log(ScriptName, "Unable to write to logfile. ({})".format(e.message))
		except:
			Parent.Log(ScriptName, "Unable to write to logfile.")

	if not no_console:
		Parent.Log(ScriptName, message)


# === PlaySound Wrapper ===
def Play(filename, level = 1.0):
	path = os.path.join(SOUNDS_FOLDER, filename)
	if not os.path.exists(path):
		raise Exception('File "{}" not found!'.format(filename))
	if not Parent.PlaySound(path, level):
		raise Exception('Unable to play "{}"'.format(filename))
	return True

