# Changelog

## 3.0.0 - Segmented Progressbar

Brand new feature, segmented Progressbar! This feature adds a progressbar to the script, that will display the progress of the current streak in a bar format. In addition, you can segment the progressbar to allow for intermediate goals. Each type of Points has their own color and can be displayed in the progressbar.

As you might have guessed, this update will pretty much break everything. Please Backup the script folder before updating to the latest version! There are detailed instructions for updating from 2.x to 3.x in the README.md file.

* New ProgressBar Class
  * Added BarDisplayColors
  * Added BarGoal
  * Added BarSegmentCount
  * Added BarSegmentSize

* New Session Variables
  * Added BitPoints
  * Added DonationPoints
  * Added FollowPoints
  * Added SubPoints
  * Added TotalFollows

* New Script Settings
  * Added BarGoal field
  * Added BarDisplayColors
  * Added BarSegmentCount
  * Added CountFollows
  * Added FollowPointValue
  * Added SoundEnabled
  * Added SoundBarGoalCompleted
  * Added SoundBarGoalCompletedDelay
  * Added SoundBarSegmentCompleted
  * Added SoundBarSegmentCompletedDelay

* New Command Parameters
  * Added $tsBitPoints
  * Added $tsDonationPoints
  * Added $tsSubPoints

* Added `e` prefix for the html elements in the overlay
* Removed `Current` prefix from all Session variables
* Fixed Temp values not resetting when the session is reset
* Fixed Command parameter parsing

## 2.8.2 - More Fixes

* Fixed typo in README.md
* Added missing `BitsLeft` descriptions for several sections in the README.md
  * Functionality was implemented, but was not mentioned in the README.md

## 2.8.1 - Fixes and Cleanup

