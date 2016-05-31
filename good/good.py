#!/usr/bin/python

import praw
import time
import sys
import random

#description of your bot
r = praw.Reddit(user_agent='')

#username and password
r.login('', '')

subreddits = ['funny', 'all', 'gifs', 'videos', '4chan', 'AdviceAnimals',\
    'AskReddit', 'cringe', 'Fitness', 'gaming', 'movies']

f = open('ids', 'r')
replied = f.read().split('\n')
if len(replied) == 1:
    replied = []
else:
    replied.pop()
f.close()

unreplied_threads = {}
replied = []
delay = 300
max_time = 3600*4
while True:
    try:
        subreddit = r.get_subreddit(random.choice(subreddits))
        submission = subreddit.get_random_submission()
        time_elapsed = int(abs(time.time() - submission.created_utc))
        if submission.id not in replied and submission.id not in unreplied_threads and time_elapsed < max_time:
                message = 'Good.'
                unreplied_threads[submission.id] = [submission, message]
                ids = []
                for value in unreplied_threads.values():
                    try:
                        print value[0]
                        value[0].add_comment(value[1])
                        ids.append(value[0].id)
                    except Exception as error:
                        print error
                for i in ids:
                    del unreplied_threads[i]
                    f = open('ids', 'a')
                    f.write(i + '\n')
                    f.close()
                    replied.append(i)
                time.sleep(delay)
    except Exception as error:
        print error
        time.sleep(delay)
