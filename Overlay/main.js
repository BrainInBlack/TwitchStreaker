/*****************
 * Overlay Logic *
 *****************/
var Overlay = {

	// Elements
	'Streak':   document.getElementById('Streak'),
	'Subs':     document.getElementById('Subs'),
	'SubsLeft': document.getElementById('SubsLeft'),
	'Goal':     document.getElementById('Goal'),
	'Tracker':  document.getElementById('Tracker'),                             // ! Outline Hack!

	// Refresh, gets called for each Event coming through the EventBus
	'refresh': function() {
		if(this.Streak)   this.Streak.innerText   = settings.Streak;
		if(this.Subs)     this.Subs.innerText     = settings.Subs;
		if(this.SubsLeft) this.SubsLeft.innerText = settings.SubsLeft;
		if(this.Goal)     this.Goal.innerText     = settings.Goal;
		if(this.Tracker)  this.Tracker.title      = this.Tracker.innerText;     // ! Outline Hack!
	}
}

/*****************
 * Tracker Logic *
 *****************/
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
				'EVENT_FOLLOW',
				'EVENT_UPDATE_SETTINGS',

				// Sub Events
				'EVENT_ADD_SUB',
				'EVENT_SUBTRACT_SUB',

				// Streak Events
				'EVENT_ADD_STREAK',
				'EVENT_ADD_STREAK_5',
				'EVENT_ADD_STREAK_10',
				'EVENT_SUBTRACT_STREAK',
				'EVENT_SUBTRACT_STREAK_5',
				'EVENT_SUBTRACT_STREAK_10',

				// Goal Events
				'EVENT_ADD_TO_GOAL',
				'EVENT_SUBTRACT_FROM_GOAL',

				// Misc Events
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
		console.warn('TwitchStreaker: Reconnecting (Socket)');
	}
	// Output errors to the console (only works in a browser)
	socket.onerror = function(error) {
		console.error('Error: ' + error + ' (System)');
	}

	// EventBus
	socket.onmessage = function (message) {
		var socketMessage = JSON.parse(message.data);

		switch (socketMessage.event) {
			case 'EVENT_SUB':
				if(settings.ManualMode) return;
				var data = JSON.parse(socketMessage.data);

				if(data.display_name.toLowerCase() == settings.StreamerName.toLowerCase()) return;
				if(data.is_gift && (data.display_name.toLowerCase() == data.gift_target.toLowerCase())) return;
				if(!settings.CountResubs && data.is_resub && !data.is_gift) return;

				switch(data.tier) {
					case '3': settings.Subs += settings.Tier3; break;
					case '2': settings.Subs += settings.Tier2; break;
					default:  settings.Subs += settings.Tier1;
				}
				console.log('TwitchStreaker: Sub added (Sub)');
				break;

			case 'EVENT_FOLLOW':
				if(!settings.CountFollows) return;
				settings.Subs++;
				console.log('TwitchStreaker: Follow added (Follow)');
				break;

			case 'EVENT_ADD_SUB':
				settings.Subs++;
				console.log('TwitchStreaker: Added Sub (Overwrite)');
				break;
			case 'EVENT_SUBTRACT_SUB':
				if(settings.Subs > 0) {
					settings.Subs--;
					console.log('TwitchStreaker: Removed Sub (Overwrite)');
				} else { return; } // Return if no change
				break;

			case 'EVENT_ADD_STREAK':
				settings.Streak++;
				console.log('TwitchStreaker: Added Streak (Overwrite)');
				break;
			case 'EVENT_ADD_STREAK_5':
				settings.Streak += 5;
				console.log('TwitchStreaker: Added 5 Streaks (Overwrite)');
				break;
			case 'EVENT_ADD_STREAK_10':
				settings.Streak += 10;
				console.log('TwitchStreaker: Added 10 Streaks (Overwrite)');
				break;

			case 'EVENT_SUBTRACT_STREAK':
				if(settings.Streak > 1) {
					settings.Streak--;
					console.log('TwitchStreaker: Removed Streak (Overwrite)');
				} else { return; } // Return if no change
				break;
			case 'EVENT_SUBTRACT_STREAK_5':
				if(settings.Streak > 5) {
					settings.Streak -= 5;
					console.log('TwitchStreaker: Removed 5 Streaks (Overwrite)');
				} else { return; } // Return if no change
				break;
			case 'EVENT_SUBTRACT_STREAK_10':
				if(settings.Streak > 10) {
					settings.Streak -= 10;
					console.log('TwitchStreaker: Removed 10 Streaks (Overwrite)');
				} else { return; } // Return if no change
				break;

			case 'EVENT_ADD_TO_GOAL':
				if(settings.Goal < settings.GoalMax) {
					settings.Goal++;
					console.log('TwitchStreaker: Added to Goal (Overwrite)');
				} else { return; } // Return if no change
				break;
			case 'EVENT_SUBTRACT_FROM_GOAL':
				if(settings.Goal > settings.GoalMin) {
					settings.Goal--;
					console.log('TwitchStreaker: Subtracted from Goal (Overwrite)');
				} else { return; } // Return if no change
				break;

			case 'EVENT_FORCE_REDRAW': // Will fall through the redraw call!
				console.log('TwitchStreaker: Force Redraw (Overwrite)');
				break;

			case 'EVENT_RESET':
				settings.Streak = 1;
				settings.Subs   = 0;
				settings.Goal   = settings.InitialGoal;
				console.log('TwitchStreaker: Reset Tracker (Overwrite)');
				break;

			case 'EVENT_UPDATE_SETTINGS':
				var data = JSON.parse(socketMessage.data);

				// Assign new values and ensure positive numbers
				settings.Goal            = Math.abs(data.Goal);
				settings.StreamerName    = Math.abs(data.StreamerName);
				settings.GoalIncrement   = Math.abs(data.GoalIncrement);
				settings.GoalMin         = Math.abs(data.GoalMin);
				settings.GoalMax         = Math.abs(data.GoalMax);
				settings.Tier1           = Math.abs(data.Tier1);
				settings.Tier2           = Math.abs(data.Tier2);
				settings.Tier3           = Math.abs(data.Tier3);
				settings.CountFollows    = data.CountFollows;
				settings.CountResubs     = data.CountResubs;
				settings.ManualMode      = data.ManualMode;
				settings.InitialGoal     = settings.Goal;

				// Calculate current Goal
				settings.Goal += ((settings.Streak - 1) * settings.GoalIncrement);

				sanityCheck();

				console.log('TwitchStreaker: Settings updated (System)');
				break;

			default:
				var sysEvents = ['EVENT_CONNECTED'];
				if(socketMessage.event, sysEvents) { return; }

				console.warn('TwitchStreaker: Unknown Event "' + socketMessage.event + '" (System)');
				return;
		}
		settings.SubsLeft = (settings.Goal - settings.Subs);

		// Calculate Current Values
		while (settings.Subs >= settings.Goal) {
			settings.Subs    -= settings.Goal;
			if(settings.Goal  < settings.GoalMax) {
				settings.Goal += settings.GoalIncrement;
			}
			settings.Streak++;
		}
		Overlay.refresh();
	}
};

