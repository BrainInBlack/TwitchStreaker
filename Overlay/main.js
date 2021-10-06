/*****************
 * Overlay Logic *
 *****************/
var Overlay = {

	// === Text Overlay ===
	'Text': {
		// Base Values
		'BitsLeft'      : 0,
		'FollowsLeft'   : 10,
		'Goal'          : 10,
		'Points'        : 0,
		'PointsLeft'    : 10,
		'Streak'        : 1,
		
		// Point Values
		'BitPoints'     : 0,
		'DonationPoints': 0,
		'FollowPoints'  : 0,
		'SubPoints'     : 1,
		
		// Totals Values
		'TotalBits'     : 0,
		'TotalDonations': 0,
		'TotalFollows'  : 0,
		'TotalSubs'     : 0,
	
		// Base Elements
		'eBitsLeft'      : document.getElementById('BitsLeft'),
		'eFollowsLeft'   : document.getElementById('FollowsLeft'),
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
			if (this.eBitsLeft)       this.eBitsLeft.innerText       = this.BitsLeft;
			if (this.eFollowsLeft)    this.eFollowsLeft.innerText    = this.FollowsLeft;
			if (this.eGoal)           this.eGoal.innerText           = this.Goal;
			if (this.ePoints)         this.ePoints.innerText         = this.Points;
			if (this.ePointsLeft)     this.ePointsLeft.innerText     = this.PointsLeft;
			if (this.eStreak)         this.eStreak.innerText         = this.Streak;

			// Points
			if (this.eBitPoints)      this.eBitPoints.innerText      = this.BitPoints;
			if (this.eDonationPoints) this.eDonationPoints.innerText = this.DonationPoints;
			if (this.eFollowPoints)   this.eFollowPoints.innerText   = this.FollowPoints;
			if (this.eSubPoints)      this.eSubPoints.innerText      = this.SubPoints;

			// Totals
			if (this.eTotalBits)      this.eTotalBits.innerText      = this.TotalBits;
			if (this.eTotalDonations) this.eTotalDonations.innerText = this.TotalDonations;
			if (this.eTotalFollows)   this.eTotalFollows.innerText   = this.TotalFollows;
			if (this.eTotalSubs)      this.eTotalSubs.innerText      = this.TotalSubs;
			if (this.eTracker)        this.eTracker.title            = this.eTracker.innerText;     // ! Outline Hack!
		},

		// User Refresh
		'onrefresh': function() {}
	},

	// === Progress Bar ===
	'Bar': {
		// Base
		'Goal'          : 100,
		'SegmentCount'  : 4,
		'SegmentSize'   : 25,

		// Points
		'BitPoints'       : 0,
		'BitsEnabled'     : true,
		'DonationPoints'  : 0,
		'DonationsEnabled': true,
		'FollowPoints'    : 0,
		'FollowsEnabled'  : true,
		'SubPoints'       : 0,
		'SubsEnabled'     : true,

		'_width': '0px',
		'_pointWidth': '0px',
		'_finished': false,

		'updateIndicators': function() {
			document.getElementById('Bar').innerHTML += '<div class="Indicator"></div>'.repeat(this.SegmentCount - 1);

			var indicators   = document.getElementsByClassName('Indicator');
			var segmentWidth = this._width / this.SegmentCount;
			var iter         = 1;

			for (var indicator of indicators) {
				_w = getContentWidth(indicator);
				indicator.style.cssText = 'Left:' + Math.floor(segmentWidth * iter) + 'px;';
				iter++;
			}
		},

		'refresh': function() {
			this._width          = getContentWidth(document.getElementById('Bar'));
			this._pointWidth     = this._width / this.Goal;

			if (this._finished === true) {return};

			var sum = 0;

			if (this.SubsEnabled) {
				document.getElementById('BarSubs').style.width = Math.floor(this._pointWidth * this.SubPoints) + 'px';
				sum += this.SubPoints;
			}
			if (this.FollowsEnabled) {
				document.getElementById('BarFollows').style.width = Math.floor(this._pointWidth * this.FollowPoints) + 'px';
				sum += this.FollowPoints;
			}
			if (this.BitsEnabled) {
				document.getElementById('BarBits').style.width = Math.floor(this._pointWidth * this.BitPoints) + 'px';
				sum += this.BitPoints;
			}
			if (this.DonationsEnabled) {
				document.getElementById('BarDonations').style.width = Math.floor(this._pointWidth * this.DonationPoints) + 'px';
				sum += this.DonationPoints;
			}

			this._finished = (sum >= this.Goal);
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
			case 'EVENT_UPDATE_OVERLAY':
				var data = JSON.parse(socketMessage.data);
				// Base
				Overlay.Text.BitsLeft       = data.BitsLeft;
				Overlay.Text.FollowsLeft    = data.FollowsLeft;
				Overlay.Text.Goal           = data.Goal;
				Overlay.Text.Streak         = data.Streak;
				Overlay.Text.Points         = data.Points;
				Overlay.Text.PointsLeft     = data.PointsLeft;
		
				// Points
				Overlay.Text.BitPoints      = data.BitPoints;
				Overlay.Text.DonationPoints = data.DonationPoints;
				Overlay.Text.FollowPoints   = data.FollowPoints;
				Overlay.Text.SubPoints      = data.SubPoints;
		
				// Totals
				Overlay.Text.TotalBits      = data.TotalBits;
				Overlay.Text.TotalDonations = data.TotalDonations;
				Overlay.Text.TotalFollows   = data.TotalFollows;
				Overlay.Text.TotalSubs      = data.TotalSubs;
		
				// Refresh
				Overlay.Text.refresh();
				Overlay.Text.onrefresh();
				break;

			case 'EVENT_UPDATE_BAR':
				var data = JSON.parse(socketMessage.data);
				// Base
				Overlay.Bar.Goal             = data.Goal;
				if (data.SegmentCount != Overlay.Bar.SegmentCount) {
					Overlay.Bar.SegmentCount = data.SegmentCount;
					Overlay.Bar.updateIndicators();
				} else {
					Overlay.Bar.SegmentCount = data.SegmentCount;
				}
				Overlay.Bar.SegmentSize      = data.SegmentSize;
				
				// Points
				Overlay.Bar.BitPoints        = data.BitPoints;
				Overlay.Bar.BitsEnabled      = data.BitsEnabled;
				Overlay.Bar.DonationPoints   = data.DonationPoints;
				Overlay.Bar.DonationsEnabled = data.DonationsEnabled;
				Overlay.Bar.FollowPoints     = data.FollowPoints;
				Overlay.Bar.FollowsEnabled   = data.FollowsEnabled;
				Overlay.Bar.SubPoints        = data.SubPoints;
				Overlay.Bar.SubsEnabled      = data.SubsEnabled;
				
				// Refresh
				Overlay.Bar.refresh();
				Overlay.Bar.onrefresh();
				break

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
