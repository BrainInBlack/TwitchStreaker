$(document).ready(function () {
	if (typeof API_Key === "undefined") {
		$("body").html("No API Key found<br>Rightclick on the script in Streamlabs Chatbot and select \"Insert API Key\"");
		$("body").css({ "font-size": "20px", "color": "#ff8080", "text-align": "center" });
		return;
	}
	if (typeof settings === "undefined") {
		$("body").html("No Settings found<br>Click on the script in Streamlabs Chatbot and click \"Save Settings\"");
		$("body").css({ "font-size": "20px", "color": "#ff8080", "text-align": "center" });
		return;
	}
	connectWebsocket();
});

function connectWebsocket() {
	var socket = new WebSocket("ws://127.0.0.1:3337/streamlabs");
	socket.onopen = function () {
		var auth = {
			author: "BrainInBlack",
			website: "http://www.twitch.tv/BrainInBlack",
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
	socket.onmessage = function (message) {
		var socketMessage = JSON.parse(message.data);
		if (socketMessage.event == "EVENT_SUB") {
			var data = JSON.parse(socketMessage.data);
			if (data.is_gift || !data.is_resub) {
				if (data.display_name.toLowerCase() != settings.StreamerName.toLowerCase()) {
					Overlay.addSub();
					Overlay.refesh();
				}
			}
		}
		if(socketMessage.event == "EVENT_ADD_SUB") {
			Overlay.addSub();
			Overlay.refesh();
		}
		if(socketMessage.event == "EVENT_SUBTRACT_SUB") {
			if(settings.CurrentSubs != 0) {
				settings.CurrentSubs--;
			}
			Overlay.refesh();
		}
		if(socketMessage.event == "EVENT_ADD_STREAK") {
			settings.CurrentStreak++;
			Overlay.refesh();
		}
		if(socketMessage.event == "EVENT_SUBTRACT_STREAK") {
			if(settings.CurrentStreak >= 2) {
				settings.CurrentStreak--;
			}
			Overlay.refesh();
		}
		if (socketMessage.event == "EVENT_UPDATE_SETTINGS") {
			var data = JSON.parse(socketMessage.data);
			settings.CurrentSubs = data.CurrentSubs;
			settings.CurrentStreak = data.CurrentStreak;
			settings.SubsPerStreak = data.SubsPerStreak;
			settings.StreamerName = data.StreamerName;
			Overlay.refesh();
		}
		if (socketMessage.event == "EVENT_REFRESH_OVERLAY") {
			Overlay.refesh();
		}
	}
};

var Overlay = {
	'CurrentStreak': $("#CurrentStreak"),
	'CurrentSubs': $("#CurrentSubs"),
	'SubsPerStreak': $("#SubsPerStreak"),
	'refesh': function() {
		Overlay.CurrentStreak.html(settings.CurrentStreak);
		Overlay.CurrentSubs.html(settings.CurrentSubs);
		Overlay.SubsPerStreak.html(settings.SubsPerStreak);
	},
	'addSub': function() {
		settings.CurrentSubs++;
		if (settings.CurrentSubs >= settings.SubsPerStreak) {
			settings.CurrentSubs = 0;
			settings.CurrentStreak++;
		}
	},
	'subtractSub': function() {
	}
}
