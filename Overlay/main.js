// OverlayLogic
var Overlay = {

	// Elements
	'Streak':   document.getElementById('Streak'),
	'Subs':     document.getElementById('Subs'),
	'SubsLeft': document.getElementById('SubsLeft'),
	'Goal':     document.getElementById('Goal'),
	'Tracker':  document.getElementById('Tracker'), // ! Outline Hack!

	// Refresh, gets called for each Event coming through the EventBus
	'refresh': function() {
		if(this.Streak)   this.Streak.innerText   = settings.Streak;
		if(this.Subs)     this.Subs.innerText     = settings.Subs;
		if(this.SubsLeft) this.SubsLeft.innerText = settings.SubsLeft;
		if(this.Goal)     this.Goal.innerText     = settings.Goal;
		if(this.Tracker)  this.Tracker.title      = this.Tracker.innerText; // ! Outline Hack!
	}
}

// MainLogic
function connectWebsocket() {
	var socket = new WebSocket(API_Socket);

	// Connect to Socket and register Events
	socket.onopen = function () {
		var auth = {
			author:  'BrainInBlack',
			website: 'https://github.com/BrainInBlack/TwitchStreaker',
			api_key:  API_Key,
			events: [
				// Streamlabs Events
				'EVENT_SUB',
				'EVENT_UPDATE_SETTINGS',
				// Custom Events
				'EVENT_ADD_SUB',
				'EVENT_SUBTRACT_SUB',
				'EVENT_ADD_STREAK',
				'EVENT_SUBTRACT_STREAK',
				'EVENT_ADD_TO_GOAL',
				'EVENT_SUBTRACT_FROM_GOAL',
				'EVENT_FORCE_REDRAW',
				'EVENT_RESET'
			]
		};
		socket.send(JSON.stringify(auth));
		console.log('TwitchStreaker: Connected (Socket)');
	};
	// Attempt reconnect after connection loss
	socket.onclose = function () {
		socket = null;
		setTimeout(connectWebsocket, 5000); // 5 Second Delay
		console.log('TwitchStreaker: Reconnecting (Socket)');
	}
	// Output errors to the console (only works in a browser)
	socket.onerror = function(error) {
		console.log('Error: ' + error + ' (System)');
	}

	// EventBus
	socket.onmessage = function (message) {
		var socketMessage = JSON.parse(message.data);

		// Subscription Event
		if (socketMessage.event == 'EVENT_SUB') {
			var data = JSON.parse(socketMessage.data);
			// Check if new or gifted subscription
			if (((data.is_gift && (data.display_name.toLowerCase() != data.gift_target.toLowerCase())) || !data.is_resub) &&
				 (data.display_name.toLowerCase() != settings.StreamerName.toLowerCase())) {
				switch(data.tier) {
					case '3': settings.Subs += settings.Tier3; break;
					case '2': settings.Subs += settings.Tier2; break;
					default:  settings.Subs += settings.Tier1;
				}
				calcStreak();
				Overlay.refresh();
				console.log('TwitchStreaker: New/Gift sub added (Sub)');
			}
			return;
		}

		// SubCounter Overwrite Events
		if(socketMessage.event == 'EVENT_ADD_SUB') {
			settings.Subs++;
			calcStreak();
			Overlay.refresh();
			console.log('TwitchStreaker: Added Sub (Overwrite)');
			return;
		}
		if(socketMessage.event == 'EVENT_SUBTRACT_SUB') {
			if(settings.Subs > 0) {
				settings.Subs--;
				calcStreak();
				Overlay.refresh();
				console.log('TwitchStreaker: Removed Sub (Overwrite)');
			}
			return;
		}

		// StreakCounter Overwrite Events
		if(socketMessage.event == 'EVENT_ADD_STREAK') {
			settings.Streak++;
			calcStreak();
			Overlay.refresh();
			console.log('TwitchStreaker: Added Streak (Overwrite)');
			return;
		}
		if(socketMessage.event == 'EVENT_SUBTRACT_STREAK') {
			if(settings.Streak > 1) {
				settings.Streak--;
				calcStreak();
				Overlay.refresh();
				console.log('TwitchStreaker: Removed Streak (Overwrite)');
			}
			return;
		}

		// StreakGoal Overwrite Events
		if(socketMessage.event == 'EVENT_ADD_TO_GOAL') {
			if(settings.Goal < settings.GoalCap) {
				settings.Goal++;
				calcStreak();
				Overlay.refresh();
				console.log('TwitchStreaker: Added to Goal (Overwrite)');
			}
			return;
		}
		if(socketMessage.event == 'EVENT_SUBTRACT_FROM_GOAL') {
			if(settings.Goal > settings.InitialGoal) {
				settings.Goal--;
				calcStreak();
				Overlay.refresh();
				console.log('TwitchStreaker: Subtracted from Goal (Overwrite)');
			}
			return;
		}

		// Redraw Overwrite Event
		if(socketMessage.event == 'EVENT_FORCE_REDRAW') {
			Overlay.refresh();
			console.log('TwitchStreaker: Force Redraw (Overwrite)');
			return;
		}

		// Reset Overwrite Event
		if(socketMessage.event == 'EVENT_RESET') {
			settings.Streak = 1;
			settings.Subs   = 0;
			settings.Goal   = settings.InitialGoal;

			calcStreak();
			Overlay.refresh();
			console.log('TwitchStreaker: Reset Tracker (Overwrite)');
			return;
		}

		// Update Settings Event
		if (socketMessage.event == 'EVENT_UPDATE_SETTINGS') {
			var data = JSON.parse(socketMessage.data);

			// Assign new values and ensure positive numbers
			settings.Goal            = Math.abs(data.Goal);
			settings.StreamerName    = Math.abs(data.StreamerName);
			settings.GoalIncrement   = Math.abs(data.GoalIncrement);
			settings.GoalCap         = Math.abs(data.GoalCap);
			settings.Tier1           = Math.abs(data.Tier1);
			settings.Tier2           = Math.abs(data.Tier2);
			settings.Tier3           = Math.abs(data.Tier3);
			settings.InitialGoal     = settings.Goal;

			// Calculate current Goal
			settings.Goal += ((settings.Streak - 1) * settings.GoalIncrement);
			settings.SubsLeft = (settings.Goal - settings.Subs);

			// Sanity checks
			if(settings.GoalCap < settings.InitialGoal) { settings.GoalCap = settings.InitialGoal; }
			if(settings.Goal    > settings.GoalCap)     { settings.Goal    = settings.GoalCap; }
			if(settings.Tier1 < 1)                      { settings.Tier1   = 1; }
			if(settings.Tier2 < 1)                      { settings.Tier2   = 1; }
			if(settings.Tier3 < 1)                      { settings.Tier3   = 1; }

			calcStreak();
			Overlay.refresh();
			console.log('TwitchStreaker: Settings updated (System)');
			return;
		}

		// System Events (ignored events)
		var sysEvents = ['EVENT_CONNECTED'];
		if(socketMessage.event, sysEvents) { return; }

		// Unknown Events
		console.log('TwitchStreaker: Unknown Event "' + socketMessage.event + '" (System)');
	}
};

