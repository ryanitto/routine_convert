Routine Convert
==

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


Adjust settings
==
Edit settings.py
--
First, you need to open the settings.py file and make sure you have the required binaries downloaded and placed in a folder.

Included on Git
--
The necessary binaries are included in:

    \routine_convert\bin\create_paths.bat

Manually
--
But... if you already have these binaries and would rather not download that right now, you can grab these binaries below:

* **HandBrakeCLI.exe**
    * CLI version:  https://handbrake.fr/downloads2.php
    * GUI version:  https://handbrake.fr/downloads.php
* **ffprobe.exe**
    * Part of ffmpeg: https://ffmpeg.zeranoe.com/builds/

   Set handbrake preset file
   --
   Preset file example:        `\routine_convert\bin\presets.json`
   
   In `settings.py`, set the `PRESET_FILE` variable to the presets.json file location.  An example above is provided, but this can also be generated from Handbrake GUI version (https://handbrake.fr/downloads.php) by just opening it up. :)

Set up folder structure
==

From script
--
Included in the `\routine_convert\bin\` folder is a `create_paths.bat` file.  Replace the `C:\path\to\python\python.exe` location with your installed python location, where this package is installed.

    \routine_convert\bin\create_paths.bat

Manually
--
Your folder structure will need to be made in the following way:
1.  In `settings.py`, set the `root_dir` to your top-level folder (e.g. `C:\media`)
2.  Create either, or both, folder(s): `Blu-Ray` and `DVD`
3.  Under that/those, create either: `Movies` and `TV Shows`
4.  Under that/those, create all three folders:
    * `TO_CONVERT`
    * `CONVERTED`
    * `SOURCE_PROCESSED`

An example of this structure would look like:

    C:\media\Blu-Ray\Movies\TO_CONVERT


To run
==

Use included script
--
Included in the `\routine_convert\bin\` folder is a `convert_all_media.bat` file.  Replace the `C:\path\to\python\python.exe` location with your installed python location, where this package is installed.

    \routine_convert\bin\create_paths.bat

Manually
--
Make a batch script that calls python and
the `convert_to.py` file:

    REM Batch process to call from Windows Task Scheduler (taskschd.msc)
    REM ===========
    REM Call python.exe path, then the path to the "convert_to.py" script
    C:\path\to\python\python.exe "C:\path\to\python\Lib\site-packages\routine_convert\convert_to.py"

Or, if you have an environment with this script and package
dependencies already made, you can run the script this way:

    C:\path\to\python\python.exe C:\path\to\python\Lib\site-packages\routine_convert\convert_to.py
