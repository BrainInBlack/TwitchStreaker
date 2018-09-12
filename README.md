# TwitchStreaker for Streamlabs Chatbot

Initially created for the Twitch-Streamer [AnEternalEnigma](http://twitch.tv/AnEternalEnigma) to keep track of new and gifted subscriptions to his channel. This is the public version of the same exact script, with some minor changes to make it a little more generic.

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

Before you attempt to make any customization's, you need to be aware that we're using a workaround to get the text-outline working in the overlay. Meaning if you don't want/need a text-outline you should remove the following:

[main.css](Overlay/main.css)
```CSS
#Tracker:before {
  content: attr(title);
  position: absolute;
  -webkit-text-stroke: 0.09em #6441a4;
  z-index: -1;
}
```

[main.js](Overlay/main.js)
```Javascript
// Outline Hack!
'Container': document.getElementById('Tracker'),
...
// Outline Hack!
this.Container.title = this.Container.innerText;
```

With that out of the way, you're free to pretty much do what ever you want. Just make sure that there are elements with IDs around that correspond to the respective values (see [Overlay.html](Overlay.html)), otherwise the script will not work without messing around with the JavaScript, and at that point you probably know what you're doing.

## Manual Overwrites

If something can go wrong, it will most like go wrong at some point. That's why the script has some overwrite functions built in to account for missed subs, streaks, and outright crashes.

Button | Functionality
-------|--------------
Add Sub | Adds a Sub, Streaks will increment if conditions are met.
Subtract Sub | Removes a Sub, until 0 (zero) is reached.
Add Streak | Adds a Streak.
Subtract Streak | Removes a Streak, until 0 (zero) is reached.
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
