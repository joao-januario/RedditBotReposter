import praw
import datetime
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Creates default directory of the program
home_path=os.path.expanduser("~")
if not os.path.exists(home_path+"\RedditBotConfigs"):
    os.makedirs(home_path+"\RedditBotConfigs")


#Creates initial configurations with some verifications of invalid inputs
if not os.path.isfile(home_path+"\RedditBotConfigs\config.txt"):
    print("All information will be stored locally on your computer, still it's recommended you create a new email for security purposes \n")
    email=input("Welcome, please enter your email: ")
    while email=="" or "@" not in email:
        email=input("Please enter a valid email")
    file=open(home_path+"\RedditBotConfigs\config.txt","w")
    file.write(email+"\n")
    reposter=input("Please enter the name of your target (insert PresidentObama if there is no target): ")
    while reposter=="":
        reposter=input("You must insert PresidentObama even if you don't have a target \n")
    while (reposter=="poketcgfan95"):
        print("That name is not valid ")
        reposter = input("Please enter the name of your target (insert PresidentObama if there is no target): ")
    file.write(reposter +"\n")
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
    file.write(email_password)
    print("\n All configurations were saved to "+ home_path+"\RedditBotConfigs\config.txt delete that file if you need to reconfigure the program \n")
    file.close()


with open(home_path+"\RedditBotConfigs\config.txt") as f:
    infolist = f.read().splitlines()

#Sends info to reddit
user_agent= "Post trading comment on /r/pkmntcgtrades periodically /u/"+infolist[2]
r = praw.Reddit(user_agent=user_agent)
r.login(infolist[2],infolist[3],disable_warning=True) #Possible deprecation in the future.
my_user_name=infolist[2]

total_time=int(input('How long between reposts (in minutes): '))


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