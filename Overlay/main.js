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
	var socket = new WebSocket("ws://127.0.0.1:3337/streamlabs");

	// Connect to Socket and register Events
	socket.onopen = function () {
		var auth = {
			author: "BrainInBlack",
			website: "https://github.com/BrainInBlack/TwitchStreaker",
			api_key: API_Key,
			events: [
				"EVENT_SUB",
				"EVENT_UPDATE_SETTINGS",
				"EVENT_ADD_SUB",
				"EVENT_SUBTRACT_SUB",
				"EVENT_ADD_STREAK",
				"EVENT_SUBTRACT_STREAK",
				"EVENT_FORCE_REDRAW",
				"EVENT_RESET"
			]
		};
		socket.send(JSON.stringify(auth));
		console.log("TwitchStreaker: Connected (Socket)");
	};
	// Attempt reconnect after connection loss
	socket.onclose = function () {
		socket = null;
		setTimeout(connectWebsocket, 5000);
		console.log("TwitchStreaker: Reconnecting (Socket)");
	}
	// Output errors to the console (only works in a browser)
	socket.onerror = function(error) {
		console.log("Error: " + error + " (System)")
	}

	// EventBus
	socket.onmessage = function (message) {
		var socketMessage = JSON.parse(message.data);

		// Subscription Event
		if (socketMessage.event == "EVENT_SUB") {
			var data = JSON.parse(socketMessage.data);
			// Check if new or gifted subscription, and ignore subscription by streamer
			if (((data.is_gift && (data.display_name.toLowerCase() != data.gift_target.toLowerCase())) || !data.is_resub) &&
				(data.display_name.toLowerCase() != settings.StreamerName.toLowerCase())) {
				// Tier Multiplier
				switch(data.tier) {
					case "3":
						settings.CurrentSubs = settings.CurrentSubs + settings.Tier3;
						break;
					case "2":
						settings.CurrentSubs = settings.CurrentSubs + settings.Tier2;
						break;
					default:
						settings.CurrentSubs = settings.CurrentSubs + settings.Tier1;
				}
				Overlay.refresh();
				console.log("TwitchStreaker: New/Gift sub added (Sub)");
			}
			return;
		}

		// SubCounter Overwrite Events
		if(socketMessage.event == "EVENT_ADD_SUB") {
			settings.CurrentSubs++;
			Overlay.refresh();
			console.log("TwitchStreaker: Added Sub (Overwrite)");
			return;
		}
		if(socketMessage.event == "EVENT_SUBTRACT_SUB") {
			if(settings.CurrentSubs != 0) {
				settings.CurrentSubs--;
				Overlay.refresh();
				console.log("TwitchStreaker: Removed Sub (Overwrite)");
			}
			return;
		}

		// StreakCounter Overwrite Events
		if(socketMessage.event == "EVENT_ADD_STREAK") {
			settings.CurrentStreak++;
			Overlay.refresh();
			console.log("TwitchStreaker: Added Streak (Overwrite)");
			return;
		}
		if(socketMessage.event == "EVENT_SUBTRACT_STREAK") {
			if(settings.CurrentStreak != 1) {
				settings.CurrentStreak--;
				Overlay.refresh();
				console.log("TwitchStreaker: Removed Streak (Overwrite)");
			}
			return;
		}

		// Redraw Overwrite Event
		if(socketMessage.event == "EVENT_FORCE_REDRAW") {
			Overlay.refresh();
			console.log("TwitchStreaker: Force Redraw (Overwrite)");
			return;
		}

		// Reset Overwrite Event
		if(socketMessage.event == "EVENT_RESET") {
			settings.CurrentStreak = 1;
			settings.CurrentSubs = 0;
			Overlay.refresh();
			console.log("TwitchStreaker: Reset Tracker (Overwrite)");
			return;
		}

		// Update Settings Event
		if (socketMessage.event == "EVENT_UPDATE_SETTINGS") {
			var data = JSON.parse(socketMessage.data);
			settings.SubsPerStreak = data.SubsPerStreak;
			settings.StreamerName = data.StreamerName;
			settings.Tier1 = data.Tier1;
			settings.Tier2 = data.Tier2;
			settings.Tier3 = data.Tier3;
			Overlay.refresh();
			console.log("TwitchStreaker: Settings updated");
			return;
		}

		// System Events (ignored events)
		var sysEvents = ['EVENT_CONNECTED'];
		if(socketMessage.event, sysEvents) { return; }

		// Unknown Events
		console.log("Unknown Event \"" + socketMessage.event + "\" (System)");
	}
};

// API Key Check
if (typeof API_Key === "undefined") {
	document.body.innerHTML = "No API Key found!<br>Right-click on the script in Streamlabs Chatbot and select \"Insert API Key\"";
	document.body.style.cssText = "font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;";
	throw new Error("API Key not loaded or missing.");
}
// Settings File Check
if (typeof settings === "undefined") {
	document.body.innerHTML = "No Settings found!<br>Click on the script in Streamlabs Chatbot and click \"Save Settings\"";
	document.body.style.cssText = "font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;";
	throw new Error("Settings file not loaded or missing.");
}
// Tier Multiplier Check
if (typeof settings.Tier1 === "undefined" || typeof settings.Tier2 === "undefined" || typeof settings.Tier3 === "undefined") {
	document.body.innerHTML = "New Sub Tier Multiplier!<br>Please check the script settings and and click \"Save Settings\"";
	document.body.style.cssText = "font-family: sans-serif; font-size: 20pt; font-weight: bold; color: rgb(255, 22, 23); text-align: center;";
	throw new Error("Sub Tier Settings not set.");
}

// Initialize
connectWebsocket();
settings.CurrentSubs = 0;
settings.CurrentStreak = 1;

// Workaround for some browser plugins having issues with the initial draw
setTimeout(function() {
	Overlay.refresh();
	console.log("TwitchStreaker: Loaded (Init)"
);}, 500);
