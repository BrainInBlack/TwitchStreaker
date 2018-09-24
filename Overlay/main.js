// OverlayLogic
var Overlay = {

	// Elements
	'CurrentStreak': document.getElementById('CurrentStreak'),
	'CurrentSubs': document.getElementById('CurrentSubs'),
	'SubsPerStreak': document.getElementById('SubsPerStreak'),

	// Outline Hack!
	'Container': document.getElementById('Tracker'),

	// Refresh/Redraw
	'refresh': function() {
		// Calculate CurrentStreak and CurrentSubs (DO NOT REMOVE)
		while (settings.CurrentSubs >= settings.SubsPerStreak) {
			settings.CurrentSubs = (settings.CurrentSubs - settings.SubsPerStreak);
			settings.SubsPerStreak = (settings.SubsPerStreak + settings.StreakIncrement);
			settings.CurrentStreak++;
		}

		// Update Overlay
		this.CurrentStreak.innerText = settings.CurrentStreak;
		this.CurrentSubs.innerText = settings.CurrentSubs;
		this.SubsPerStreak.innerText = settings.SubsPerStreak;

		// Outline Hack!
		this.Container.title = this.Container.innerText;
	}
}

// MainLogic
function connectWebsocket() {
	var socket = new WebSocket(API_Socket);

	// Connect to Socket and register Events
	socket.onopen = function () {
		var auth = {
			author: 'BrainInBlack',
			website: 'https://github.com/BrainInBlack/TwitchStreaker',
			api_key: API_Key,
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
		setTimeout(connectWebsocket, 5000);
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
					case '3': settings.CurrentSubs = settings.CurrentSubs + settings.Tier3; break;
					case '2': settings.CurrentSubs = settings.CurrentSubs + settings.Tier2; break;
					default:  settings.CurrentSubs = settings.CurrentSubs + settings.Tier1;
				}
				Overlay.refresh();
				console.log('TwitchStreaker: New/Gift sub added (Sub)');
			}
			return;
		}

		// SubCounter Overwrite Events
		if(socketMessage.event == 'EVENT_ADD_SUB') {
			settings.CurrentSubs++;
			Overlay.refresh();
			console.log('TwitchStreaker: Added Sub (Overwrite)');
			return;
		}
		if(socketMessage.event == 'EVENT_SUBTRACT_SUB') {
			if(settings.CurrentSubs != 0) {
				settings.CurrentSubs--;
				Overlay.refresh();
				console.log('TwitchStreaker: Removed Sub (Overwrite)');
			}
			return;
		}

		// StreakCounter Overwrite Events
		if(socketMessage.event == 'EVENT_ADD_STREAK') {
			settings.CurrentStreak++;
			Overlay.refresh();
			console.log('TwitchStreaker: Added Streak (Overwrite)');
			return;
		}
		if(socketMessage.event == 'EVENT_SUBTRACT_STREAK') {
			if(settings.CurrentStreak != 1) {
				settings.CurrentStreak--;
				Overlay.refresh();
				console.log('TwitchStreaker: Removed Streak (Overwrite)');
			}
			return;
		}

		// StreakGoal Overwrite Events
		if(socketMessage.event == 'EVENT_ADD_TO_GOAL') {
			settings.SubsPerStreak++;
			Overlay.refresh();
			console.log('TwitchStreaker: Added to Goal (Overwrite)');
			return;
		}
		if(socketMessage.event == 'EVENT_SUBTRACT_FROM_GOAL') {
			if(settings.SubsPerStreak != 1) {
				settings.SubsPerStreak--;
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
			settings.CurrentStreak = 1;
			settings.CurrentSubs = 0;
			settings.SubsPerStreak = initialGoal;
			Overlay.refresh();
			console.log('TwitchStreaker: Reset Tracker (Overwrite)');
			return;
		}

		// Update Settings Event
		if (socketMessage.event == 'EVENT_UPDATE_SETTINGS') {
			var data = JSON.parse(socketMessage.data);
			settings.SubsPerStreak = data.SubsPerStreak;
			settings.StreamerName = data.StreamerName;
			settings.StreakIncrement = data.StreakIncrement;
			settings.Tier1 = data.Tier1;
			settings.Tier2 = data.Tier2;
			settings.Tier3 = data.Tier3;
			settings.SubsPerStreak = (((settings.CurrentStreak - 1) * settings.StreakIncrement) + settings.SubsPerStreak);
			Overlay.refresh();
			console.log('TwitchStreaker: Settings updated');
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
	document.body.innerHTML = 'API Key not found!<br>Right-click on the TwitchStreaker Script in Streamlabs Chatbot and select "Insert API Key".';
	document.body.style.cssText = 'font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;';
	throw new Error('TwitchStreaker: API Key not loaded or missing.');
}
// Settings File Check
if (typeof settings === 'undefined') {
	document.body.innerHTML = 'No Settings found!<br>Click on the TwitchStreaker Script in Streamlabs Chatbot and click "Save Settings".';
	document.body.style.cssText = 'font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;';
	throw new Error('TwitchStreaker: Settings file not loaded or missing.');
}
// New Settings Check
if (typeof settings.Tier1 === 'undefined' ||
	typeof settings.Tier2 === 'undefined' ||
	typeof settings.Tier3 === 'undefined' ||
	typeof settings.StreakIncrement === 'undefined') {
	document.body.innerHTML = 'New set of Settings!<br>Please check the Script Settings and the Changelog, then click "Save Settings".';
	document.body.style.cssText = 'font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;';
	throw new Error('TwitchStreaker: Missing Settings.');
}

// Initialize
connectWebsocket();
settings.CurrentSubs = 0;
settings.CurrentStreak = 1;
var initialGoal = settings.SubsPerStreak;

// Workaround for some browser plugins having issues with the initial draw
setTimeout(function() {
	Overlay.refresh();
	console.log('TwitchStreaker: Loaded (Init)');
}, 500);
