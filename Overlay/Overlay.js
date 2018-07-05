$(document).ready(function () {

	// API Key Check
	if (typeof API_Key === "undefined") {
		$("body").html("No API Key found<br>Rightclick on the script in Streamlabs Chatbot and select \"Insert API Key\"");
		$("body").css({ "font-size": "20px", "color": "#ff8080", "text-align": "center" });
		return;
	}
	// Settings File Check
	if (typeof settings === "undefined") {
		$("body").html("No Settings found<br>Click on the script in Streamlabs Chatbot and click \"Save Settings\"");
		$("body").css({ "font-size": "20px", "color": "#ff8080", "text-align": "center" });
		return;
	}

	// Init
	connectWebsocket();
	settings.CurrentSubs = 0;
	settings.CurrentStreak = 1;
	Overlay.refesh(); // Force redraw to prevent a strange issue with some browser plugins
});

function connectWebsocket() {
	var socket = new WebSocket("ws://127.0.0.1:3337/streamlabs");

	// Connect/Reconnect
	socket.onopen = function () {
		var auth = {
			author: "BrainInBlack",
			website: "https://github.com/BrainInBlack/TwitchStreaker",
			api_key: API_Key,
			events: [
				"EVENT_SUB",
				"EVENT_UPDATE_SETTINGS",
				"EVENT_REFRESH_OVERLAY",
				"EVENT_ADD_SUB",
				"EVENT_SUBTRACT_SUB",
				"EVENT_ADD_STREAK",
				"EVENT_SUBTRACT_STREAK"
			]
		};
		socket.send(JSON.stringify(auth));
	};
	socket.onclose = function () {
		socket = null;
		setTimeout(connectWebsocket, 5000);
	}

	// EventBus
	socket.onmessage = function (message) {
		var socketMessage = JSON.parse(message.data);

		// Subscription Event
		if (socketMessage.event == "EVENT_SUB") {
			var data = JSON.parse(socketMessage.data);
			// Ignore GiftSubs made by the streamer
			if (data.display_name.toLowerCase() == settings.StreamerName.toLowerCase()) {
				return;
			}
			// Check if GiftSub or NewSub (ignores Self-GiftSubs)
			if ((data.is_gift && (data.display_name.toLowerCase() != data.gift_target.toLowerCase())) || !data.is_resub) {
				Overlay.addSub();
				Overlay.refesh();
			}
			return;
		}

		// Custom Overwrite Events
		if(socketMessage.event == "EVENT_ADD_SUB") {
			Overlay.addSub();
			Overlay.refesh();
			return;
		}
		if(socketMessage.event == "EVENT_SUBTRACT_SUB") {
			if(settings.CurrentSubs != 0) {
				settings.CurrentSubs--;
			}
			Overlay.refesh();
			return;
		}
		if(socketMessage.event == "EVENT_ADD_STREAK") {
			settings.CurrentStreak++;
			Overlay.refesh();
			return;
		}
		if(socketMessage.event == "EVENT_SUBTRACT_STREAK") {
			if(settings.CurrentStreak >= 2) {
				settings.CurrentStreak--;
			}
			Overlay.refesh();
			return;
		}

		// ForceRedraw
		/*if (socketMessage.event == "EVENT_REFRESH_OVERLAY") {<
			Overlay.refesh();
			return;
		}*/

		// Update Settings
		if (socketMessage.event == "EVENT_UPDATE_SETTINGS") {
			var data = JSON.parse(socketMessage.data);
			settings.SubsPerStreak = data.SubsPerStreak;
			settings.StreamerName = data.StreamerName;
			Overlay.refesh();
			return;
		}
	}
};

var Overlay = {
	'Container': $("#Container"),
	'CurrentStreak': $("#CurrentStreak"),
	'CurrentSubs': $("#CurrentSubs"),
	'SubsPerStreak': $("#SubsPerStreak"),

	// Redraw
	'refesh': function() {
		Overlay.CurrentStreak.html(settings.CurrentStreak);
		Overlay.CurrentSubs.html(settings.CurrentSubs);
		Overlay.SubsPerStreak.html(settings.SubsPerStreak);
		Overlay.Container.prop('title', Overlay.Container.text());
	},

	// Increment Sub
	'addSub': function() {
		settings.CurrentSubs++;
		if (settings.CurrentSubs >= settings.SubsPerStreak) {
			settings.CurrentSubs = 0;
			settings.CurrentStreak++;
		}
	}
}
