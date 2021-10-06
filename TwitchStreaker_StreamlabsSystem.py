# === Imports ===
import codecs, json, math, os, time

# === Paths ===
SCRIPT_FOLDER = os.path.realpath(os.path.dirname(__file__))
TEXT_FOLDER   = os.path.join(SCRIPT_FOLDER, "Text\\")
SOUNDS_FOLDER = os.path.join(SCRIPT_FOLDER, "Sounds\\")

# === System Files ===
LOG_FILE      = os.path.join(SCRIPT_FOLDER, "TwitchStreaker.log")
SESSION_FILE  = os.path.join(SCRIPT_FOLDER, "Session.json")
SETTINGS_FILE = os.path.join(SCRIPT_FOLDER, "Settings.json")

# === Base Files ===
BITS_LEFT_FILE    = os.path.join(TEXT_FOLDER, "BitsLeft.txt")
FOLLOWS_LEFT_FILE = os.path.join(TEXT_FOLDER, "FollowsLeft.txt")
GOAL_FILE         = os.path.join(TEXT_FOLDER, "Goal.txt")
POINTS_FILE       = os.path.join(TEXT_FOLDER, "Points.txt")
POINTS_LEFT_FILE  = os.path.join(TEXT_FOLDER, "PointsLeft.txt")
STREAK_FILE       = os.path.join(TEXT_FOLDER, "Streak.txt")

# === Point Files ===
BIT_POINTS_FILE      = os.path.join(TEXT_FOLDER, "BitPoints.txt")
DONATION_POINTS_FILE = os.path.join(TEXT_FOLDER, "DonationPoints.txt")
FOLLOW_POINTS_FILE   = os.path.join(TEXT_FOLDER, "FollowPoints.txt")
SUB_POINTS_FILE      = os.path.join(TEXT_FOLDER, "SubPoints.txt")

# === Bar Files ===
BAR_GOAL_FILE               = os.path.join(TEXT_FOLDER, "BarGoal.txt")
BAR_POINTS_LEFT_FILE        = os.path.join(TEXT_FOLDER, "BarPointsLeft.txt")
BAR_SEGMENT_POINTS_LEFT     = os.path.join(TEXT_FOLDER, "BarSegmentPointsLeft.txt")
BAR_SEGMENTS_COMPLETED_FILE = os.path.join(TEXT_FOLDER, "BarSegmentsCompleted.txt")

# === Totals Files ===
TOTAL_BITS_FILE      = os.path.join(TEXT_FOLDER, "TotalBits.txt")
TOTAL_DONATIONS_FILE = os.path.join(TEXT_FOLDER, "TotalDonations.txt")
TOTAL_FOLLOWS_FILE   = os.path.join(TEXT_FOLDER, "TotalFollows.txt")
TOTAL_SUBS_FILE      = os.path.join(TEXT_FOLDER, "TotalSubs.txt")

