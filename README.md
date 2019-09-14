# TwitchStreaker for Streamlabs Chatbot

Initially created for the Twitch-Streamer [AnEternalEnigma](http://twitch.tv/AnEternalEnigma) to keep track of new and gifted subscriptions to his channel. This is the public version of the same exact script, with some minor changes to make it a little more generic.

## Table of Contents

- [TwitchStreaker for Streamlabs Chatbot](#twitchstreaker-for-streamlabs-chatbot)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Updates](#updates)
  - [Updating to 2.x from 1.x](#updating-to-2x-from-1x)
  - [Streamlabs SocketToken](#streamlabs-sockettoken)
  - [Known Issues](#known-issues)
    - [Script not showing up after Installation/Update](#script-not-showing-up-after-installationupdate)
  - [Chatbot Command Parameters](#chatbot-command-parameters)
  - [Customization](#customization)
  - [JavaScript Variables](#javascript-variables)
  - [Manual Overwrites](#manual-overwrites)
  - [Support](#support)
  - [Streamers using TwitchStreaker](#streamers-using-twitchstreaker)
  - [Contributing](#contributing)
  - [Contributor's](#contributors)
  - [Project Info](#project-info)

## Installation

1. Download the [latest release](http://github.com/BrainInBlack/TwitchStreaker/releases/latest).
2. Extract the downloaded archive into the```Chatbot > Services > Scripts``` directory.
3. In Chatbot, open the Scripts Tab and click the ```Reload Scripts``` button.
4. Right click on the ```TwitchStreaker``` script and click ```Insert API Key```.
5. Enter your ```SocketToken``` and the amount of subs required per streak. [See here](#streamlabs-sockettoken)
6. Add the [Overlay.html](Overlay.html) as Browser Source to your scene in your preferred streaming software.
   - Recommended Browser Source width: ```800px```

## Updates

**Remember to Backup your customized files!**

1. Download the [latest release](http://github.com/BrainInBlack/TwitchStreaker/releases/latest).
2. Extract the downloaded archive and overwrite existing files.
3. Check the [Changelog](CHANGELOG.md) for additional instructions
4. Reapply your customization's.
5. Reload the script and overlay.

## Updating to 2.x from 1.x

With version 2.0.0 and onwards the Tracking is done in a different part of the Script, allowing us to track Subs and Streaks across multiple Sessions and different Overlays. All that without having to worry about loosing progress when switching Scenes or having the Chatbot crash on you.

1. Make a Backup of the entire folder.
2. Extract the 2.x archive and overwrite existing files.
3. Delete ```Settings.js```and ```Settings.json``` from the folder.
4. Enter your ```SocketToken``` [See here](#streamlabs-sockettoken).
5. Reapply your Settings and Customizations.
   - Modifications to the Script have to be redone, since most of the logic has been removed from the JavaScript part.
6. Save the Settings

## Streamlabs SocketToken

1. Navigate to [Streamlabs API Settings](https://streamlabs.com/dashboard#/settings/api-settings)
2. Click on ```API Tokens```
3. Click the ```Copy``` Button next to the ```Your Socket API Token``` field
4. Insert the Token under ```Streamlabs > Socket Token``` in the Script Settings

## Known Issues

### Script not showing up after Installation/Update

With version 2.x and onwards we're using an additional library that, depending on your system, needs additional libraries to work correctly. These libraries are usually downloaded as needed, but this process is blocked by the system for security reasons. The following steps will remedy this issue.

1. Open `Streamlabs Chatbot.exe.config` (Chatbot main folder) with a Text Editor
2. Add `<loadFromRemoteSources enabled="true"/>` in a new line after `<runtime>`.
3. Save and Restart the Chatbot

## Chatbot Command Parameters

You can use the following Parameters in your Commands and Timers:

Parameter | Description
----------|------------
$tsGoal | Amount of Subs needed per Streak
$tsSubs | Current amount of Subs in the current Streak
$tsSubsLeft | Amount of Subs needed to complete the current Streak
$tsStreak | Current Streak
$tsTotalSubs | Amount of Subs accumulated in the current Session

### Example

- Command: `We are currently working on Streak #$tsStreak and need $tsSubsLeft additional Subs.`
- Result: `We are currently working on Streak #5 and need 6 additional Subs.`

## Customization

Making your own designs for TwitchStreaker is straight forward and only require a few things to keep in mind. The single most important thing is to load the required JavaScript files in the correct order.

```HTML
<html>
  <head>
    <!-- OtherStuff -->
    <script src="API_Key.js"></script>
    <script src="overlay/main.js" defer></script>
    <!-- OtherScripts -->
  </head>
  <body>
    <!-- Content -->
  </body>
</html>
```

The following element ID's are available for use in your design:

ID | Description
---|------------
Goal | Amount of Subs needed per Streak
Subs | Current amount of Subs in the current Streak
SubsLeft | Amount of Subs needed to complete the current Streak
Streak | Current Streaks
TotalSubs | Amount of Subs accumulated in the current Session

None of those ID's are required and can be placed anywhere in the document, in case of the default design we're only using ```Subs```, ```Streak``` and ```Goal```. Here a few examples:

### "X Subs left until Wheel #1"

```HTML
<div><span id="SubsLeft">2</span> Subs left until Wheel #<span id="Streak">1</span></div>
```

### "X of X Subs, then we spin Wheel #1"

```HTML
<div><span id="Subs">2</span> of <span id="Goal">7</span> Subs, then we spin Wheel #<span id="Streak">1</span></div>
```

The rest is just CSS and your own creativity.

## JavaScript Variables

Variable | Description
---------|------------
Overlay.CurrentGoal | Amount of Subs needed to complete a Streak (min: 1)
Overlay.CurrentStreak | Current amount Streaks (min: 1)
Overlay.CurrentSubs | Current amount of Subs in the Streak (min: 0)
Overlay.CurrentSubsLeft | Amount of subs left to the next Streak
Overlay.CurrentTotalSubs | Amount of Subs accumulated in the current Session

## Manual Overwrites

If something can go wrong, it will most like go wrong at some point. That's why the script has some overwrite functions built in to account for missed subs, streaks, and outright crashes.

Button | Functionality
-------|--------------
\+ Sub | Adds a Sub, Streaks will increment if conditions are met.
\- Sub | Removes a Sub, until 0 (zero) is reached.
\+ Streak | Adds a Streak.
\- Streak | Removes a Streak, until 1 (one) is reached.
\+ Goal | Increments the Goal by one.
\- Goal | Decrements the Goal by one, until 1 (one) is reached.
Refresh Overlay | Refreshes the Overlay without loosing the current values.
Reset Tracker | Resets everything to their initial values.

## Support

[Discord](https://discord.gg/HWTaady)

[Twitter](http://twitter.com/BrainInBlack)

## Streamers using TwitchStreaker

[**AnEternalEnigma**](http://twitch.tv/AnEternalEnigma)

[**BloodThunder**](http://twitch.tv/BloodThunder)

[**KatLink**](http://twitch.tv/KatLink)

[**PersonSuit**](http://twitch.tv/PersonSuit)

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Contributor's

[**BrainInBlack**](https://github.com/BrainInBlack) - Programming

[**AnEternalEnigma**](http://twitch.tv/AnEternalEnigma) - Initial Concept

## Project Info

[GNU GPL-3.0 License](LICENSE.md)

[Changelog](CHANGELOG.md)
