Installation instructions:

After installing python 3.0 or above , on a command line type pip install praw=

If you get an error saying pip ins't recognized by the OS you can either add python to your system PATH or open the command line from the python folder (shift+right click -> open command line, on windows).

The default python directory on windows is C:\Users\<YourUser>\AppData\Local\Programs\Python\<Your Python Version>

After praw is installed just right click and select open with python and it should work.

The bot can only send mails to a gmail domain so it's mandatory that the chosen email is a @gmail.com adress. Also you need to activate the "Allow less secure applications" option for it to be able to actually send the emails (since the program sends an email from yourself to yourself to avoid emails going to the junk folder and other issues). This option is found in the settings of your gmail account or easily found by googling the option name.

The bot will ask for a reddit client id and a reddit secret.

Go to https://www.reddit.com/prefs/apps and create a new application at the bottom of the page

Under web app in bold will be your client ID, your secret will be below your ID.


If you have any doubts contact /u/flyingepeto on reddit.



What it does:

This bot posts a comment equal to your latest comment on the latest post you commented, according to your specified time interval ( 30 minutes, 60 minutes, etc..) then deletes the previous comment (to avoid cluttering). It's extremely useful if you sell/buy things on reddit and need to keep reposting your sale on a specific thread.

The email feature was mainly implemented so you can link gmail to your phone and get phone alerts everytime someone sends you a private message on reddit (it checks if you have any unread message and emails you warning you if you do).

Enjoy!
