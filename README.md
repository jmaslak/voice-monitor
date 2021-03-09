# Pitch Tracker

This is a text-mode (console) application that builds a histogram of
your vocal pitch. It's right now useful for people trying to get their
voice above the typical male range, but sadly the app is not yet ready
for use by most people (I'll spend some time on that soon!).

It listens to your system default input device, and is currently
configured (hard coded) in the code to show a histogram between 110hz
and 260hz, with a red column at 160hz (representing "bad" for me), a
green column (representing "good" for me) at 180hz.  When it detects
sound above a threshold, it starts outputting lines to the console of
the current primary pitch that it detects.  Green "date" text output
to the screen means that the pitch is above 180hz.  Yellow means that
the pitch is between 160hz and 180hz.  Red means the pitch is below
160hz.

# WARNING

This is extremely ugly code right now!  Use at your own risk.

Right now, it's probably only suitable for people who are comfortable
with the command line and possibly modifying the script to their own
needs.

I do plan on packaging this up much nicer! Stay tuned for that!

# Installation Instructions

Install Python3 on your environment.

Clone the git repo to your machine.

Start a shell and change to the directory you cloned above.

Create a virtualenv using the following commands on Linux:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, do this:

```
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Once this succeeds, you can run the app.

To start the app, on Linux:

```
source venv/bin/activate
python3 pitch.py
```

To start the app, on Windows:

```
venv\Scripts\activate
python3 pitch.py
```

To exit the application, use ctrl-c.

