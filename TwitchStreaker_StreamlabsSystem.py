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

# === Base Files ===
BITS_LEFT               = os.path.join(TEXT_FOLDER, "BitsLeft.txt")
FOLLOWS_LEFT            = os.path.join(TEXT_FOLDER, "FollowsLeft.txt")
GOAL                    = os.path.join(TEXT_FOLDER, "Goal.txt")
POINTS                  = os.path.join(TEXT_FOLDER, "Points.txt")
POINTS_LEFT             = os.path.join(TEXT_FOLDER, "PointsLeft.txt")
STREAK                  = os.path.join(TEXT_FOLDER, "Streak.txt")

# === Point Files ===
BIT_POINTS              = os.path.join(TEXT_FOLDER, "BitPoints.txt")
DONATION_POINTS         = os.path.join(TEXT_FOLDER, "DonationPoints.txt")
FOLLOW_POINTS           = os.path.join(TEXT_FOLDER, "FollowPoints.txt")
SUB_POINTS              = os.path.join(TEXT_FOLDER, "SubPoints.txt")

# === Bar Files ===
BAR_GOAL                = os.path.join(TEXT_FOLDER, "BarGoal.txt")
BAR_POINTS_LEFT         = os.path.join(TEXT_FOLDER, "BarPointsLeft.txt")
BAR_SEGMENT_POINTS_LEFT = os.path.join(TEXT_FOLDER, "BarSegmentPointsLeft.txt")
BAR_SEGMENTS_COMPLETED  = os.path.join(TEXT_FOLDER, "BarSegmentsCompleted.txt")

