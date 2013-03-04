ativ
====

Script to help manage screen rotations and digitizers while running Linux on the
Samsung ATIV Smart PC Pro 700T

Uses the python tkinter module, which can be installed on Ubuntu with:

  sudo apt-get install python-tk

Desktop shortcut
----------------

The file ativ.desktop.sample can be copied to the ~/Desktop directory, renaming
it to ativ.desktop in the process. The line Exec=path_to_ativ.py needs to be
modified to point to the location of ativ.py

Known issues
------------

Touch sensor rotation doesn't seem to work. Work around is to disable touch when rotating screen and use stylus.

