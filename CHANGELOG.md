# Changelog

## 1.4.5 - Fixes

* Added Exception prefix
* Changed now using API_Socket dynamic variable from the API_Key.js
* Improved initialization error messages
* Fixed single and double quotes consistency

## 1.4.4 - Project Maintenance

* Fixed default font-size causing issues with the recommended browser source width of 800px
* Updated BugReport template
* Updated README.md
* Added explanations to .gitignore
* Added .version to the repo, might be useful for contributors
* Added GitHub specific files
* Removed .gitattributes, no longer required

## 1.4.3 - Minor Update

* Added/Changed check for new/changed settings
* Changed styling (external change)
* Improved how archives are generated (external change)
* Minor fixes and formatting

## 1.4.2 - New Build System

* Updated README.md
* Changed default styling to be more generic
* Changed default phrase to be more generic
* Changed default font to Roboto
* Removed CSS map files
* Fixed several typos
* Minor changes to account for the new build system

## 1.4.1 - Fixes

* Fixed Save Settings was not applying the Tier Multipliers

## 1.4.0 - Tier Multipliers

**Click "Save Settings" at least once!** Otherwise the script wont work as intended.

* Added multiplier for tiered subs (default: 1), thanks to [KatLink](http://twitch.tv/KatLink) for the idea
* Streak calculation moved to refresh(), less overhead
* Fixed reset setting the current streak to 0 instead of 1
* Changed streak calculation, now able to calculate multiple streaks at once

## 1.3.0 - Goodbye jQuery

* Removed jQuery
* Locked down font sizes
* Added delay for initial redraw

## 1.2.2 - Structure Rework Phase III

* Removed minimized CSS (HTML/CSS/JS)

## 1.2.1 - Structure Rework Phase II

**Elements got renamed!** If you're using custom styling, you'll have to redo those customization's. In the future there will be a different way to customize the Overlay.

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
