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
    'cringe', 'gaming', 'movies', 'soccer', 'crossfit', 'loseit']

f = open('ids', 'r')
replied = f.read().split('\n')
if len(replied) == 1:
    replied = []
else:
    replied.pop()
f.close()

def get_facts(filename):
    message_facts = []
    f = open(filename, 'r')
    for line in f:
        message = line.replace('\n','')
        message_facts.append(message)
    f.close()
    return message_facts

random_facts  = get_facts('random.txt')
soccer_facts  = get_facts('soccer.txt')
games_facts   = get_facts('games.txt')
fitness_facts = get_facts('fitness.txt')
movies_facts  = get_facts('movies.txt')

games_list   = ['gaming', 'games', 'game', 'videogame', 'starcraft']
soccer_list  = ['soccer']
fitness_list = ['crossfit', 'gym', 'loseit']
movies_list  = ['movie', 'movies', 'cinema']

def get_phrase(subreddit_name):
    if (any(word in subreddit_name.lower() for word in soccer_list)):
        return random.choice(soccer_facts)
    elif (any(word in subreddit_name.lower() for word in games_list)):
        return random.choice(games_facts)
    elif (any(word in subreddit_name.lower() for word in fitness_list)):
        return random.choice(fitness_facts)
    elif (any(word in subreddit_name.lower() for word in movies_list)):
        return random.choice(movies_facts)
    else:
        return random.choice(random_facts)

unreplied_threads = {}
replied = []
delay = 120
max_time = 3600*1
while True:
    try:
        subreddit = r.get_subreddit(random.choice(subreddits))
        submission = subreddit.get_random_submission()
        time_elapsed = int(abs(time.time() - submission.created_utc))
        if submission.id not in replied and submission.id not in unreplied_threads and time_elapsed < max_time:
            phrase = get_phrase(subreddit.display_name)
            message = 'Have some interesting fact to lighten up your thread - \"*' + phrase + '*\"'
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