* Added Disclaimer regarding platform ToS to README.md
* Added CONTRIBUTING.md
* Added possible fix for (#38)
* Cleaned up Log messages
  * Removed messages that are not really needed
* Cleaned up globals declaration
* Changed constants are now using MACRO_CASE
* Changed Session and Settings into classes
  * This should prevent typos
* Simplified ParseString
* Fixed CurrentPointsLeft de-sync
* Fixed Links in the README.md and CHANGELOG.md
* Fixed Cumulative Bits being counted even when the option was disabled

## 2.8.0 - Youtube Superchats (Beta)

* Added support for Superchats (Beta)
  * The Donation Settings are used for Superchats
* Updated README.md
* Fixed potential bug when changing the SocketToken
* Optimized Tick function
* Optimized Event Function

## 2.7.3 - Bits and Donation Fixes

* Added BitsLeft Values for the Overlay and Command Variables
  * `BitsLeft` for HTML/JavaScript
  * `$BitsLeft` for Command Variables
* Fixed ID bug in EventReceiver library
* Fixed minimum bits/donation amount required being `Amount + 1`
* Fixed Bits/Donation calculation

## 2.7.2 - Updates

* Updated StreamlabsEventReceiver

## 2.7.1 - Bug Fixes

* Fixed Event Filtering

## 2.7.0 - RIP Mixer

* Added Event Filtering
  * This should prevent events from being counted more than once
* Removed Mixer support (for obvious reasons)
* Further shortened highly used variable names
* Slight restructure
* Session is no longer saved if the script is not ready yet
  * Should not cause any issues since no changes can happen at that time

## 2.6.1 - Events, Logs and Fixes

* Added logging to file
* Refined Log function
* EventMessages are no longer run through a loop, since there is only a single entry per event anyways
  * This should fix the doubling issue that can happen under rare circumstances
* Moved early resub check into the resub section
* Fixed using wrong temp variable for cumulative bits

## 2.6.0 - Bits and Donations

**IMPORTANT CHANGES!** We went ahead and changed a bunch of variables and terminology to reflect the changes we made to the script. In particular, how the Point-System works. `Points` is now used instead of Subs for the value that used to refer to the amount of Subs in the current Streak.

All this means that you need to save the Settings at least once and you should delete the `Session.json` file from the script folder. Changes you made to the Overlay have to be redone. And if you're using the text files, then you have to use `Points.txt` and `PointsLeft.txt` instead.

### Donation Changes

* Donations now use their own point value
* Introduced Cumulative Donations (Experimental)
  * Donations that are below the minimum amount are able to add up to a full DonationPoint

### Added Bits (Experimental)

* Bits have their own point value
* A minimum amount can be defined
* Bits below the minimum amount can add up to a full BitPoint (Experimental)

### Other Changes

* Updated README.md
* Updated Settings UI
* Improved path definitions
* Improved variable names
* Improved exception handling
* Improved log messages
* Added SaveText() to Unload()
* Added comments to important procedures
* Added automatic reconnect
* Added automatic reconnect in case the Token changes in the Settings
* Added UserRefresh to [main.js](Overlay/main.js)
  * This can be used in custom scripts as a trigger if the most recent are required for the script to function correctly. (See [README.md](README.md))
* Added skip for repeated alerts
* Added checks to keep point values above 0 (zero)
* Added Session cleanup
* Consolidated the Update functions into UpdateTracker()
* Consolidated the StartUp functions into StartUp()
* Consolidated GiftSubs and AnonGiftSubs
* Renamed some variables for more clarity
* Removed Library dependencies (see [2.5.2](https://github.com/BrainInBlack/TwitchStreaker/releases/tag/2.5.2))
* Removed instant update from the overwrite functions, to prevent ws-event throttling
* Removed unused Option from the script settings
* Fixed script not reconnecting when the token changed
* Fixed total subs command variable
* Fixed FileIO issues
* Fixed an Issue when changing Settings
* Fixed a potential issue with variables keeping their old value (Chatbot issue?)
* Fixed script error when SocketToken is not defined

## 2.5.6 - Improvements

* Improved script start
* Improved update functions
* Removed unused import
* Fixed load order
* Cleanup

## 2.5.5 - Improvements

* Fixed ReInit not setting the channel name
* Improved Settings CleanUp

## 2.5.4 - More Fixes

* Reverted the "fix" for Subs getting registered that aren't supposed to be tracked (2.5.3)

## 2.5.3 - Fixes

* Total Subs now reflect the amount of subs gathered, instead of the point value assigned to them
* Donations no longer have an impact on the Total Subs
* Load Functions now close the file-handler properly
* Fixed possible issue with Subs getting registered that are not supposed to be tracked

## 2.5.2 - Text Files

* Added text files for each value that is available in the Overlay (see Text Folder)
  * This allows for simple access to those values for other applications
  * Text files are updated every 5 seconds
* Removed UpdateOverlay from EventBus to prevent excess SocketEvents
  * This hopefully fixes the issue of the script breaking when a lot of subscriptions roll in at the same time
  * Overlay will update every 5 seconds
  * Overwrites will update instantly, as the did before the change
* Added Comments to the EventBus to make code navigation easier
* Simplified file and folder path declarations
* Added cleanup procedure for Settings, will remove no longer used Settings to keep the file clean (does not apply to Settings.js)

* Added Library dependencies (untested)
  * This should remove the requirement of changing the "Streamlabs Chatbot.exe.config" file
  * However, I was not able to test this for myself in a reliable manner, meaning that this might not work
  * Feedback is very welcome!

## 2.5.1 - Fixes

* Fixed Issue with the script not registering certain types/tiers of Subs
  * The last few Updates broke a bunch of stuff, everything should be fixed now
* Fixed Typo in Config UI

## 2.5.0 - Separated Subs

This Update requires you to redo your Settings. The new Feature required for a bunch of Settings to be renamed, to make more sense when viewed in the config file and source code.

* Changed how Subscriptions are counted for Twitch
  * Subscription Tiers now can be separated between gifted-subs and self-subs

## 2.4.1 - Fixes

* Script will attempt to re-initialize on a 5 second interval, to remove the need of reloading the script when the connection was lost.
* Script will abort the initialization, if the bot is not connected properly. (Undocumented Change from previous release)

## 2.4.0 - Tiered ReSubs

* Added Options to give resubs a separate value than new subs.
  * Resubs need to be enabled for this feature!
* Changed Init function to cancel if there are any issues that would prevent the script from running properly.

## 2.3.2 - Improvements

* Fixed Command parser only processing one keyword at a time
* Sanity Check now loads Settings if not loaded
* Added wrapper function for Log messages to prevent further mishaps

## 2.3.1 - Improved Donations

* Added Option to only count Donations once, regardless if they are a multiple of the minimum Donation amount.
* Script now checks if the bot is connected properly. (See LogMessages)
* LoadSettings now creates a Settings File in case there is none. Settings still have to be applied for the Script to work properly!
* Fixed Log Message using the wrong Variable
* Fixed another missed ScriptName Reference in LogMessages
* Fixed Overlay not updating after a Donation was processed

## 2.3.0 - Donations

* Added Donations to be counted as a sub, if they exceed a certain amount (Requested by BloodThunder)
  * A Donation of 12.00 with a specified amount of 5.00, will be counted as 2 Subs
* Fixed missing Script reference in Log Messages

## 2.2.2 - Improvements

* Added Return Statement to prevent Events from falling through
* Changed Session now saves every 5 minutes, instead of 5 seconds
* Changed some Variables to be easy to understand

## 2.2.1 - Logs

* Added Log message for each counted Subscription
* Removed TotalSubs from Overwrite Functions
* Fixed Overlay Refresh firing on each Loop (Mixer/YouTube)

## 2.2.0 - CleanUp

This Updates some things in the Settings and Session files, you might have to save the Settings at least once and reset the Tracker.

* Removed Option to include Follows (unused Feature)
* Added TotalSubs per Session
* Moved SubsLeft calculation into the python part
* Fixed SubsLeft in main.js
* Improved/Updated Documentation
* Minor Fixes and Cleanup

### Changed Overlay Files

* Overlay/main.js

*No update needed for the other Overlay Files and can be skipped.*

## 2.1.2 - Improvements

* Improved timed Overlay Update, this should finally fix the clogged EventBus
* Improved SanityCheck to save Session/Settings in case of value corrections

## 2.1.1 - Fixes and Improvements

* Changed at what point Sessions are saved to the disc
* Fixed Bug in Follower Mode
* Added Mixer and YouTube support (beta)

## 2.1.0 - Parameters

* Added Parameters for Commands ($tsGoal, $tsSubs, $tsSubsLeft, $tsStreak)
* Increased the Automated Overlay Update Delay to 5 seconds
* Reintroduced the UpdateOverlay function
* Updated README.md

## 2.0.2 - Fixes and Improvements

* Improved Type Checks
* Stopped using built-in names
* Improved Sanity Checks
* Added Comments to complex functions
* Added additional checks for the GoalIncrement mechanic
* Fixed Bug in the Resub detection

## 2.0.0 & 2.0.1 - General Rework

**IMPORTANT CHANGES!** A lot of things have changed with this rework. Amongst other things, your Subs and Streaks are now tracked across sessions and require a manual reset.

Please take your time and consult the README.md there you find a guide for upgrading to 2.x

* Moved core logic into the python part of the script for consistent tracking over multiple sessions (the reset is now done manually via the menu within the bot)
* Updated README.md
* Fixed SelfGiftSubs and StreamerSubs being detected incorrectly
* ~~Moved Refresh Overlay function into the python part, since it makes more sense there~~
* Optimized Session handling (reduces file IO)
* Added Timer based Refresh
* Removed manual Refresh
* Allowed Test Alerts to bypass all restrictions
* Removed UpdateOverlay function and moved it's functionality to the Tick function
* Fixed potential bug when initializing the script while CurrentSubs is at Zero, potentially reverting the CurrentGoal to the default Goal
* Fixed potential bug in the core logic

## 1.6.0 - Goal Rework

**Settings and Variables have changed! Please check your settings and save them at least once!**

* Added Min/Max Goal (Replaces the initial goal and goal cap mechanic)
* Added +-5 and +-10 variants for the Streaks Overwrites (speeds up crash recovery with a high Streak)

## 1.5.6 - Cumulative Subs

* Added Manual Mode Option (script will be entirely controlled by the overwrites if enabled)
* Improved EventBus
* Moved value calculations back into the refresh function
* Changed default design
* Fixed settings validation
* Fixed README.md

## 1.5.5 - SubsLeft Fix

* Fixed SubsLeft only being calculated when a Goal is reached
* Updated README.md

## 1.5.4 - Follower Fix

* Fixed inverted follower logic

## 1.5.3 - Resubs and Follows

* Added an options to count resubs as well as follows (default: off)
  * Resubs are worth as much as the respective Tier Value (min: 1)
  * Gifted Resubs will always count, as they did in previous versions
  * Follows, if enabled, are worth one point

## 1.5.2 - Flexible Design

* Added new value/element "SubsLeft", amount of subs needed to complete the next streak
* Changed how the refresh works, none of the values/elements are required for the script to work, allowing for a more flexible design

## 1.5.1 - Cleanup and Improvements

* Better sanity checks
* Minor fixes

## 1.5.0 - Better Naming Scheme

**Settings and Variables have changed!**

In an effort to make things a little more clear for everybody, we changed the names of pretty much all the variables. Those changes are reflected across the whole script, meaning that you have to re-apply your settings and customization's. This will hopefully the last time we make changes on this scale.

* Added cap to the incremental goals
* Renamed variables
* Updated README.md
* Streamlined main.js
* Minor improvements and fixes

## 1.4.6 - Growing Streaks

* Added new Streak Growth Mechanic

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

* Added multiplier for tiered subs (default: 1), thanks to [KatLink](https://twitch.tv/KatLink) for the idea
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
