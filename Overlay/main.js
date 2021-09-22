/*****************
 * Overlay Logic *
 *****************/
var Overlay = {

	// === Text Overlay ===
	'Text': {
		'BitsLeft'      : 0,
		'BitPoints'     : 0,
		'DonationPoints': 0,
		'Goal'          : 10,
		'Streak'        : 1,
		'SubPoints'     : 1,
		'Points'        : 0,
		'PointsLeft'    : 10,
		'TotalSubs'     : 0,
		'TotalBits'     : 0,
		'TotalDonations': 0,
	
		// Elements
		// TODO: Implement follows
		'eBitsLeft'      : document.getElementById('BitsLeft'),
		'eBitPoints'     : document.getElementById('BitPoints'),
		'eDonationPoints': document.getElementById('DonationPoints'),
		'eGoal'          : document.getElementById('Goal'),
		'ePoints'        : document.getElementById('Points'),
		'ePointsLeft'    : document.getElementById('PointsLeft'),
		'eStreak'        : document.getElementById('Streak'),
		'eSubPoints'     : document.getElementById('SubPoints'),
		'eTotalSubs'     : document.getElementById('TotalSubs'),
		'eTotalBits'     : document.getElementById('TotalBits'),
		'eTotalDonations': document.getElementById('TotalDonations'),
		'eTracker'       : document.getElementById('Tracker'),          // ! Outline Hack!
	
		// Refresh, gets called for each Event coming through the EventBus
		// TODO: Implement follows
		'refresh': function() {
			if (this.eBitsLeft)       this.eBitsLeft.innerText       = this.BitsLeft;
			if (this.eBitPoints)      this.eBitPoints.innerText      = this.BitPoints;
			if (this.eGoal)           this.eGoal.innerText           = this.Goal;
			if (this.ePoints)         this.ePoints.innerText         = this.Points;
			if (this.ePointsLeft)     this.ePointsLeft.innerText     = this.PointsLeft;
			if (this.eStreak)         this.eStreak.innerText         = this.Streak;
			if (this.eTotalSubs)      this.eTotalSubs.innerText      = this.TotalSubs;
			if (this.eTotalBits)      this.eTotalBits.innerText      = this.TotalBits;
			if (this.eTotalDonations) this.eTotalDonations.innerText = this.TotalDonations;
			if (this.eTracker)        this.eTracker.title            = this.eTracker.innerText;     // ! Outline Hack!
		},

		// User Refresh
		'onrefresh': function() {}
	},

	// === Progress Bar ===
	'Bar': {
		'DisplayColors' : true,
		'Goal'          : 100,
		'SegmentCount'  : 4,
		'SegmentSize'   : 25,
		'BitPoints'     : 0,
		'DonationPoints': 0,
		'SubPoints'     : 0,
	
		'refresh': function() {
			// TODO: Implement
		},

		// User Refresh
		'onrefresh':  function() {}
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
				'EVENT_UPDATE_OVERLAY',
				'EVENT_UPDATE_BAR'
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
			case 'EVENT_UPDATE_BAR':  // TODO: Complete separation
				var data = JSON.parse(socketMessage.data);
				Overlay.Bar.DisplayColors  = data.DisplayColors;
				Overlay.Bar.Goal           = data.Goal;
				Overlay.Bar.SegmentCount   = data.SegmentCount;
				Overlay.Bar.SegmentSize    = data.SegmentSize;

				Overlay.Bar.BitPoints      = data.BitPoints;
				Overlay.Bar.DonationPoints = data.DonationPoints;
				Overlay.Bar.SubPoints      = data.SubPoints;

				Overlay.Bar.refresh();
				Overlay.Bar.onrefresh();
				break
			case 'EVENT_UPDATE_OVERLAY':  // TODO: Implement follows
				var data = JSON.parse(socketMessage.data);
				Overlay.Text.BitsLeft       = data.BitsLeft;
				Overlay.Text.BitPoints      = data.BitPoints;
				Overlay.Text.DonationPoints = data.DonationPoints;
				Overlay.Text.Goal           = data.Goal;
				Overlay.Text.Streak         = data.Streak;
				Overlay.Text.SubPoints      = data.SubPoints;
				Overlay.Text.Points         = data.Points;
				Overlay.Text.PointsLeft     = data.PointsLeft;
				Overlay.Text.TotalSubs      = data.TotalSubs;
				Overlay.Text.TotalBits      = data.TotalBits;
				Overlay.Text.TotalDonations = data.TotalDonations;
				Overlay.Text.refresh();
				Overlay.Text.onrefresh();
				break;

			default:
				if(socketMessage.event, ['EVENT_CONNECTED']) { return; }
				console.warn('TwitchStreaker: Unknown Event "' + socketMessage.event + '" (System)');
				return;
		}
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
	Overlay.refreshText();
	console.log('TwitchStreaker: Loaded (Init)');
}, 500);