# === Totals Files ===
TOTAL_BITS              = os.path.join(TEXT_FOLDER, "TotalBits.txt")
TOTAL_DONATIONS         = os.path.join(TEXT_FOLDER, "TotalDonations.txt")
TOTAL_FOLLOWS           = os.path.join(TEXT_FOLDER, "TotalFollows.txt")
TOTAL_SUBS              = os.path.join(TEXT_FOLDER, "TotalSubs.txt")

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
	BarPointsLeft        = 0
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
		self.LogFile = "{}.log".format(time.strftime("%m-%d-%y_%H-%M-%S"))

	def Load(self):
		try:
			with codecs.open(SESSION_FILE, encoding="utf-8-sig", mode="r") as f:
				self.__dict__.update(json.load(f, encoding="utf-8-sig"))
				f.close()
		except:
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
	DonationMinAmount        = 5.0
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
	Sub2        = 1
	Sub3        = 1
	ReSub1      = 1
	ReSub2      = 1
	ReSub3      = 1
	GiftSub1    = 1
	GiftSub2    = 1
	GiftSub3    = 1
	GiftReSub1  = 1
	GiftReSub2  = 1
	GiftReSub3  = 1

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
	try:
		Session.Load()
		Settings.Load()
	except Exception as e:
		Log(e.message)
		return
	Session.BarGoal = Settings.BarGoal
	Session.Goal    = Settings.Goal

	# Create missing folders
	if not os.path.exists(LOG_FOLDER):    os.mkdir(LOG_FOLDER)
	if not os.path.exists(SOUNDS_FOLDER): os.mkdir(SOUNDS_FOLDER)
	if not os.path.exists(TEXT_FOLDER):   os.mkdir(TEXT_FOLDER)

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
	if not "message" in event:
		Log("No message in Event: {}".format(json.dumps(event)))
	
	# Fix Streamlabs Donation
	if not "for" in event and "type" in event and event["type"] == "donation":
		event["for"] = "streamlabs"

	# Fix Message Format
	if isinstance(event["message"], dict):
		event["message"] = json.loads("[ {} ]".format(json.dumps(event["message"])))

	msg = event["message"][0]  # Messages come in as single events, a loop is not needed

	# Repeat and isTest
	if "repeat" in msg:
		return
	if "isTest" in msg:
		isTest = msg["isTest"]
	else:
		isTest = False

	# Event Filter
	Internal.FlushStamp = time.time()
	if msg["_id"] in Internal.EventIDs:
		return
	Internal.EventIDs.append(msg["_id"])

	# === Twitch ===
	if event["for"] == "twitch_account":

		# === Bits ===
		if event["type"] == "bits" and Settings.CountBits:

			# Simplification
			name   = msg["name"]
			amount = int(msg["amount"])

			# Ignore TestBits for the total amount of Bits
			if not isTest:
				Session.TotalBits += amount

			# Bits are above the minimum amount required
			if amount >= Settings.BitsMinAmount:

				# Non cumulative Bits
				if Settings.CountBitsOnce:
					Session.Points += Settings.BitsPointValue
					Session.BitPoints += Settings.BitsPointValue
					Log("Added {} Point(s) for {} Bits from {}".format(Settings.BitsPointValue, amount, name))
					return

				# Calculate Points
				res = int(Settings.BitsPointValue * math.floor(amount / Settings.BitsMinAmount))

				# Add remainder to TempBits, if cumulative Bits are enabled
				if Settings.CountBitsCumulative:
					Internal.TempBits += amount % Settings.BitsMinAmount

				# Update Session
				Session.Points += res
				Session.BitPoints += res
				Log("Added {} Point(s) for {} Bits from {}".format(res, amount, name))
				return

			# Bits are below the minimum amount required and cumulative Bits are enabled
			elif Settings.CountBitsCumulative:
				Internal.TempBits += amount
				Log("Added {} Bit(s) from {} to the cumulative amount".format(amount, name))

			# Amount of Bits are not above the minimum amount required and cumulative Bits are disabled
			else:
				Log("Ignored {} Bits from {}, not above the Bits minimum.".format(amount, name))
			return

		# === Follows ===
		if event["type"] == "follow" and Settings.CountFollows:

			# Simplification
			name = msg["name"]
			
			# Ignore TestFollows for the total amount of Follows
			if not isTest:
				Session.TotalFollows += 1

			# Update TempFollows
			Internal.TempFollows += 1

			# Update Session and TempFollows if the TempFollows are above the minimum amount required
			if Internal.TempFollows >= Settings.FollowsRequired:
				Session.Points += Settings.FollowPointValue
				Session.FollowPoints += Settings.FollowPointValue
				Internal.TempFollows -= Settings.FollowsRequired
				Log("Added {} Point(s) for the follow from {}".format(Settings.FollowPointValue, name))
			return
		
		# === Subscriptions ===
		if event["type"] == "subscription":

			# Simplification
			name = msg["name"]

			# Type Hackery
			if not "sub_type" in msg and "type" in msg:
				type = msg["type"]
			elif "sub_type" in msg:
				type = msg["sub_type"]
			elif "months" in msg and int(msg["months"]) > 0:
				type = "resub"
			else:
				type = "sub"
			
			# Tier Hackery
			if "plan" in msg:
				tier = msg["plan"]
			elif "subPlan" in msg:
				tier = msg["subPlan"]
			else:
				tier = msg["sub_plan"]

			# Months Hackery
			if "months" in msg:
				months = int(msg["months"])
			else:
				months = None

			# === Gifted Subs ===
			if type == "subgift" or type == "anonsubgift":

				# Simplification
				gifter = msg["gifter"]

				# Ignore gifted subs by the Streamer or the Recipient
				if gifter == ChannelName and not isTest:
					return
				if gifter == name and not isTest:
					return

				# Point Value
				if months is not None and months > 0:
					res = Settings.GiftReSub1
					if tier == "2000": res = Settings.GiftReSub2
					if tier == "3000": res = Settings.GiftReSub3
				else:
					res = Settings.GiftSub1
					if tier == "2000": res = Settings.GiftSub2
					if tier == "3000": res = Settings.GiftSub3

				# Update Session
				Session.Points    += res
				Session.SubPoints += res
				if not isTest:
					Session.TotalSubs += 1
				Log("Added {} Point(s) for a {} from {} to {}".format(res, type, gifter, name))
				return

			# === Resubs ===
			elif type == "resub" and (Settings.CountReSubs or isTest):
				# Point Value
				res = Settings.ReSub1
				if tier == "2000": res = Settings.ReSub2
				if tier == "3000": res = Settings.ReSub3

				# Update Session
				Session.Points    += res
				Session.SubPoints += res
				if not isTest:
					Session.TotalSubs += 1
				Log("Added {} Point(s) for a {} from {}".format(res, type, name))
				return

			# === Subs ===
			else:
				# Point Value
				res = Settings.Sub1
				if tier == "2000": res = Settings.Sub2
				if tier == "3000": res = Settings.Sub3

				# Update Session
				Session.Points    += res
				Session.SubPoints += res
				if not isTest:
					Session.TotalSubs += 1
				Log("Added {} Point(s) for a {} from {}".format(res, type, name))
				return
		return

	# === Youtube ===
	if event["for"] == "youtube_account":

		# === Follows aka Subscriptions ===
		if event["type"] == "follow" and Settings.CountFollows:

			# Simplification
			name = msg["name"]
			
			# Ignore TestFollows for the total amount of Follows
			if not isTest:
				Session.TotalFollows += 1

			# Update TempFollows
			Internal.TempFollows += 1

			# Update Session and TempFollows if the TempFollows are above the minimum amount required
			if Internal.TempFollows >= Settings.FollowsRequired:
				Session.Points += Settings.FollowPointValue
				Session.FollowPoints += Settings.FollowPointValue
				Internal.TempFollows -= Settings.FollowsRequired
				Log("Added {} Point(s) for the follow from {}".format(Settings.FollowPointValue, name))
			return

		# === Subscriptions aka Memberships ===
		if event["type"] == "subscription":
			# TODO: Implementation
			return

		return

	# === Streamlabs ===
	if event["for"] == "streamlabs":

		# === Donations ===
		if event["type"] == "donation" and Settings.CountDonations:

			# Simplification
			name     = msg["from"]
			amount   = float(msg["amount"])
			currency = msg["currency"]

			# Ignore test Donation for the total amount
			if not isTest:
				Session.TotalDonations += amount

			# Donation is above the minimum amount required
			if amount >= Settings.DonationMinAmount:

				# Non cumulative Donation
				if Settings.CountDonationsOnce:
					Session.Points         += Settings.DonationPointValue
					Session.DonationPoints += Settings.DonationPointValue
					Log("Added {} Point(s) for a {} {} Donation from {}.".format(Settings.DonationPointValue, amount, currency, name))
					return

				# Calculate Points
				res = int(Settings.DonationPointValue * amount / Settings.DonationMinAmount)

				# Add remainder to TempDonation, if cumulative Donations are enabled
				if Settings.CountDonationsCumulative:
					Internal.TempDonations += amount % Settings.DonationMinAmount

				# Update Session
				Session.Points += Settings.DonationPointValue
				Session.DonationPoints += Settings.DonationPointValue
				Log("Added {} Point(s) for a {} {} Donation from {}.".format(res, amount, currency, name))
				return

			# Donation is below the minimum amount required and cumulative Donations are enabled
			elif Settings.CountDonationsCumulative:
				Internal.TempDonations += amount
				Log("Added Donation of {} {} from {} to the cumulative Amount.".format(amount, currency, name))
				return

			# Donation is below the minimum amount required and cumulative Donations are disabled
			else:
				Log("Ignored Donation of {} {} from {}, Donation is not above the Donation minimum.".format(amount, currency, name))
				return

		return

	Log("Unknown/Unsupported Platform {}!".format(event["for"]))


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
	if (now - Internal.FlushStamp) >= FLUSH_DELAY and len(Internal.EventIDs) > 0:
		Internal.EventIDs = []
		Internal.FlushStamp = now

	# Main Refresh
	if (now - Internal.RefreshStamp) >= REFRESH_DELAY:

		# Attempt Startup
		if not Internal.ScriptReady:
			StartUp()

		# Reconnect
		if not Socket:
			Connect()
			Internal.RefreshStamp = now
			return

		UpdateTracker()
		Internal.RefreshStamp = now

	# Save Timer
	if (now - Internal.SaveStamp) >= SAVE_DELAY:
		if not Internal.ScriptReady: return
		try:
			Session.Save()
		except Exception as e:
			Log(e.message)
		Internal.SaveStamp = now

	# Sound System
	if Settings.SoundEnabled and (Internal.GoalSoundCued or Internal.SegmentSoundCued):
		if not Internal.ScriptReady: return

		if Internal.GoalSoundCued and Internal.SegmentSoundCued:  # ! Only play goal sound
			Internal.SegmentSoundCued = False

		# Goal Sound
		if (now - Internal.GoalSoundStamp) >= Settings.GoalCompletedSoundDelay and Internal.GoalSoundCued:
			snd = os.path.join(SOUNDS_FOLDER, Settings.GoalCompletedSound)
			if not os.path.exists(snd):
				Log("Goal Completion Sound file \"{}\" is missing!".format(Settings.GoalCompletedSound))
			if not PlaySound(snd):
				Log("Unable to play sound {}".format(Settings.GoalCompletedSound))
			Internal.GoalSoundStamp = now
			Internal.GoalSoundCued = False

		# Segment Sound
		if (now - Internal.SegmentSoundStamp) >= Settings.SegmentCompletedSoundDelay and Internal.SegmentSoundCued:
			snd = os.path.join(SOUNDS_FOLDER, Settings.SegmentCompletedSound)
			if not os.path.exists(snd):
				Log("Segment Completion Sound file \"{}\" is missing!".format(Settings.SegmentCompletedSound))
			if not PlaySound(snd):
				Log("Unable to play sound {}".format(Settings.SegmentCompletedSound))
			Internal.SegmentSoundStamp = now
			Internal.SegmentSoundCued = False