// Sanity Check
function sanityCheck() {
	if(settings.GoalMin < 1)                    { settings.GoalMin = 1; }
	if(settings.GoalMin > settings.InitialGoal) { settings.GoalMin = settings.InitialGoal; }
	if(settings.GoalMax < settings.InitialGoal) { settings.GoalMax = settings.InitialGoal; }
	if(settings.Goal    > settings.GoalMax)     { settings.Goal    = settings.GoalMax; }
	if(settings.Tier1   < 1)                    { settings.Tier1   = 1; }
	if(settings.Tier2   < 1)                    { settings.Tier2   = 1; }
	if(settings.Tier3   < 1)                    { settings.Tier3   = 1; }
}

/***************
 * Entry Point *
 ***************/

// API File Check
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
// Settings Check
if (typeof settings.Tier1         === 'undefined' ||
	typeof settings.Tier2         === 'undefined' ||
	typeof settings.Tier3         === 'undefined' ||
	typeof settings.GoalIncrement === 'undefined' ||
	typeof settings.Goal          === "undefined" ||
	typeof settings.GoalMin       === "undefined" ||
	typeof settings.GoalMax       === "undefined" ||
	typeof settings.CountResubs   === "undefined" ||
	typeof settings.CountFollows  === "undefined" ||
	typeof settings.ManualMode    === "undefined") {
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
settings.GoalMin       = Math.abs(settings.GoalMin);
settings.GoalMax       = Math.abs(settings.GoalMax);
settings.InitialGoal   = settings.Goal;

sanityCheck();
connectWebsocket();

// Workaround for some browser plugins having issues with the initial draw
setTimeout(function() {
	Overlay.refresh();
	console.log('TwitchStreaker: Loaded (Init)');
}, 500);
