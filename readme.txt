Installation instructions:

After installing python 3.0 or above , on a command line type pip install praw.

If you get an error saying pip ins't recognized by the OS you can either add python to your system PATH or open the command line from the python folder (shift+right click -> open command line, on windows).

The default python directory on windows is C:\Users\<YourUser>\AppData\Local\Programs\Python\<Your Python Version>

After praw is installed just right click and select open with python and it should work.

During the configuration process the program will ask for a "Target", the target means that you will post a comment everytime your target posts a comment. NOTE: The program might not work if you just type a random name, insert PresidentObama if you have no interest in this feature.

The bot can only send mails to a gmail domain so it's mandatory that the chosen email is a @gmail.com adress. Also you need to activate the "Allow less secure applications" option for it to be able to actually send the emails (since the program sends an email from yourself to yourself to avoid emails going to the junk folder and other issues). This option is found in the settings of your account or easily found by googling the option name.

If you have any doubts contact /u/flyingepeto on reddit.



What it does:

This bot posts a comment equal to your latest comment on the latest post you commented, according to your specified time interval ( 30 minutes, 60 minutes, etc..) then deletes the previous comment (to avoid cluttering). It's extremely useful if you sell/buy things on reddit and need to keep reposting your sale on a specific thread.

It's also able to target a specific user in case someone keeps spamming the thread (this bot was initially created because of that reason).

Enjoy!