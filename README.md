# TwitchStreaker for Streamlabs Chatbot

Initially created for the Twitch-Streamer [AnEternalEnigma](https://twitch.tv/AnEternalEnigma) to keep track of new and gifted subscriptions to his channel. This is the public version of the same exact script, with some minor changes to make it a little more generic.

TwitchStreaker is compatible with Twitch and YouTube. For YouTube, only the regular Subscription options apply.

## Table of Contents

- [TwitchStreaker for Streamlabs Chatbot](#twitchstreaker-for-streamlabs-chatbot)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Updates](#updates)
  - [Updating from 2.x to 3.x](#updating-from-2x-to-3x)
  - [Streamlabs SocketToken](#streamlabs-sockettoken)
  - [Troubleshooting](#troubleshooting)
  - [Settings](#settings)
    - [General](#general)
    - [Bits](#bits)
    - [Donations](#donations)
    - [Follows](#follows)
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
  - [Compensation](#compensation)
  - [Project Info](#project-info)

## Disclaimer

**We are not responsible for the misuse of this script!** It is up to YOU to apply the scripts functionality according to your platforms Terms of Service. For example, Twitch does NOT allow you to give away Subscriptions for Bits (see [Bits Acceptable Use Policy](https://www.twitch.tv/p/en/legal/bits-acceptable-use/)). Please make sure that you use the Script in a way that does not violate any Terms of the platform that you are using.

## Installation

1. Download the [latest release](https://github.com/BrainInBlack/TwitchStreaker/releases/latest).
2. Extract the downloaded archive into the `Chatbot > Services > Scripts` directory.
3. In the Chatbot, open the Scripts Tab and click the `Reload Scripts` button.
4. Right click on the `TwitchStreaker` script and click `Insert API Key`.
5. Enter your `SocketToken` and the amount of subs required per streak. [See here](#streamlabs-sockettoken)
6. Add the Overlay as a Browser Source to your scene in your preferred streaming software.
   - [Overlay.html](Overlay.html) the "Classic" Overlay.
     - Recommended Browser Source width: `800px`
     - You can use the text files contained within the `Text` folder as an alternative
   - [BarOverlay.html](BarOverlay.html) the "new" Progressbar.
     - The size is defined by the Browser Source properties
   - These Overlays has separate settings within the bot, i.e. you can use both Overlay if you want to

## Updates

**Remember to Backup your customized files!**

1. Download the [latest release](https://github.com/BrainInBlack/TwitchStreaker/releases/latest).
2. Check the [Changelog](CHANGELOG.md) for additional instructions
3. Extract the downloaded archive and overwrite existing files.
4. Reapply your customization's.
5. Reload the script and overlay.
   - Click the `Reload Script` button on the Chatbot.
   - De-select and then re-select the script, to update the UI.
   - Click the `Save Settings` and then the `Reset Session` button, to makes sure that the most recent changes are applied.
   - Reload the Overlay within your Streaming software.

## Updating from 2.x to 3.x

With version 3.0.0 we added a progressbar that runs separate to the classic overlay, with separate settings and sounds. The classic Overlay is still the same exact things, but has some additional element options (see [HTML Elements](#html-elements)).

1. Make a Backup of the entire folder.
2. Extract the 3.x archive and overwrite existing files.
3. Delete `Settings.js`, `Settings.json`, `Session.json` and `TwitchStreaker.log` from the folder.
4. Enter your `SocketToken`, [See here](#streamlabs-sockettoken).
5. Reapply your Settings and Customizations
   - Customizations to the Script should be redone, since quite a few things have changed under the hood and there are additional options for you to explore.
6. Save the Settings and reset the Session

## Streamlabs SocketToken

1. Navigate to [Streamlabs API Settings](https://streamlabs.com/dashboard#/settings/api-settings)
2. Click on `API Tokens`
3. Click the `Copy` Button next to the `Your Socket API Token` field
4. Insert the Token under `Streamlabs > Socket Token` in the Script Settings

## Troubleshooting

### Check your Account Connections

In most cases it is as simple as reconnecting your Accounts to the bot.

1. Go to connections :bust_in_silhouette:
2. Generate new Tokens for both the `Twitch Bot` and `Twitch Streamer`
3. Reload the script and reset the session

### Check your Python Installation

Another common issue is a problem with the Python 2.7.x installation.

- Make sure [python 2.7.13](https://www.python.org/downloads/release/python-2713/)  x86 is installed. Don't use newer versions of python or x64
- Make sure the lib folder path found in `scripts tab` -> `settings` :gear: leads to the lib folder located inside the python folder that was created when installing python. By default this would look like [THIS](https://i.imgur.com/5mtHoNL.png)
- Make sure you installed [python 2.7.13](https://www.python.org/downloads/release/python-2713/) x86 and NOT python 3.X

### Reset the current Session, reset the Settings

Some rare cases involve a corrupted Session, or a corrupted Settings file.

1. Delete `Session.json` from the script folder.
2. Reload the Script and continue with step 3 if the issue persists.
3. Delete `Settings.json` and `Settings.js` from the script folder.
4. Redo your settings, incl. the [Socket Token](#streamlabs-sockettoken).
5. Reload the Script.

### Get Support on Discord

If all that fails, then there is [Discord](https://discord.gg/HWTaady), where we can help you resolve the issue you're having.

## Settings

TwitchStreaker has a lot of Options to give you as much control as possible on how the script works for you. For example you can make your `Goal` increase over time, or allow Donations to be counted as `Points` when they exceed a specified amount.

### General

Option            | Description
------------------|------------
Goal              | The amount of `Points` required for the next Streak.
Goal Min          | Minimum value of the `Goal` option (Defaults to the value of `Goal` when above the `Goal`)
Goal Max          | Maximum value of the `Goal` option (Defaults to the value of `Goal` when below the `Goal`)
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

### Follows

Option              | Description
--------------------|------------
Follows Required    | Amount of `Follows` required for it to be counted.
Follow Point Values | Amount of `Points` awarded.
Allow Follows       | Enables Follows to be counted as `Points` if the exceed the `Follows Required` amount.

### Progress Bar

Option                 | Description
-----------------------|------------
Goal                   | Amount of `Points` required to fill the bar.
Segment Count          | Amount of segments within the bar. (0 = disabled)
Enable Bits            | Enable Bits to be displayed on the bar.
Enable Donations       | Enable Donations to be displayed on the bar.
Enable Follows         | Enable Follows to be displayed on the bar.
Enable Subs            | Enable Subscriptions to be displayed on the bar.
Enable Sound           | Enable the Sound System
Completion Sound       | Filename, incl. the file-extension, for the Bar Completion sound within the `Sounds` folder. (Plays when the bar is completely filled)
Completion Sound Delay | Delay for the Completion Sound.
Segment Sound          | Filename, incl. the file-extension, for the Segment Completion sound within the `Sounds` folder. (Plays when a Segment is filled.)
Segment Sound Delay    | Delay for the Segment Completion Sound.

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

Parameter               | Description
------------------------|------------
$tsBarGoal              | Amount of `Points` needed to fill the Progressbar
$tsBarPointsLeft        | Amount of `Points` needed to fill the Progressbar
$tsBarSegmentsCompleted | Amount of Segments that are completely filled
$tsBarSegmentPointsLeft | Amount of `Points` needed to fill the current Segment on the Progressbar
$tsBitsLeft             | Amount of `Bits` needed to get the next `Point`
$tsBitPoints            | Amount of `Points` acquired via `Bits`
$tsDonationPoints       | Amount of `Points` acquired via `Donations`
$tsFollowsLeft          | Amount of `Follows` needed to get the next `Point`
$tsFollowPoints         | Amount of `Points` acquired vie `Follows`
$tsGoal                 | Amount of `Points` needed per Streak
$tsPoints               | Current amount of `Points` in the current Streak
$tsPointsLeft           | Amount of `Points` needed to complete the current Streak
$tsStreak               | Current Streak
$tsSubPoints            | Amount of `Points` acquired via `Subscriptions`
$tsTotalBits            | Amount of Bits accumulated in the current Session
$tsTotalDonations       | Donation amount accumulated in the current Session
$tsTotalFollows         | Amount of Follows accumulated in the current Session
$tsTotalSubs            | Amount of total Subs (not `Points`) accumulated in the current Session

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

**The Progressbar is not yet finalized, customization documentation will come as soon as it is finalized**

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
BitsLeft       | Amount of `Bits` needed to get the next `Point`
BitPoints      | Amount of `Points` acquired via `Bits`
DonationPoints | Amount of `Points` acquired via `Donations`
FollowPoints   | Amount of `Points` acquired via `Follows`
Goal           | Amount of `Points` needed per Streak
Points         | Current amount of `Points` in the current Streak
PointsLeft     | Amount of `Points` needed to complete the current Streak
Streak         | Current Streaks
SubPoints      | Amount of `Points` acquired via `Subscriptions`
TotalBits      | Amount of `Bits` accumulated in the current Session
TotalDonations | Donation amount accumulated in the current Session
TotalFollows   | Amount of total Follows accumulated in the current Session
TotalSubs      | Amount of total Subs (not `Points`) accumulated in the current Session

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

**The Progressbar is not final at the moment and will not yet be documented!**

### Setup

```javascript
Overlay.Text.UserRefresh = function() {

  // Your stuff here

}
```

It is important that this always evaluates as a function, since it is called from within the EventBus in [main.js](Overlay/main.js). Anything else will result in a bunch of error and probably unwanted side-effects.

### Variables

The following variables are available for your custom script.

Variable                    | Description
----------------------------|------------
Overlay.BitsLeft       | Amount of `Bits` needed to get the next `Point`
Overlay.BitPoints      | Amount of `Points` acquired via `Bits`
Overlay.DonationPoints | Amount of `Points` acquired via `Donations`
Overlay.FollowPoints   | Amount of `Points` acquired via `Follows`
Overlay.Goal           | Amount of `Points` needed to complete a Streak (min: 1)
Overlay.Streak         | Current amount Streaks (min: 1)
Overlay.SubPoints      | Amount of `Points` acquired via `Subscriptions`
Overlay.Points         | Current amount of `Points` in the Streak (min: 0)
Overlay.PointsLeft     | Amount of `Points` left to the next Streak
Overlay.TotalBits      | Amount of total Bits accumulated in the current Session
Overlay.TotalDonations | Donation amount accumulated in the current Session
Overlay.TotalFollows   | Follow amount accumulated in the current Session
Overlay.TotalSubs      | Amount of total Subs (not `Points`) accumulated in the current Session

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

[Twitter](https://twitter.com/BrainInBlack)

## Streamers using TwitchStreaker

[**AnEternalEnigma**](https://twitch.tv/AnEternalEnigma)

[**BloodThunder**](https://twitch.tv/BloodThunder)

[**KatLink**](https://twitch.tv/KatLink)

[**PersonSuit**](https://twitch.tv/PersonSuit)

[**TheLevelUpShow**](https://www.twitch.tv/thelevelupshow)

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Contributor's

[**BrainInBlack**](https://github.com/BrainInBlack) - Programming

[**AnEternalEnigma**](https://twitch.tv/AnEternalEnigma) - Initial Concept

[**TheLevelUpShow**](https://www.twitch.tv/thelevelupshow) - Progressbar Concept and Debugging

## Compensation

The topic of compensating me for my work came up quite a few times. While I appreciate the idea, I do this for fun and don't need any type of monetary compensation. If you still feel like compensating me for my work, then there is my [GoG.com Wishlist](https://www.gog.com/u/beStrange/wishlist) with a mix of games in most price classes.

In case you decide to gift me something from said wishlist, thank you and use braininblack@gmail.com as the recipient. However, a simple "thank you!" goes a long way and is more than welcome.

## Project Info

TwitchStreaker is using [StreamLabs Event Receiver](https://github.com/ocgineer/Streamlabs-Events-Receiver) by [Ocgineer](https://github.com/ocgineer)

[GNU GPL-3.0 License](LICENSE.md)

[Changelog](CHANGELOG.md)
