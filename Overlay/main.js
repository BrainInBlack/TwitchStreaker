/*****************
 * Overlay Logic *
 *****************/
var Overlay = {

	'CurrentGoal':          10,
	'CurrentStreak':         1,
	'CurrentPoints':         0,
	'CurrentPointsLeft':    10,
	'CurrentTotalSubs':      0,
	'CurrentTotalBits':      0,
	'CurrentTotalDonations': 0,

	// Elements
	'Goal':           document.getElementById('Goal'),
	'Points':         document.getElementById('Points'),
	'PointsLeft':     document.getElementById('PointsLeft'),
	'Streak':         document.getElementById('Streak'),
	'TotalSubs':      document.getElementById('TotalSubs'),
	'TotalBits':      document.getElementById('TotalBits'),
	'TotalDonations': document.getElementById('TotalDonations'),
	'Tracker':        document.getElementById('Tracker'),                                    // ! Outline Hack!

	// Refresh, gets called for each Event coming through the EventBus
	'refresh': function() {
		if (this.Goal)           this.Goal.innerText           = this.CurrentGoal;
		if (this.Points)         this.Points.innerText         = this.CurrentPoints;
		if (this.PointsLeft)     this.PointsLeft.innerText     = this.CurrentPointsLeft;
		if (this.Streak)         this.Streak.innerText         = this.CurrentStreak;
		if (this.TotalSubs)      this.TotalSubs.innerText      = this.CurrentTotalSubs;
		if (this.TotalBits)      this.TotalBits.innerText      = this.CurrentTotalBits;
		if (this.TotalDonations) this.TotalDonations.innerText = this.CurrentTotalDonations;
		if (this.Tracker)        this.Tracker.title            = this.Tracker.innerText;     // ! Outline Hack!
	},

	// User Refresh is triggered every refresh
	'onrefresh': function() {}

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
				Overlay.CurrentGoal           = data.CurrentGoal;
				Overlay.CurrentStreak         = data.CurrentStreak;
				Overlay.CurrentPoints         = data.CurrentPoints;
				Overlay.CurrentPointsLeft     = data.CurrentPointsLeft;
				Overlay.CurrentTotalSubs      = data.CurrentTotalSubs;
				Overlay.CurrentTotalBits      = data.CurrentTotalBits;
				Overlay.CurrentTotalDonations = data.CurrentTotalDonations;
				break;

			default:
				if(socketMessage.event, ['EVENT_CONNECTED']) { return; }
				console.warn('TwitchStreaker: Unknown Event "' + socketMessage.event + '" (System)');
				return;
		}
		Overlay.refresh();
		Overlay.onrefresh();
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
