# TwitchStreaker for Streamlabs Chatbot

Initially created for the Twitch-Streamer [AnEternalEnigma](http://twitch.tv/AnEternalEnigma) to keep track of new and gifted subscriptions to his channel. This is the public version of the same exact script, with some minor changes to make it a little more generic.

## Table of Contents

- [TwitchStreaker for Streamlabs Chatbot](#twitchstreaker-for-streamlabs-chatbot)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Updates](#updates)
  - [Customization](#customization)
  - [JavaScript Variables](#javascript-variables)
  - [Manual Overwrites](#manual-overwrites)
  - [Support](#support)
  - [Contributing](#contributing)
  - [Contributor's](#contributors)
  - [Project Info](#project-info)

## Installation

1. Download the [latest release](http://github.com/BrainInBlack/TwitchStreaker/releases/latest).
2. Extract the downloaded archive into the```Chatbot > Services > Scripts``` directory.
3. In Chatbot, open the Scripts Tab and click the ```Reload Scripts``` button.
4. Right click on the ```TwitchStreaker``` script and click ```Insert API Key```.
5. Enter your ```Twitch Name``` and the amount of subs required per streak.
6. Add the [Overlay.html](Overlay.html) as Browser Source to your scene in your preferred streaming software.
   1. Recommended Browser Source width: ```800px```

**For OBS:** Make sure that ```Shutdown source when not visible``` and ```Refresh browser when scene becomes active``` are unchecked. If you want to use the Overlay in other scenes, use the existing Source.

**For XSplit:** Make sure that ```Keep source in memory``` is checked, ```Reload on scene enter``` and ```Reload on source show``` are unchecked. If you want to use the Overlay in other scenes, copy&paste the source as a linked source to another scene.

## Updates

**Remember to Backup your customized files!**

1. Download the [latest release](http://github.com/BrainInBlack/TwitchStreaker/releases/latest).
2. Extract the downloaded archive and overwrite existing files.
3. Check the [Changelog](CHANGELOG.md) for additional instructions
4. Reapply your customization's.
5. Reload the script and overlay.

## Customization

Making your own designs for TwitchStreaker is straight forward and only require a few things to keep in mind. The single most important thing is to load the required JavaScript files in the correct order.

```HTML
<html>
  <head>
    <!-- OtherStuff -->
    <script src="API_Key.js"></script>
    <script src="Settings.js"></script>
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
Subs | Current amount of Subs in the Streak
SubsLeft | Amount of Subs left for the next Streak
Streak | Current amount of Streaks
Goal | Amount of Subs needed to complete the current Streak

None of those ID's are required and can be placed anywhere in the document, in case of the default design we're only using ```Subs```, ```Streak``` and ```Goal```. Here a few examples:

*"X Subs left until Wheel #1"*
```HTML
<div><span id="SubsLeft">2</span> Subs left until Wheel #<span id="Streak">1</span></div>
```

*"X of X Subs, then we spin Wheel #1"*
```HTML
<div><span id="Subs">2</span> of <span id="Goal">7</span> Subs, then we spin Wheel #<span id="Streak">1</span></div>
```

The rest is just CSS and your own creativity.

## JavaScript Variables

Variable | Description
---------|------------
settings.Subs | Current amount of Subs in the Streak (min: 0)
settings.SubLeft | Amount of subs left to the next Streak
settings.Streak | Current amount Streaks (min: 1)
settings.Goal | Amount of Subs needed to complete a Streak (min: 1)
settings.GoalIncrement | Amount of which the Goal gets incremented each time a Streak is completed (min: 0)
settings.GoalCap | Cap for the incremental goals. (min: initial goal)
settings.InitialGoal | Original Goal value upon init (needed for the reset)
settings.StreamerName | Name of the Streamer (required to be able to ignore gifted Subs made by the streamer)
settings.Tier1..3 | Worth of subs for each SubTier (min: 1)

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

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Contributor's

[**BrainInBlack**](https://github.com/BrainInBlack)

[**AnEternalEnigma**](http://twitch.tv/AnEternalEnigma)

[**KatLink**](http://twitch.tv/KatLink)

## Project Info

[GNU GPL-3.0 License](LICENSE.md)

[Changelog](CHANGELOG.md)
