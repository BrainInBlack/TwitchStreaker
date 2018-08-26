# Changelog

## 1.2.2 - Structure Rework Phase III

* Removed minimized CSS (HTML/CSS/JS)

## 1.2.1 - Structure Rework Phase II

**Elements got renamed!** If you're using custom styling, you'll have to redo those customizations. In the future there will be a different way to customize the Overlay.

* Renamed Container into Tracker (HTML/CSS/JS)
* Moved StreamerName and SubsPerStreak option out of groups (chatbot)

## 1.2.0 - Structure Rework (IMPORTANT CHANGES)

**This version breaks a lot of things!** The Overlay was moved to the main folder, and the settings file got renamed. Meaning you have to redo your settings and change your Overlay in your streaming software of choice. Just point the browser plugin to the "Overlay.html" file in the **main folder**.

* Reorganized and renamed files
* Added "Refresh" overwrite to resolve eventual render issues
* Moved redraws where they are actually needed
* Modified log messages to be a little clearer
* Fixed system events are handled now, unknown events will be logged to the console

## 1.1.0 - Errors and Resets

* Added log messages for easier troubleshooting
* Added reset button
* Removed residue of the "ForceRedraw" workaround
* Minor changes and improvements

## 1.0.10 - Minor Improvements

* Removed timed redraw
* Improved styling
* Minor fixes

## 1.0.9 - Fixing Stuff

* Added subtract buttons for subs/streaks
* Reduced default glow

## 1.0.8 - Primary Release

* First public release attempt

## 1.0.7 - Repo Init

* Initialized the Repo and added the existing files