// Calculate Streak
function calcStreak() {
	while (settings.Subs >= settings.Goal) {
		settings.Subs    -= settings.Goal;
		if(settings.Goal  < settings.GoalCap) {
			settings.Goal += settings.GoalIncrement;
		}
		settings.SubsLeft = (settings.Goal - settings.Subs);
		settings.Streak++;
	}
}

// API Key Check
if (typeof API_Key === 'undefined' || typeof API_Socket === 'undefined') {
	document.body.innerHTML     = 'API Key not found!<br>Right-click on the TwitchStreaker Script in Streamlabs Chatbot and select "Insert API Key".';
	document.body.style.cssText = 'font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;';
	throw new Error('TwitchStreaker: API Key not loaded or missing.');
}
// Settings File Check
if (typeof settings === 'undefined') {
	document.body.innerHTML     = 'No Settings found!<br>Click on the TwitchStreaker Script in Streamlabs Chatbot and click "Save Settings".';
	document.body.style.cssText = 'font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;';
	throw new Error('TwitchStreaker: Settings file not loaded or missing.');
}
// New Settings Check
if (typeof settings.Tier1         === 'undefined' ||
	typeof settings.Tier2         === 'undefined' ||
	typeof settings.Tier3         === 'undefined' ||
	typeof settings.GoalIncrement === 'undefined' ||
	typeof settings.Goal          === "undefined" ||
	typeof settings.GoalCap       === "undefined") {
	document.body.innerHTML     = 'New set of Settings!<br>Please check the Script Settings and the Changelog, then click "Save Settings".';
	document.body.style.cssText = 'font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;';
	throw new Error('TwitchStreaker: Missing Settings.');
}

// Initialize Values
settings.Subs          = 0;
settings.Streak        = 1;
settings.Goal          = Math.abs(settings.Goal);
settings.Tier1         = Math.abs(settings.Tier1);
settings.Tier2         = Math.abs(settings.Tier2);
settings.Tier3         = Math.abs(settings.Tier3);
settings.GoalIncrement = Math.abs(settings.GoalIncrement);
settings.GoalCap       = Math.abs(settings.GoalCap);
settings.InitialGoal   = settings.Goal;
settings.SubsLeft      = settings.Goal;

// Sanity checks
if(settings.GoalCap < settings.InitialGoal) { settings.GoalCap = settings.InitialGoal; }
if(settings.Goal    > settings.GoalCap)     { settings.Goal    = settings.GoalCap; }
if(settings.Tier1   < 1)                    { settings.Tier1   = 1; }
if(settings.Tier2   < 1)                    { settings.Tier2   = 1; }
if(settings.Tier3   < 1)                    { settings.Tier3   = 1; }

// Connect Socket
connectWebsocket();

// Workaround for some browser plugins having issues with the initial draw
setTimeout(function() {
	Overlay.refresh();
	console.log('TwitchStreaker: Loaded (Init)');
}, 500);