# === Update Tracker ===
def UpdateTracker():  # ! Only call if a quick response is required

	now = time.time()

	# Calculate Bits
	if Settings.CountBitsCumulative and Internal.TempBits >= Settings.BitsMinAmount:
		res = math.trunc(Internal.TempBits / Settings.BitsMinAmount)
		Session.Points    += Settings.BitsPointValue * res
		Session.BitPoints += Settings.BitsPointValue
		Internal.TempBits -= Settings.BitsMinAmount * res
		Log("Added {} Point(s), because the cumulative Bits amount exceeded the minimum Bits Amount.".format(Settings.BitsPointValue * res))
		Session.BitsLeft = Settings.BitsMinAmount - Internal.TempBits
		del res

	# Calculate Donations
	if Settings.CountDonationsCumulative and Internal.TempDonations >= Settings.DonationMinAmount:
		res = math.trunc(Internal.TempDonations / Settings.DonationMinAmount)
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
			if Session.Goal  > Settings.GoalMax:
				Session.Goal = Settings.GoalMax

	Session.PointsLeft  = Session.Goal - Session.Points
	Session.FollowsLeft = Settings.FollowsRequired - Internal.TempFollows

	# Update Progress Bar
	pointsSum = 0
	if Settings.BarBitsEnabled:      pointsSum += Session.BitPoints
	if Settings.BarDonationsEnabled: pointsSum += Session.DonationPoints
	if Settings.BarFollowsEnabled:   pointsSum += Session.FollowPoints
	if Settings.BarSubsEnabled:      pointsSum += Session.SubPoints
	segmentSize = math.trunc(Settings.BarGoal / Settings.BarSegmentCount)

	Session.BarPointsLeft = Settings.BarGoal - pointsSum
	if Session.BarPointsLeft < 0: Session.BarPointsLeft = 0

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

	# Update Overlay
	payload = Session.__dict__
	payload["BitsEnabled"]      = Settings.BarBitsEnabled
	payload["DonationsEnabled"] = Settings.BarDonationsEnabled
	payload["FollowsEnabled"]   = Settings.BarFollowsEnabled
	payload["SubsEnabled"]      = Settings.BarSubsEnabled
	payload["SegmentCount"]     = Settings.BarSegmentCount
	Parent.BroadcastWsEvent("EVENT_UPDATE_OVERLAY", str(json.dumps(payload)))

	# Update Text Files
	SimpleWrite(BAR_GOAL,                Session.BarGoal)
	SimpleWrite(BAR_POINTS_LEFT,         Session.BarPointsLeft)
	SimpleWrite(BAR_SEGMENT_POINTS_LEFT, Session.BarSegmentPointsLeft)
	SimpleWrite(BAR_SEGMENTS_COMPLETED,  Session.BarSegmentsCompleted)
	SimpleWrite(BITS_LEFT,               Session.BitsLeft)
	SimpleWrite(BIT_POINTS,              Session.BitPoints)
	SimpleWrite(DONATION_POINTS,         Session.DonationPoints)
	SimpleWrite(FOLLOW_POINTS,           Session.FollowPoints)
	SimpleWrite(FOLLOWS_LEFT,            Session.FollowsLeft)
	SimpleWrite(GOAL,                    Session.Goal)
	SimpleWrite(POINTS,                  Session.Points)
	SimpleWrite(POINTS_LEFT,             Session.PointsLeft)
	SimpleWrite(STREAK,                  Session.Streak)
	SimpleWrite(SUB_POINTS,              Session.SubPoints)
	SimpleWrite(TOTAL_BITS,              Session.TotalBits)
	SimpleWrite(TOTAL_FOLLOWS,           Session.TotalFollows)
	SimpleWrite(TOTAL_SUBS,              Session.TotalSubs)
	SimpleWrite(TOTAL_DONATIONS,         Session.TotalDonations)


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

	Internal.TempBits      = 0
	Internal.TempDonations = 0
	Internal.TempFollows   = 0

	Session             = ScriptSession()
	Session.BarGoal     = Settings.BarGoal
	Session.BitsLeft    = Settings.BitsMinAmount
	Session.FollowsLeft = Settings.FollowsRequired
	Session.Goal        = Settings.Goal
	Session.PointsLeft  = Settings.Goal

	Session.Save()

	SanityCheck()
	UpdateTracker()
	Log("Session Reset!")


# === Reload Settings ===
def ReloadSettings(json_data):
	global Socket

	# Backup old token for comparison
	old_token = Settings.SocketToken
	Settings.__dict__.update(json.loads(json_data))

	# Reconnect if Token changed
	if old_token is None or Settings.SocketToken != old_token:
		# TODO: Update connection
		if Socket:
			Socket.Close()
			Socket = None
		Connect()
		if not Internal.ScriptReady:
			Internal.ScriptReady = True

	Session.BarGoal     = Settings.BarGoal
	Session.Goal        = Settings.Goal

	SanityCheck()
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


# === Simple Write ===
def SimpleWrite(path, content):
	try:
		f = open(path, "w")
		f.write(str(content))
		f.close()
	except IOError as e:
		Log("Unable to write file \"{}\" ({})".format(path, e.message))
	except:
		Log("Unable to write file \"{}\"".format(path))

# === PlaySound Wrapper ===
def PlaySound(path, level = 1.0):
	return Parent.PlaySound(path, level)
