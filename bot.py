import praw
import datetime
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Creates initial configurations file with some verifications of invalid inputs
def getInfo():
    print("All information will be stored locally in a text file, still it's recommended you create a new email for security purposes \n")
    email=input("Welcome, please enter the email to send the reddit message notifications: ")
    while email=="" or "@" not in email:
        email=input("Please enter a valid email")
    file=open(home_path+"\RedditBotConfigs\config.txt","w")
    file.write(email+"\n")
    reddit_username_for_write=input("Enter your reddit username: ")
    while reddit_username_for_write=="":
        reddit_username_for_write=input("Please insert a valid reddit username")
    file.write(reddit_username_for_write+'\n')
    reddit_password=input("Please enter your reddit password: ")
    while reddit_password=="":
        reddit_password=input("Please enter a non empty password")
    file.write(reddit_password+'\n')
    email_password=input("Please enter your email password: ")
    while email_password=="":
        email_password=input("Please insert a valid password, i'm not stealing your email, i promise ;)")
    file.write(email_password+'\n')
    client_id=input("Please enter your reddit client ID (Check the readme file if you don't know what his is)")
    while client_id=="":
        client_id = input("Please enter a valid client ID (Check the readme file if you don't know what his is)")
    file.write(client_id+'\n')
    client_secret=input("Please enter your reddit client secret")
    while client_secret=="":
        client_secret=("Please enter a valid secret")
    file.write(client_secret)

    print("\n All configurations were saved to " + home_path + "\RedditBotConfigs\config.txt delete that file if you need to reconfigure the program \n")
    file.close()


def email_notification(unreadMessages):
    if (len(unreadMessages)!=0):
        for x in range(0, 4):
            print("\n You have a new unread message!!!!!!!! \n")
        msg = MIMEMultipart()
        msg['From'] = infolist[0]
        msg['To'] = infolist[0]
        msg['Subject'] = "Unread message on reddit!"

        body = "You have a new unread message on reddit"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(infolist[0], infolist[3])
        text = msg.as_string()
        server.sendmail(infolist[0], infolist[0], text)
        server.quit()


#Creates default directory of the program
home_path=os.path.expanduser("~")
if not os.path.exists(home_path+"\RedditBotConfigs"):
    os.makedirs(home_path+"\RedditBotConfigs")
if not os.path.isfile(home_path + "\RedditBotConfigs\config.txt"):
    getInfo()


with open(home_path+"\RedditBotConfigs\config.txt") as f:
    infolist = f.read().splitlines()

redditor=""
#Sends authentication info to reddit
try:
    redditor = praw.Reddit(client_id=infolist[4],client_secret=infolist[5],password=infolist[2],user_agent='Posts comments periodically',username=infolist[1])
except IndexError:
    print("Error: Something went wrong while reading the configuration file, delete the configuration folder (Located in your user folder) and reconfigure the script parameters again, if that doens't fix it feel free to contact me at /u/flyingepeto on reddit")


totalTime=int(input('How long between reposts (in minutes): '))

while True:
    commentTree = redditor.redditor(infolist[1]).comments.new()
    unreadMessages=list(redditor.inbox.unread())
    email_notification(unreadMessages)

    latest_comment = commentTree.next()
    current_thread = latest_comment.submission

    total_minutes_since_last_comment= (datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(latest_comment.created_utc)).total_seconds()/60

    if (totalTime< total_minutes_since_last_comment):
        print(str(totalTime) + ' minutes have passed, posting a new comment')
        latest_comment.delete()
        current_thread.reply(latest_comment.body)
    else:
        print(str(total_minutes_since_last_comment) + ' minutes have passed')

    time.sleep(180)
'''
while(True):
#Gets info on the last comment of the spammer you want to target
    enemy_user_name=infolist[1]
    enemy_redditor = r.get_redditor(enemy_user_name)
    gen=enemy_redditor.get_comments()
    first_comment=next(gen)
    enemy_last_comment_date=datetime.datetime.fromtimestamp(first_comment.created_utc)


#Gets info on your latest comment and the submission it belongs to
    redditor=r.get_redditor(my_user_name)
    gen2=redditor.get_comments()
    #Sends an email if there is an unread message
    unread_comment_list = []
    unread_messages=r.get_unread()
    for message in unread_messages:
        unread_comment_list.append(message)
        break
    if len(unread_comment_list)!=0:
        for x in range(0, 4):
            print("\n You have a new unread message!!!!!!!! \n")
        msg = MIMEMultipart()
        msg['From'] = infolist[0]
        msg['To'] = infolist[0]
        msg['Subject'] = "Unread message on reddit!"

        body = "You have a new unread message on reddit"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(infolist[0],infolist[4])
        text = msg.as_string()
        server.sendmail(infolist[0], infolist[0], text)
        server.quit()
        unread_comment_list=[]

    my_last_comment=next(gen2)
    my_last_comment_text=my_last_comment.body
    my_last_comment_date=datetime.datetime.fromtimestamp(my_last_comment.created_utc)
    submission=my_last_comment.submission


#Prints dates of both comments, for testing purposes only.

    #print("Last time enemy posted a comment: " + str(enemy_last_comment_date))
    #print("Last time i posted a comment: " + str(my_last_comment_date))

#Compares date of your last comment with the enemy and posts a comment if he posted a comment after you.
    if (my_last_comment_date<enemy_last_comment_date):
        print(str(enemy_user_name) + " posted a comment,resposting. ")
        my_last_comment.delete()
        submission.add_comment(my_last_comment_text)

#else checks the first comment of the post and sees if 45mins have passed since your comment.
    else:
        post=r.get_submission(submission_id=submission.id)
        post_comment_list=praw.helpers.flatten_tree(post.comments)
        latest_comment= post_comment_list[0]
        print(latest_comment.author)
        if(latest_comment.author != my_user_name):
            latest_comment_date=datetime.datetime.fromtimestamp(latest_comment.created_utc)
            total_minutes=(latest_comment_date-my_last_comment_date) + (datetime.datetime.utcnow()-latest_comment_date)
            print("Total minutes since latest comment:" + str(total_minutes.total_seconds()/60))
            if ((total_minutes.total_seconds()/60) > total_time):
                print(str(total_time) + " minutes have passed, posting a new comment")
                my_last_comment.delete()
                submission.add_comment(my_last_comment_text)



    time.sleep(180)

'''