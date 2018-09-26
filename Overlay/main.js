// OverlayLogic
var Overlay = {

	// Elements
	'Streak': document.getElementById('Streak'),
	'Subs':   document.getElementById('Subs'),
	'Goal':   document.getElementById('Goal'),

	// Outline Hack!
	'Tracker': document.getElementById('Tracker'),

	// Refresh/Redraw
	'refresh': function() {
		// Calculate CurrentStreak and CurrentSubs (DO NOT REMOVE)
		while (settings.Subs >= settings.Goal) {
			settings.Subs    -= settings.Goal;
			settings.Goal    += settings.GoalIncrement;
			settings.Streak++;
		}

		// Update Overlay
		this.Streak.innerText = settings.Streak;
		this.Subs.innerText   = settings.Subs;
		this.Goal.innerText   = settings.Goal;

		// Outline Hack!
		this.Tracker.title = this.Tracker.innerText;
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
				Overlay.refresh();
				console.log('TwitchStreaker: New/Gift sub added (Sub)');
			}
			return;
		}

		// SubCounter Overwrite Events
		if(socketMessage.event == 'EVENT_ADD_SUB') {
			settings.Subs++;
			Overlay.refresh();
			console.log('TwitchStreaker: Added Sub (Overwrite)');
			return;
		}
		if(socketMessage.event == 'EVENT_SUBTRACT_SUB') {
			if(settings.Subs != 0) {
				settings.Subs--;
				Overlay.refresh();
				console.log('TwitchStreaker: Removed Sub (Overwrite)');
			}
			return;
		}

		// StreakCounter Overwrite Events
		if(socketMessage.event == 'EVENT_ADD_STREAK') {
			settings.Streak++;
			Overlay.refresh();
			console.log('TwitchStreaker: Added Streak (Overwrite)');
			return;
		}
		if(socketMessage.event == 'EVENT_SUBTRACT_STREAK') {
			if(settings.Streak != 1) {
				settings.Streak--;
				Overlay.refresh();
				console.log('TwitchStreaker: Removed Streak (Overwrite)');
			}
			return;
		}

		// StreakGoal Overwrite Events
		if(socketMessage.event == 'EVENT_ADD_TO_GOAL') {
			settings.Goal++;
			Overlay.refresh();
			console.log('TwitchStreaker: Added to Goal (Overwrite)');
			return;
		}
		if(socketMessage.event == 'EVENT_SUBTRACT_FROM_GOAL') {
			if(settings.Goal != 1) {
				settings.Goal--;
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
			settings.Goal   = initialGoal;

			Overlay.refresh();
			console.log('TwitchStreaker: Reset Tracker (Overwrite)');
			return;
		}

		// Update Settings Event
		if (socketMessage.event == 'EVENT_UPDATE_SETTINGS') {
			var data = JSON.parse(socketMessage.data);

			settings.Goal            = Math.abs(data.Goal);
			settings.StreamerName    = Math.abs(data.StreamerName);
			settings.GoalIncrement   = Math.abs(data.GoalIncrement);
			settings.Tier1           = Math.abs(data.Tier1);
			settings.Tier2           = Math.abs(data.Tier2);
			settings.Tier3           = Math.abs(data.Tier3);

			// Adjust SubsPerStreak based on CurrentStreak
			settings.Goal = (((settings.Streak - 1) * settings.GoalIncrement) + settings.Goal);

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
	typeof settings.Goal          === "undefined") {
	document.body.innerHTML     = 'New set of Settings!<br>Please check the Script Settings and the Changelog, then click "Save Settings".';
	document.body.style.cssText = 'font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;';
	throw new Error('TwitchStreaker: Missing Settings.');
}

// Initialize
connectWebsocket();
settings.Subs          = 0;
settings.Streak        = 1;
settings.Goal          = Math.abs(settings.Goal);
settings.Tier1         = Math.abs(settings.Tier1);
settings.Tier2         = Math.abs(settings.Tier2);
settings.Tier3         = Math.abs(settings.Tier3);
settings.GoalIncrement = Math.abs(settings.GoalIncrement);

// Backup for Reset
var initialGoal = settings.Goal;

// Workaround for some browser plugins having issues with the initial draw
setTimeout(function() {
	Overlay.refresh();
	console.log('TwitchStreaker: Loaded (Init)');
}, 500);
