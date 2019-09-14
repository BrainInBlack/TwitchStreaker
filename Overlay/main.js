/*****************
 * Overlay Logic *
 *****************/
var Overlay = {

	'CurrentGoal': 10,
	'CurrentStreak': 1,
	'CurrentSubs': 0,
	'CurrentSubsLeft': 10,
	'CurrentTotalSubs': 0,

	// Elements
	'Goal':      document.getElementById('Goal'),
	'Subs':      document.getElementById('Subs'),
	'SubsLeft':  document.getElementById('SubsLeft'),
	'Streak':    document.getElementById('Streak'),
	'TotalSubs': document.getElementById('TotalSubs'),
	'Tracker':   document.getElementById('Tracker'),                             // ! Outline Hack!

	// Refresh, gets called for each Event coming through the EventBus
	'refresh': function() {
		if(this.Goal)      this.Goal.innerText      = this.CurrentGoal;
		if(this.Subs)      this.Subs.innerText      = this.CurrentSubs;
		if(this.SubsLeft)  this.SubsLeft.innerText  = this.CurrentSubsLeft;
		if(this.Streak)    this.Streak.innerText    = this.CurrentStreak;
		if(this.TotalSubs) this.TotalSubs.innerText = this.CurrentTotalSubs;
		if(this.Tracker)   this.Tracker.title       = this.Tracker.innerText;     // ! Outline Hack!
	}
}

/**********************
 * Chatbot Connection *
 **********************/
function connectWebsocket() {
	var socket = new WebSocket(API_Socket);

	// Connect to Socket and register Events
	socket.onopen = function () {
		socket.send(JSON.stringify({
			author:  'BrainInBlack',
			website: 'https://github.com/BrainInBlack/TwitchStreaker',
			api_key:  API_Key,
			events: [
				'EVENT_UPDATE_OVERLAY'
			]
		}));
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
			case 'EVENT_UPDATE_OVERLAY':
				var data = JSON.parse(socketMessage.data);
				Overlay.CurrentGoal      = data.CurrentGoal;
				Overlay.CurrentStreak    = data.CurrentStreak;
				Overlay.CurrentSubs      = data.CurrentSubs;
				Overlay.CurrentSubsLeft  = data.CurrentSubsLeft;
				Overlay.CurrentTotalSubs = data.CurrentTotalSubs
				break;

			default:
				if(socketMessage.event, ['EVENT_CONNECTED']) { return; }
				console.warn('TwitchStreaker: Unknown Event "' + socketMessage.event + '" (System)');
				return;
		}
		Overlay.refresh();
	}
};

// API File Check
if (typeof API_Key === 'undefined' || typeof API_Socket === 'undefined') {
	document.body.innerHTML     = 'API Key not found!<br>Right-click on the TwitchStreaker Script in Streamlabs Chatbot and select "Insert API Key".';
	document.body.style.cssText = 'font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;';
	throw new Error('TwitchStreaker: API Key not loaded or missing.');
}

connectWebsocket();

// Workaround for some browser plugins having issues with the initial draw
setTimeout(function() {
	Overlay.refresh();
	console.log('TwitchStreaker: Loaded (Init)');
}, 500);