# === External References ===
import clr
clr.AddReference("Newtonsoft.Json.dll")
clr.AddReference("EngineIoClientDotNet.dll")
clr.AddReference("SocketIoClientDotNet.dll")
clr.AddReferenceToFileAndPath(os.path.join(SCRIPT_FOLDER, "Lib\\StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient


# === Script Info ===
ScriptName  = "Twitch Streaker"
Website     = "https://github.com/BrainInBlack/TwitchStreaker"
Creator     = "BrainInBlack"
Version     = "3.0.0"
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

	def __init__(self):
		self.__dict__ = self.DefaultSession()

	def Load(self):
		try:
			with codecs.open(SESSION_FILE, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8-sig")
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

	@staticmethod
	def DefaultSession():
		return {
			# Base Values
			"BitsLeft": 500,
			"FollowsLeft": 0,
			"Goal": 10,
			"Points": 0,
			"PointsLeft": 10,
			"Streak": 1,

			# Point Values
			"BitPoints": 0,
			"DonationPoints": 0,
			"FollowPoints": 0,
			"SubPoints": 0,

			# Bar Values
			"BarGoal": 100,
			"BarGoalCompleted": False,
			"BarPointsLeft": 0,
			"BarSegmentPointsLeft": 0,
			"BarSegmentsCompleted": 0,

			# Totals Values
			"TotalBits": 0,
			"TotalFollows": 0,
			"TotalSubs": 0,
			"TotalDonations": 0
		}


# === Settings Class ===
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

	# Follows
	CountFollows = False
	FollowsRequired = 10
	FollowPointValue = 1

	# Progressbar
	BarGoal = 100
	BarSegmentCount = 4
	BarBitsEnabled = True
	BarDonationsEnabled = True
	BarFollowsEnabled = True
	BarSubsEnabled = True

	# Sounds
	SoundEnabled = False
	SoundBarGoalCompleted = None
	SoundBarGoalCompletedDelay = 0
	SoundBarSegmentCompleted = None
	SoundBarSegmentCompletedDelay = 0

	# Streamlabs
	SocketToken = None

	def __init__(self):
		self.__dict__ = self.DefaultSettings()

	def Load(self):
		try:
			with codecs.open(SETTINGS_FILE, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8-sig")
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

			# Follows
			"CountFollows": False,
			"FollowPointValue": 1,
			"FollowsRequired": 10,

			# Progressbar
			"BarDisplayColors": True,
			"BarGoal": 100,
			"BarSegmentCount": 4,
			"BarBitsEnabled": True,
			"BarDonationsEnabled": True,
			"BarFollowsEnabled": True,
			"BarSubsEnabled": True,

			# Sounds
			"SoundEnabled": False,
			"SoundBarGoalCompleted": None,
			"SoundBarGoalCompletedDelay":0,
			"SoundBarSegmentCompleted": None,
			"SoundBarSegmentCompletedDelay": 0,

			# Streamlabs
			"SocketToken": None
		}


# === Internal Class ===
class ScriptInternals(object):
	
	# BaseVars
	ScriptReady = False
	EventIDs    = []

	# SoundVars
	SoundGoalCued    = False
	SoundSegmentCued = False

	# StampVars
	StampFlush        = time.time()
	StampRefresh      = time.time()
	StampSave         = time.time()
	StampSoundGoal    = time.time()
	StampSoundSegment = time.time()

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

	# Create missing folders
	if not os.path.exists(TEXT_FOLDER):   os.mkdir(TEXT_FOLDER)
	if not os.path.exists(SOUNDS_FOLDER): os.mkdir(SOUNDS_FOLDER)

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

	Socket = StreamlabsEventClient()
	Socket.StreamlabsSocketConnected    += SocketConnected
	Socket.StreamlabsSocketDisconnected += SocketDisconnected
	Socket.StreamlabsSocketEvent        += SocketEvent
	Socket.Connect(Settings.SocketToken)


# === Event Bus ===
def SocketEvent(sender, args):

	# Get Data
	data = args.Data
	msg  = data.Message[0]  # Messages come in as single events, no need for a loop

	# Event Filtering
	Internal.StampFlush = time.time()
	if msg.Id in Internal.EventIDs:
		return
	Internal.EventIDs.append(msg.Id)

	# Skip on Repeat and NotLive
	if msg.IsRepeat:
		return
	if not msg.IsLive and not msg.IsTest:
		return

	# === Twitch ===
	if data.For == "twitch_account":

		# === Bits ===
		if data.Type == "bits" and Settings.CountBits:

			# Ignore TestBits for the total amount of Bits
			if not msg.IsTest:
				Session.TotalBits += msg.Amount

			# Bits are above MinAmount
			if msg.Amount >= Settings.BitsMinAmount:

				if Settings.CountBitsOnce:
					Session.Points    += Settings.BitsPointValue
					Session.BitPoints += Settings.BitsPointValue
					Log("Added {} Point(s) for {} Bits from {}".format(Settings.BitsPointValue, msg.Amount, msg.Name))
					return

				res = Settings.BitsPointValue * math.trunc(msg.Amount / Settings.BitsMinAmount)

				# Add remainder to BitsTemp, if cumulative Bits are enabled
				if Settings.CountBitsCumulative:
					Internal.TempBits += msg.Amount % Settings.BitsMinAmount

				Session.Points    += res
				Session.BitPoints += res
				Log("Added {} Point(s) for {} Bits from {}".format(res, msg.Amount, msg.Name))
				return

			# Cumulative Bits
			elif Settings.CountBitsCumulative:

				Internal.TempBits += msg.Amount
				Log("Added {} Bit(s) from {} to the cumulative amount".format(msg.Amount, msg.Name))

			else:
				Log("Ignored {} Bits from {}, not above the Bits minimum.".format(msg.Amount, msg.Name))
			return

		# === Follows ===
		if data.Type == "follow" and Settings.CountFollows:

			# Ignore TestFollows for the total amount of follows
			if not msg.IsTest:
				Session.TotalFollows += 1

			Internal.TempFollows += 1
			if Internal.TempFollows >= Settings.FollowsRequired:
				Session.Points       += Settings.FollowPointValue
				Session.FollowPoints += Settings.FollowPointValue
				Internal.TempFollows -= Settings.FollowsRequired
				Log("Added {} Point(s) for the follow from {}".format(Settings.FollowPointValue, msg.Name))

		# === Subscriptions ===
		if data.Type == "subscription":

			# === Gifted Subs ===
			if msg.SubType == "subgift" or msg.SubType == "anonsubgift":

				# Ignore gifted Subs by the Streamer or the Recipient
				if msg.Gifter == ChannelName and not msg.IsTest:
					return
				if msg.Name == msg.Gifter and not msg.IsTest:
					return

				# ReSub
				if msg.Months is not None:

					res = Settings.GiftReSub1
					if msg.SubPlan == "2000": res = Settings.GiftReSub2
					if msg.SubPlan == "3000": res = Settings.GiftReSub3

					Session.Points    += res
					Session.SubPoints += res
					Session.TotalSubs += 1
					Log("Added {} Point(s) for a {} Subscription from {} to {}".format(res, msg.SubType, msg.Gifter, msg.Name))
					return

				# New Sub
				else:

					res = Settings.GiftSub1
					if msg.SubPlan == "2000": res = Settings.GiftSub2
					if msg.SubPlan == "3000": res = Settings.GiftSub3

					Session.Points    += res
					Session.SubPoints += res
					Session.TotalSubs += 1
					Log("Added {} Point(s) for a {} Subscription from {} to {}".format(res, msg.SubType, msg.Gifter, msg.Name))
					return

			# ReSubs
			elif msg.SubType == "resub" and (Settings.CountReSubs or msg.IsTest):

				res = Settings.ReSub1
				if msg.SubPlan == "2000": res = Settings.ReSub2
				if msg.SubPlan == "3000": res = Settings.ReSub3

				Session.Points    += res
				Session.SubPoints += res
				Session.TotalSubs += 1
				Log("Added {} Point(s) for a {} Subscription from {}".format(res, msg.SubType, msg.Name))
				return
			# Resubs - END

			# Subs
			else:

				res = Settings.Sub1
				if msg.SubPlan == "2000": res = Settings.Sub2
				if msg.SubPlan == "3000": res = Settings.Sub3

				Session.Points    += res
				Session.SubPoints += res
				Session.TotalSubs += 1
				Log("Added {} Point(s) for a {} Subscription from {}".format(res, msg.SubType, msg.Name))
				return
			# Subs - END

		return  # /Twitch

	# === Youtube ===
	if data.For == "youtube_account":

		# === Subscription ===
		if data.Type == "subscription":

			if msg.Months > 1 and not Settings.CountResubs:
				return

			Session.Points    += Settings.Sub1
			Session.SubPoints += Settings.Sub2
			Session.TotalSubs += 1
			Log("Added {} Point(s) for a Sponsorship from {} (YouTube)".format(Settings.Sub1, msg.Name))
			return

		# === Superchat ===
		if data.Type == 'superchat':

			if not msg.IsTest:
				Session.TotalDonations += msg.Amount

			if msg.Amount >= Settings.DonationMinAmount:

				if Settings.CountDonationsOnce:
					Session.Points += Settings.DonationPointValue
					Log("Added {} Point(s) for a {} {} Superchat from {}".format(Settings.DonationPointValue, msg.Amount, msg.Currency, msg.Name))
					return

				res = Settings.DonationPointValue * math.trunc(msg.Amount / Settings.DonationMinAmount)

				# Add remainder to DonationTemp, if cumulative Donations are enabled
				if Settings.CountDonationsCumulative:
					Internal.TempDonations += msg.Amount % Settings.DonationMinAmount

				Session.Points         += res
				Session.DonationPoints += res
				Log("Added {} Point(s) for a {} {} Superchat from {}".format(res, msg.Amount, msg.Currency, msg.Name))
				return

			elif Settings.CountDonationsCumulative:

				Internal.TempDonations += msg.Amount
				Log("Added Superchat of {} {} from {} to the cumulative Amount.".format())
				return

			else:
				Log("Ignored Superchat of {} {} from {}, Donation is not above the Donation minimum.".format(msg.Amount, msg.Currency, msg.Name))
				return

		return

	# === Streamlabs ===
	if data.For == "streamlabs":

		# === Donation ===
		if data.Type == "donation" and Settings.CountDonations:

			# Ignore test donations for the total amount
			if not msg.IsTest:
				Session.TotalDonations += msg.Amount

			# Donation is above MinAmount
			if msg.Amount >= Settings.DonationMinAmount:

				if Settings.CountDonationsOnce:
					Session.Points += Settings.DonationPointValue
					Session.DonationPoints += Settings.DonationPointValue
					Log("Added {} Point(s) for a {} {} Donation from {}.".format(Settings.DonationPointValue, msg.Amount, msg.Currency, msg.FromName))
					return

				res = Settings.DonationPointValue * math.trunc(msg.Amount / Settings.DonationMinAmount)

				# Add remainder to DonationTemp, if cumulative Donations are enabled
				if Settings.CountDonationsCumulative:
					Internal.TempDonations += msg.Amount % Settings.DonationMinAmount  # Add remainder to DonationTemp

				Session.Points         += res
				Session.DonationPoints += res
				Log("Added {} Point(s) for a {} {} Donation from {}.".format(res, msg.Amount, msg.Currency, msg.FromName))
				return

			# Cumulative Donation
			elif Settings.CountDonationsCumulative:

				Internal.TempDonations += msg.Amount
				Log("Added Donation of {} {} from {} to the cumulative Amount.".format(msg.Amount, msg.Currency, msg.FromName))
				return

			else:
				Log("Ignored Donation of {} {} from {}, Donation is not above the Donation minimum.".format(msg.Amount, msg.Currency, msg.FromName))
				return

		return  # /Streamlabs

	Log("Unknown/Unsupported Platform {}!".format(data.For))


# === Event Connected ===
def SocketConnected(sender, args): Log("Connected")


# === Event Disconnected ===
def SocketDisconnected(sender, args): Log("Disconnected")


# === Tick ===
def Tick():
	now = time.time()

	# Flush EventIDs
	if(now - Internal.StampFlush) >= FLUSH_DELAY and len(Internal.EventIDs) > 0:
		Internal.EventIDs = []
		Internal.StampFlush = now

	# Main Refresh
	if (now - Internal.StampRefresh) >= REFRESH_DELAY:

		# Attempt Startup
		if not Internal.ScriptReady:
			StartUp()

		# Reconnect
		if Socket is None or not Socket.IsConnected:
			Connect()
			return

		UpdateTracker()  # Updates StampRefresh

	# Save Timer
	if (now - Internal.StampSave) >= SAVE_DELAY:
		if not Internal.ScriptReady: return
		try:
			Session.Save()
		except Exception as e:
			Log(e.message)
		Internal.StampSave = now

	# Sound System
	if Settings.SoundEnabled and (Internal.SoundGoalCued or Internal.SoundSegmentCued):
		if not Internal.ScriptReady: return

		if Internal.SoundGoalCued and Internal.SoundSegmentCued:  # ! Only play goal sound
			Internal.SoundSegmentCued = False

		# Goal Sound
		if (now - Internal.StampSoundGoal) >= Settings.SoundBarGoalCompletedDelay:
			snd = os.path.join(SOUNDS_FOLDER, Settings.SoundBarGoalCompleted)
			if not os.path.exists(snd):
				Log("Goal Completion Sound file \"{}\" is missing!".format(Settings.SoundBarGoalCompleted))
			if not Parent.PlaySound(snd, 1.0):
				Log("Unable to play sound {}".format(Settings.SoundBarGoalCompleted))
			Internal.StampSoundGoal = now
			Internal.SoundGoalCued = False

		# Segment Sound
		if (now - Internal.StampSoundSegment) >= Settings.SoundBarSegmentCompletedDelay:
			snd = os.path.join(SOUNDS_FOLDER, Settings.SoundBarSegmentCompleted)
			if not os.path.exists(snd):
				Log("Segment Completion Sound file \"{}\" is missing!".format(Settings.SoundBarSegmentCompleted))
			if not Parent.PlaySound(snd, 1.0):
				Log("Unable to play sound {}".format(Settings.SoundBarSegmentCompleted))
			Internal.StampSoundSegment = now
			Internal.SoundSegmentCued = False



# === Update Tracker ===
def UpdateTracker():  # ! Only call if a quick response is required

	now = time.time()

	# Calculate Bits
	if Settings.CountBitsCumulative and Internal.TempBits >= Settings.BitsMinAmount:
		res = math.trunc(Internal.TempBits / Settings.BitsMinAmount)
		Session.Points += Settings.BitsPointValue * res
		Session.BitPoints += Settings.BitsPointValue
		Internal.TempBits -= Settings.BitsMinAmount * res
		Log("Added {} Point(s), because the cumulative Bits amount exceeded the minimum Bits Amount.".format(Settings.BitsPointValue * res))
		Session.BitsLeft = Settings.BitsMinAmount - Internal.TempBits
		del res

	# Calculate Donations
	if Settings.CountDonationsCumulative and Internal.TempDonations >= Settings.DonationMinAmount:
		res = math.trunc(Internal.TempDonations / Settings.DonationMinAmount)
		Session.Points += Settings.DonationPointValue
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
			Internal.SoundGoalCued  = True
			Internal.StampSoundGoal = now
		elif pointsSum >= segmentSize and Session.BarSegmentsCompleted < math.floor(pointsSum / segmentSize) and not Internal.SoundGoalCued:
			Session.BarSegmentsCompleted += 1
			Internal.SoundSegmentCued  = True
			Internal.StampSoundSegment = now

	# Update Overlay
	Parent.BroadcastWsEvent("EVENT_UPDATE_OVERLAY", str(json.dumps(Session.__dict__)))
	Parent.BroadcastWsEvent("EVENT_UPDATE_BAR",     str(json.dumps({
		"DisplayColors":    Settings.BarDisplayColors,
		"Goal":             Settings.BarGoal,
		"SegmentCount":     Settings.BarSegmentCount,
		"SegmentSize":      segmentSize,
		"BitPoints":        Session.BitPoints,
		"BitsEnabled":      Settings.BarBitsEnabled,
		"DonationPoints":   Session.DonationPoints,
		"DonationsEnabled": Settings.BarDonationsEnabled,
		"FollowPoints":     Session.FollowPoints,
		"FollowsEnabled":   Settings.BarFollowsEnabled,
		"SubPoints":        Session.SubPoints,
		"SubsEnabled":      Settings.BarSubsEnabled
	})))

	# Update Text Files
	SimpleWrite(BAR_GOAL_FILE,               Session.BarGoal)
	SimpleWrite(BAR_POINTS_LEFT_FILE,        Session.BarPointsLeft)
	SimpleWrite(BAR_SEGMENT_POINTS_LEFT,     Session.BarSegmentPointsLeft)
	SimpleWrite(BAR_SEGMENTS_COMPLETED_FILE, Session.BarSegmentsCompleted)
	SimpleWrite(BITS_LEFT_FILE,              Session.BitsLeft)
	SimpleWrite(BIT_POINTS_FILE,             Session.BitPoints)
	SimpleWrite(DONATION_POINTS_FILE,        Session.DonationPoints)
	SimpleWrite(FOLLOW_POINTS_FILE,          Session.FollowPoints)
	SimpleWrite(FOLLOWS_LEFT_FILE,           Session.FollowsLeft)
	SimpleWrite(GOAL_FILE,                   Session.Goal)
	SimpleWrite(POINTS_FILE,                 Session.Points)
	SimpleWrite(POINTS_LEFT_FILE,            Session.PointsLeft)
	SimpleWrite(STREAK_FILE,                 Session.Streak)
	SimpleWrite(SUB_POINTS_FILE,             Session.SubPoints)
	SimpleWrite(TOTAL_BITS_FILE,             Session.TotalBits)
	SimpleWrite(TOTAL_FOLLOWS_FILE,          Session.TotalFollows)
	SimpleWrite(TOTAL_SUBS_FILE,             Session.TotalSubs)
	SimpleWrite(TOTAL_DONATIONS_FILE,        Session.TotalDonations)

	# Update Refresh Stamp
	Internal.StampRefresh = now


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
	if Session.Goal  < Settings.GoalMin:
		Session.Goal = Settings.GoalMin
		is_session_dirty    = True

	# Prevent Goal from being higher than GoalMax
	if Session.Goal  > Settings.GoalMax:
		Session.Goal = Settings.GoalMax
		is_session_dirty    = True

	# Prevent PointsLeft de-sync
	if Session.Goal != (Session.PointsLeft + Session.Points):
		Session.PointsLeft = Session.Goal - Session.Points
		is_session_dirty = True

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

	Internal.TempBits      = 0
	Internal.TempDonations = 0
	Internal.TempFollows   = 0

	Session.__dict__    = Session.DefaultSession()
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
def ReloadSettings(json_data):  # Triggered by the bot on Save Settings
	global Socket

	# Backup old token for comparison
	old_token = Settings.SocketToken
	Settings.__dict__ = json.loads(json_data)

	# Reconnect if Token changed
	if old_token is None or Settings.SocketToken != old_token:
		if Socket:
			if Socket.IsConnected:
				Socket.Disconnect()
			Socket = None
		Connect()
		if not Internal.ScriptReady:
			Internal.ScriptReady = True

	SanityCheck()
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
	if Socket and Socket.IsConnected:
		Socket.Disconnect()
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
def Log(message):
	try:
		with codecs.open(LOG_FILE, encoding="utf-8", mode="a+") as f:
			f.write("{} - {}\n".format(time.strftime("%m/%d/%y - %H:%M:%S"), message))
			f.close()
	except IOError as e:
		Parent.Log(ScriptName, "Unable to write to logfile. ({})".format(e.message))
	except:
		Parent.Log(ScriptName, "Unable to write to logfile.")

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
