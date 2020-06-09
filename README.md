Routine Convert
===========

"Routine convert" compresses movies which have been backed up by
a user, from a tool such as MakeMKV.

My initial idea was to write a script that would make converting my
backed up movies, to smaller files, easier.  I found it became more
and more tedious to do this by hand, especially in the case with
TV shows.  When I learned that a tool like Handbrake can be ran
at command-line, I started to explore a routine script.

My goal was to make it as easy as - I pop in a movie in my disc
drive, I back it up with MakeMKV, eject the disc and move on to
another!  Overnight, a script would kick off and my computer would
just render until morning - depending on the compression settings.

You can have this too!  Let's get started.


Settings (settings.py)
=========
First, you need to open the settings.py file and make sure
you have the required binaries downloaded and placed a single folder.

* **HandBrakeCLI.exe**
    * CLI version:  https://handbrake.fr/downloads2.php
    * GUI version:  https://handbrake.fr/downloads.php
* **ffprobe.exe**
    * Part of ffmpeg: https://ffmpeg.zeranoe.com/builds/

Media directory
-------------
`root_dir`:           Needs to point to a "media folder" on your system!
                    (ex.  "C:\BluRay_Files")


Handbrake preset file
-------------
`Preset file`:        C:\users\yourname\AppData\HandBrake\presets.json

This is generated by opening up the GUI version of the program https://handbrake.fr/downloads.php.


To run
=========
Make a batch script that calls python and
the `convert_to.py` file:

    REM Batch process to call from Windows Task Scheduler (taskschd.msc)
    REM ===========
    REM Call python.exe path, then the path to the "convert_to.py" script
    C:\Python\python.exe "C:\handbrake_convert\convert_to.py"

Or, if you have an environment with this script and package
dependencies already made, you can run the script this way:

    python C:\<python_env>\handbrake_convert\convert_to.py
