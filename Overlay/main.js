/*****************
 * Overlay Logic *
 *****************/
var Overlay = {

	// Base Values
	'BitsLeft'      : 0,
	'Goal'          : 10,
	'Points'        : 0,
	'PointsLeft'    : 10,
	'Streak'        : 1,

	// BarValues
	'BarGoal': 100,
	'BarGoalCompleted': false,
	'BarSegmentPointsLeft': 25,
	'BarSegmentsCompleted': 0,

	// Point Values
	'BitPoints'     : 0,
	'DonationPoints': 0,
	'FollowPoints'  : 0,
	'SubPoints'     : 0,

	// Totals Values
	'TotalBits'     : 0,
	'TotalDonations': 0,
	'TotalFollows'  : 0,
	'TotalSubs'     : 0,

	// === Text Overlay ===
	'Text': {

		// Base Elements
		'eBitsLeft'      : document.getElementById('BitsLeft'),
		'eGoal'          : document.getElementById('Goal'),
		'ePoints'        : document.getElementById('Points'),
		'ePointsLeft'    : document.getElementById('PointsLeft'),
		'eStreak'        : document.getElementById('Streak'),

		// Point Elements
		'eBitPoints'     : document.getElementById('BitPoints'),
		'eDonationPoints': document.getElementById('DonationPoints'),
		'eFollowPoints'  : document.getElementById('FollowPoints'),
		'eSubPoints'     : document.getElementById('SubPoints'),

		// Totals Elements
		'eTotalBits'     : document.getElementById('TotalBits'),
		'eTotalDonations': document.getElementById('TotalDonations'),
		'eTotalFollows'  : document.getElementById('TotalFollows'),
		'eTotalSubs'     : document.getElementById('TotalSubs'),
		'eTracker'       : document.getElementById('Tracker'),          // ! Outline Hack!
	
		// Refresh, gets called for each Event coming through the EventBus
		'refresh': function() {
			// Base
			if (this.eBitsLeft)       this.eBitsLeft.innerText       = Overlay.BitsLeft;
			if (this.eGoal)           this.eGoal.innerText           = Overlay.Goal;
			if (this.ePoints)         this.ePoints.innerText         = Overlay.Points;
			if (this.ePointsLeft)     this.ePointsLeft.innerText     = Overlay.PointsLeft;
			if (this.eStreak)         this.eStreak.innerText         = Overlay.Streak;

			// Points
			if (this.eBitPoints)      this.eBitPoints.innerText      = Overlay.BitPoints;
			if (this.eDonationPoints) this.eDonationPoints.innerText = Overlay.DonationPoints;
			if (this.eFollowPoints)   this.eFollowPoints.innerText   = Overlay.FollowPoints;
			if (this.eSubPoints)      this.eSubPoints.innerText      = Overlay.SubPoints;

			// Totals
			if (this.eTotalBits)      this.eTotalBits.innerText      = Overlay.TotalBits;
			if (this.eTotalDonations) this.eTotalDonations.innerText = Overlay.TotalDonations;
			if (this.eTotalFollows)   this.eTotalFollows.innerText   = Overlay.TotalFollows;
			if (this.eTotalSubs)      this.eTotalSubs.innerText      = Overlay.TotalSubs;
			if (this.eTracker)        this.eTracker.title            = this.eTracker.innerText;     // ! Outline Hack!
		},

		// User Refresh
		'onrefresh': function() {}
	},

	// === Progress Bar ===
	'Bar': {
		// Base
		'SegmentCount' : 4,

		// Points
		'BitsEnabled'     : true,
		'DonationsEnabled': true,
		'FollowsEnabled'  : true,
		'SubsEnabled'     : true,

		// Internal
		'_width'     : '0px',
		'_pointWidth': '0px',

		'updateIndicators': function() {
			if (!(tmp = document.getElementById('Bar'))) { return; }
			var indicators = document.getElementsByClassName('Indicator');
			while (indicators[0]) { indicators[0].parentNode.removeChild(indicators[0]); }
			tmp.innerHTML += '<div class="Indicator"></div>'.repeat(this.SegmentCount - 1);

			indicators       = document.getElementsByClassName('Indicator');
			var segmentWidth = this._width / this.SegmentCount;
			var iter         = 1;

			for (var indicator of indicators) {
				_w = getContentWidth(indicator);
				indicator.style.cssText = 'Left:' + Math.floor(segmentWidth * iter) + 'px;';
				iter++;
			}
		},

		'refresh': function() {
			if (!(tmp = document.getElementById('Bar'))) { return; }

			this._width      = getContentWidth(tmp);
			this._pointWidth = this._width / Overlay.BarGoal;

			if (this.SubsEnabled) {
				document.getElementById('BarSubs').style.width      = Math.floor(this._pointWidth * Overlay.SubPoints) + 'px';
			}
			if (this.FollowsEnabled) {
				document.getElementById('BarFollows').style.width   = Math.floor(this._pointWidth * Overlay.FollowPoints) + 'px';
			}
			if (this.BitsEnabled) {
				document.getElementById('BarBits').style.width      = Math.floor(this._pointWidth * Overlay.BitPoints) + 'px';
			}
			if (this.DonationsEnabled) {
				document.getElementById('BarDonations').style.width = Math.floor(this._pointWidth * Overlay.DonationPoints) + 'px';
			}
		},

		// User Refresh
		'onrefresh': function() {}
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

				// Base Values
				Overlay.BitsLeft   = data.BitsLeft;
				Overlay.Goal       = data.Goal;
				Overlay.Points     = data.Points;
				Overlay.PointsLeft = data.PointsLeft;
				Overlay.Streak     = data.Streak;
			
				// BarValues
				Overlay.BarGoal              = data.BarGoal;
				Overlay.BarGoalCompleted     = data.BarGoalCompleted;
				Overlay.BarSegmentPointsLeft = data.BarSegmentPointsLeft;
				Overlay.BarSegmentsCompleted = data.BarSegmentsCompleted;
			
				// Point Values
				Overlay.BitPoints      = data.BitPoints;
				Overlay.DonationPoints = data.DonationPoints;
				Overlay.FollowPoints   = data.FollowPoints;
				Overlay.SubPoints      = data.SubPoints;
			
				// Totals Values
				Overlay.TotalBits      = data.TotalBits;
				Overlay.TotalDonations = data.TotalDonations;
				Overlay.TotalFollows   = data.TotalFollows;
				Overlay.TotalSubs      = data.TotalSubs;

				// Bar Specific
				Overlay.Bar.BitsEnabled      = data.BitsEnabled;
				Overlay.Bar.DonationsEnabled = data.DonationsEnabled;
				Overlay.Bar.FollowsEnabled   = data.FollowsEnabled;
				Overlay.Bar.SubsEnabled      = data.SubsEnabled;
				Overlay.Bar.SegmentCount     = data.SegmentCount;
		
				// Refresh Text
				Overlay.Text.refresh();
				Overlay.Text.onrefresh();

				// Refresh Bar
				Overlay.Bar.updateIndicators();
				Overlay.Bar.refresh();
				Overlay.Bar.onrefresh();
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
	Overlay.Text.refresh();
	Overlay.Bar.refresh();
	console.log('TwitchStreaker: Loaded (Init)');
}, 500);

function getContentWidth(element) {
	styles = getComputedStyle(element);
	return element.clientWidth - parseFloat(styles.paddingLeft) - parseFloat(styles.paddingLeft)
}
