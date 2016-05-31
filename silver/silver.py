#!/usr/bin/python

import praw
import time
import sys

#description of your bot
r = praw.Reddit(user_agent='')

#username and password
r.login('', '')

subreddit = r.get_subreddit('all')

message = '[Congratulations on your comment! Have some silver!](http://i.imgur.com/lXVJYnh.png)'

f = open('ids', 'r+a')
replied = f.read().split('\n')
if len(replied) == 1:
    replied = []
else:
    replied.pop()
f.close()

unreplied_comments = []
karma = 300
max_time = 20000
sleep_time = 60

def reply_user(comment):
    print 'Jackpot! %s' % (comment.author)
    comment.reply(message)
    f = open('ids', 'a')
    f.write(comment.id + '\n')
    f.close()
    replied.append(comment.id)
    time.sleep(sleep_time)

excluded_words = ['robin williams']
while True:
    try:
        submission = subreddit.get_random_submission()
        print submission
        if (any(word in submission.title.lower() for word in excluded_words)):
            print 'Jumping thread'
            continue
        submission.replace_more_comments(limit=None, threshold=0)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            if type(comment) is praw.objects.MoreComments: continue
            time_created = int(abs(time.time() - comment.created_utc))
            try:
                while len(unreplied_comments) > 0:
                    comment_elem = unreplied_comments.pop()
                    if comment_elem.id not in replied:
                        reply_user(comment_elem)
                if comment.score > karma and comment.id not in replied\
                        and time_created < max_time:
                    reply_user(comment)
            except Exception as error:
                print error
                if comment.score > karma and comment.id not in replied\
                        and time_created < max_time:
                    unreplied_comments.append(comment)
                    time.sleep(sleep_time)
                continue;
    except Exception as error:
        print error
        time.sleep(sleep_time)
