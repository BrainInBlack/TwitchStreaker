# TwitchStreaker for Streamlabs Chatbot

Initially created for the Twitch-Streamer [AnEternalEnigma](http://twitch.tv/AnEternalEnigma) to keep track of new and gifted subscriptions to his channel. This is the public version of the same exact script, with some minor changes to make it a little more generic.

TwitchStreaker is compatible with Twitch and YouTube. For YouTube, only the regular Subscription options apply.

## Table of Contents

- [TwitchStreaker for Streamlabs Chatbot](#twitchstreaker-for-streamlabs-chatbot)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Updates](#updates)
  - [Updating from 1.x to 2.x](#updating-from-1x-to-2x)
  - [Streamlabs SocketToken](#streamlabs-sockettoken)
  - [Known Issues](#known-issues)
    - [Script not showing up after Installation/Update](#script-not-showing-up-after-installationupdate)
  - [Settings](#settings)
    - [General](#general)
    - [Bits](#bits)
    - [Donations](#donations)
    - [Subscription Values](#subscription-values)
    - [Streamlabs](#streamlabs)
  - [Chatbot Command Parameters](#chatbot-command-parameters)
    - [Command Example](#command-example)
  - [Customization](#customization)
    - [HTML Elements](#html-elements)
    - [HTML Examples](#html-examples)
  - [JavaScript](#javascript)
    - [Setup](#setup)
    - [Variables](#variables)
  - [Manual Overwrites](#manual-overwrites)
  - [Support](#support)
  - [Streamers using TwitchStreaker](#streamers-using-twitchstreaker)
  - [Contributing](#contributing)
  - [Contributor's](#contributors)
  - [Project Info](#project-info)

## Installation

1. Download the [latest release](http://github.com/BrainInBlack/TwitchStreaker/releases/latest).
2. Extract the downloaded archive into the `Chatbot > Services > Scripts` directory.
3. In the Chatbot, open the Scripts Tab and click the `Reload Scripts` button.
4. Right click on the `TwitchStreaker` script and click `Insert API Key`.
5. Enter your `SocketToken` and the amount of subs required per streak. [See here](#streamlabs-sockettoken)
6. Add the [Overlay.html](Overlay.html) as Browser Source to your scene in your preferred streaming software.
   - Recommended Browser Source width: `800px`
   - You can use the text files contained within the `Text` folder as an alternative

## Updates

**Remember to Backup your customized files!**

1. Download the [latest release](http://github.com/BrainInBlack/TwitchStreaker/releases/latest).
2. Check the [Changelog](CHANGELOG.md) for additional instructions
3. Extract the downloaded archive and overwrite existing files.
4. Reapply your customization's.
5. Reload the script and overlay.
   - Click the `Reload Script` button on the Chatbot.
   - De-select and then re-select the script, to update the UI.
   - Click the `Save Settings` and then the `Reset Session` button, to makes sure that the most recent changes are applied.
   - Reload the Overlay within your Streaming software.

## Updating from 1.x to 2.x

With version 2.0.0 and onwards the Tracking is done in a different part of the Script, allowing us to track Subs and Streaks across multiple Sessions and different Overlays. All that without having to worry about loosing progress when switching Scenes or having the Chatbot crash on you.

1. Make a Backup of the entire folder.
2. Extract the 2.x archive and overwrite existing files.
3. Delete `Settings.js` and `Settings.json` from the folder.
4. Enter your `SocketToken` [See here](#streamlabs-sockettoken).
5. Reapply your Settings and Customizations.
   - Modifications to the Script have to be redone, since most of the logic has been removed from the JavaScript part.
6. Save the Settings

## Streamlabs SocketToken

1. Navigate to [Streamlabs API Settings](https://streamlabs.com/dashboard#/settings/api-settings)
2. Click on `API Tokens`
3. Click the `Copy` Button next to the `Your Socket API Token` field
4. Insert the Token under `Streamlabs > Socket Token` in the Script Settings

## Known Issues

### Script not showing up after Installation/Update

1. Open `Streamlabs Chatbot.exe.config` in Chatbot main folder, with a Text Editor
   - `Right click` > `Open file location` on the Chatbot shortcut brings you right to the Chatbot main folder
2. Add `<loadFromRemoteSources enabled="true"/>` in a new line after `<runtime>`
3. Save and Start/Restart the Chatbot

Additional information available [here](https://github.com/BrainInBlack/TwitchStreaker/issues/38)

## Settings

TwitchStreaker has a lot of Options to give you as much control as possible on how the script works for you. For example you can make your `Goal` increase over time, or allow Donations to be counted as `Points` when they exceed a specified amount.

### General

Option            | Description
------------------|------------
Goal              | The amount of `Points` required for the next Streak.
Goal Min          | Minimum value of the `Goal` option (Defaults to the value of `Goal` when above the `Goal`)
Goal Max          | Maximum value of the `Goal` option (Defaults to the value of `Goal` when above the `Goal`)
Increment Goal By | Value by which the `Goal` will be increased when completing a Streak (Leave at `0` to disable this mechanic)
Allow Resubs      | Allows Resubs to be counted as well as regular Subs.

### Bits

Option           | Description
-----------------|------------
Bits Amount      | Minimum amount of Bits required for it to be counted.
Bits Point Value | Amount of `Points` awarded.
Allow Bits       | Enables Bits to be counted as `Points` if they exceed the `Bits Amount`.
Count Bits Once  | Counts Bits only once, even if they exceed the `Bits Amount`.
Cumulative Bits  | Allows Bits below the `Bits Amount` to pile up and add `Points` if the exceed the `Bits Amount`.

### Donations

Option               | Description
---------------------|------------
Donation Amount      | Minimum Donation required for it to be counted.
Donation Point Value | Amount of `Points` awarded.
Allow Donations      | Enables Donations to be counted as `Points` if they exceed the `Donation Amount` value.
Only Count Once      | Counts a Donation only once, if it exceeds the `Donation Amount`
Cumulative Donations | Allows for Donations below the `Donation Amount` to pile up and add `Points` if they exceed the `Donation Amount`.

### Subscription Values

Under each Tier, you'll find the following options. Prime Subscriptions (Twitch) have the same value as Tier 1 Subscriptions and will be handled as such by the Script.

Option       | Description
-------------|------------
Sub          | Points rewarded for a Subs
Resub        | Points rewarded for a Resubs
Gifted Sub   | Points rewarded for a gifted Sub
Gifted Resub | Points awarded for a gifted Resub

### Streamlabs

Option       | Description
-------------|------------
Socket Token | Token required for the script to function. [See here](#streamlabs-sockettoken)

## Chatbot Command Parameters

You can use the following Parameters in your Commands and Timers:

Parameter         | Description
------------------|------------
$tsGoal           | Amount of `Points` needed per Streak
$tsPoints         | Current amount of `Points` in the current Streak
$tsPointsLeft     | Amount of `Points` needed to complete the current Streak
$tsStreak         | Current Streak
$tsTotalSubs      | Amount of total Subs (not `Points`) accumulated in the current Session
$tsTotalBits      | Amount of Bits accumulated in the current Session
$tsTotalDonations | Donation amount accumulated in the current Session

### Command Example

All these examples assume that a Subscription is worth one Point!

```text
We are currently working on Streak #$tsStreak and need $tsPointsLeft additional Subs.
```

> We are currently working on Streak #5 and need 6 additional Subs.

```text
We reached $tsTotalSubs subs so far!
```

> We reached 42 Subs so far!

## Customization

Making your own designs for the TwitchStreaker Overlay is straight forward and only require a few things to keep in mind. The single most important thing is to load the required JavaScript files in the correct order.

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

In case you're using a custom script, it has to be loaded after the `main.js` and should be deferred via the `defer` keyword as well, to prevent issues later on.

### HTML Elements

The following element ID's are available for use in your design:

ID             | Description
---------------|------------
Goal           | Amount of `Points` needed per Streak
Points         | Current amount of `Points` in the current Streak
PointsLeft     | Amount of `Points` needed to complete the current Streak
Streak         | Current Streaks
TotalSubs      | Amount of total Subs (not `Points`) accumulated in the current Session
TotalBits      | Amount of `Bits` accumulated in the current Session
TotalDonations | Donation amount accumulated in the current Session

None of those ID's are actually required and can be placed anywhere in the document, in case of the default design we're only using `Points`, `Streak` and `Goal`. Here a few examples:

### HTML Examples

#### "X Subs left until Wheel #X"

```HTML
<div>
  <span id="PointsLeft">2</span> Subs left until Wheel #<span id="Streak">1</span>
</div>
```

#### "X of X Subs, then we spin Wheel #X"

```HTML
<div>
  <span id="Points">2</span> of <span id="Goal">7</span> Subs, then we spin Wheel #<span id="Streak">1</span>
</div>
```

## JavaScript

Though you could just modify the [main.js](Overlay/main.js) in the `Overlay` folder. There is a more elegant way that keeps things simple and clean.

The Overlay object has an additional field with an anonymous function that is called on every refresh of the overlay and can be used for your custom code to be triggered at the same time with the most recent values.

### Setup

```javascript
Overlay.UserRefresh = function() {

  // Your stuff here

}
```

It is important that this always evaluates as a function, since it is called from within the EventBus in [main.js](Overlay/main.js). Anything else will result in a bunch of error and probably unwanted side-effects.

### Variables

The following variables are available for your custom script.

Variable                      | Description
------------------------------|------------
Overlay.CurrentGoal           | Amount of `Points` needed to complete a Streak (min: 1)
Overlay.CurrentStreak         | Current amount Streaks (min: 1)
Overlay.CurrentPoints         | Current amount of `Points` in the Streak (min: 0)
Overlay.CurrentPointsLeft     | Amount of `Points` left to the next Streak
Overlay.CurrentTotalSubs      | Amount of total Subs (not `Points`) accumulated in the current Session
Overlay.CurrentTotalBits      | Amount of total Bits accumulated in the current Session
Overlay.CurrentTotalDonations | Donation amount accumulated in the current Session

## Manual Overwrites

If something can go wrong, it will most like go wrong at some point. That's why the script has some overwrite functions built in to account for missed subs, streaks, and outright crashes.

Changes made will not display instantly, the update happens on a 5 second interval.

Button          | Functionality
----------------|--------------
\+ Sub          | Adds a Sub, Streaks will increment if conditions are met.
\- Sub          | Removes a Sub, until 0 (zero) is reached.
\+ Streak       | Adds a Streak.
\- Streak       | Removes a Streak, until 1 (one) is reached.
\+ Goal         | Increments the Goal by one.
\- Goal         | Decrements the Goal by one, until 1 (one) is reached.
Refresh Overlay | Refreshes the Overlay without loosing the current values.
Reset Tracker   | Resets everything to their initial values.

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

TwitchStreaker is using [StreamLabs Event Receiver](https://github.com/ocgineer/Streamlabs-Events-Receiver) by [Ocgineer](https://github.com/ocgineer)

[GNU GPL-3.0 License](LICENSE.md)

[Changelog](CHANGELOG.md)
