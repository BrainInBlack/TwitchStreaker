function connectWebsocket() {
	var socket = new WebSocket("ws://127.0.0.1:3337/streamlabs");

	// DefaultEvents
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
	socket.onclose = function () {
		socket = null;
		setTimeout(connectWebsocket, 5000);
		console.log("TwitchStreaker: Reconnecting (Socket)");
	}
	socket.onerror = function(error) {
		console.log("Error: " + error + " (System)")
	}

	// EventBus
	socket.onmessage = function (message) {
		var socketMessage = JSON.parse(message.data);

		// Subscription Event
		if (socketMessage.event == "EVENT_SUB") {
			var data = JSON.parse(socketMessage.data);
			// Check if GiftSub or NewSub (ignores Self-GiftSubs)
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
				Overlay.refesh();
				console.log("TwitchStreaker: New/Gift sub added (Sub)");
			}
			return;
		}

		// CustomEvents
		if(socketMessage.event == "EVENT_ADD_SUB") {
			settings.CurrentSubs++;
			Overlay.refesh();
			console.log("TwitchStreaker: Added Sub (Overwrite)");
			return;
		}
		if(socketMessage.event == "EVENT_SUBTRACT_SUB") {
			if(settings.CurrentSubs != 0) {
				settings.CurrentSubs--;
				Overlay.refesh();
				console.log("TwitchStreaker: Removed Sub (Overwrite)");
			}
			return;
		}
		if(socketMessage.event == "EVENT_ADD_STREAK") {
			settings.CurrentStreak++;
			Overlay.refesh();
			console.log("TwitchStreaker: Added Streak (Overwrite)");
			return;
		}
		if(socketMessage.event == "EVENT_SUBTRACT_STREAK") {
			if(settings.CurrentStreak >= 2) {
				settings.CurrentStreak--;
				Overlay.refesh();
				console.log("TwitchStreaker: Removed Streak (Overwrite)");
			}
			return;
		}
		if(socketMessage.event == "EVENT_FORCE_REDRAW") {
			Overlay.refesh();
			console.log("TwitchStreaker: Force Redraw (Overwrite)");
			return;
		}
		if(socketMessage.event == "EVENT_RESET") {
			settings.CurrentStreak = 1;
			settings.CurrentSubs = 0;
			Overlay.refesh();
			console.log("TwitchStreaker: Reset Tracker (Overwrite)");
			return;
		}

		// Update Settings
		if (socketMessage.event == "EVENT_UPDATE_SETTINGS") {
			var data = JSON.parse(socketMessage.data);
			settings.SubsPerStreak = data.SubsPerStreak;
			settings.StreamerName = data.StreamerName;
			Overlay.refesh();
			console.log("TwitchStreaker: Settings updated");
			return;
		}

		// System Events (ignored events)
		var sysEvents = ['EVENT_CONNECTED'];
		if(socketMessage.event, sysEvents) { return; }

		// Unknown Event
		console.log("Unknown Event \"" + socketMessage.event + "\" (System)");
	}
};

var Overlay = {
	'Container': document.getElementById('Tracker'),
	'CurrentStreak': document.getElementById('CurrentStreak'),
	'CurrentSubs': document.getElementById('CurrentSubs'),
	'SubsPerStreak': document.getElementById('SubsPerStreak'),

	// Redraw
	'refesh': function() {
		while (settings.CurrentSubs >= settings.SubsPerStreak) {
			settings.CurrentSubs = (settings.CurrentSubs - settings.SubsPerStreak);
			settings.CurrentStreak++;
		}
		this.CurrentStreak.innerText = settings.CurrentStreak;
		this.CurrentSubs.innerText = settings.CurrentSubs;
		this.SubsPerStreak.innerText = settings.SubsPerStreak;

		// Outline Hack, remove when there are better methods for outlined text!
		this.Container.title = this.Container.innerText;
	}
}

// API Key Check
if (typeof API_Key === "undefined") {
	document.body.innerHTML = "No API Key found!<br>Rightclick on the script in Streamlabs Chatbot and select \"Insert API Key\"";
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

// Init
connectWebsocket();
settings.CurrentSubs = 0;
settings.CurrentStreak = 1;

// defer seems to be ignored by OBS and probably other browser plugins
setTimeout(function() {
	Overlay.refesh();
	console.log("TwitchStreaker: Loaded (Init)"
);}, 500);
