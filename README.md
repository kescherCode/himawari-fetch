# himawari_fetch
*Put near-realtime picture of Earth into a directory*

A fork of [himawaripy](https://github.com/boramalper/himawaripy).

![24 hours long animation by /u/hardypart](https://i.giphy.com/l3vRnMYNnbhdnz5Ty.gif)

himawari_fetch is a Python 3 script based on himawaripy that fetches near-realtime
(10 minutes delayed) picture of Earth as its taken by
[Himawari 8 (ひまわり8号)](https://en.wikipedia.org/wiki/Himawari_8) and saves them
to a prespecified directory. It also cleans up images older than a day.

Set a cronjob (or systemd service) that runs in every 10 minutes to automatically get the
near-realtime picture of Earth.

## Configuration

```                      
usage: himawari_fetch [-h] [-d DEADLINE] [--output-dir OUTPUT_DIR]
                      [--override-date OVERRIDE_DATE]

optional arguments:
  -h, --help            show this help message and exit
  -d DEADLINE, --deadline DEADLINE
                        deadline in seconds for this script to finish, set 0 to cancel
  --output-dir OUTPUT_DIR
                        directory to save images and metadata
  --override-date OVERRIDE_DATE
                        UTC timestamp in format '%Y-%m-%d %H:%M:%S'
```
While the script is fetching a new image, it will use around 700 MiB of memory.

You should set a deadline compatible with your cronjob (or timer) settings to assure that script will terminate in X
minutes before it is started again.

## Installation
Uh. Will have to figure this one out, since I don't want to push it to pypi.

### For Mac OSX Users

OSX has deprecated crontab, and replaced it with `launchd`. To set up a launch agent, copy the provided sample `plist`
file in `osx/at.kescher.himawari_fetch.plist` to `~/Library/LaunchAgents`, and edit the following entries if required

    mkdir -p ~/Library/LaunchAgents/
    cp osx/at.kescher.himawari_fetch.plist ~/Library/LaunchAgents/

* `ProgrammingArguments` needs to be the path to himawari_fetch installation. This *should* be `/usr/local/bin/himawari_fetch`
by default, but himawari_fetch may be installed elsewhere.

* `StartInterval` controls the interval between successive runs, set to 10 minutes (600 seconds) by default,
edit as desired.

Finally, to launch it, enter this into the console:

    launchctl load ~/Library/LaunchAgents/at.kescher.himawari_fetch.plist


## Uninstallation

```
# Either remove the cronjob
crontab -e
    # Remove the line
    */10 * * * * himawari_fetch...

# OR if you used the systemd timer
systemctl disable --now himawari_fetch.timer
# If not packaged but manually created systemd units, also do
rm /etc/systemd/system/himawari_fetch.{timer,service}

# Uninstall the package
# haha, TODO!
```


`<INSTALLATION_PATH>` can be found using the command `which -- himawari_fetch`.

## Attributions
Thanks to [Bora M. Alper](https://github.com/boramalper) for the maintaining of himawaripy.

The next attributions are kept intact from the original repo:

Thanks to *[MichaelPote](https://github.com/MichaelPote)* for the [initial
implementation](https://gist.github.com/MichaelPote/92fa6e65eacf26219022) using
Powershell Script.

Thanks to *[Charlie Loyd](https://github.com/celoyd)* for image processing logic
([hi8-fetch.py](https://gist.github.com/celoyd/39c53f824daef7d363db)).

Obviously, thanks to the Japan Meteorological Agency for opening these pictures
to public.
