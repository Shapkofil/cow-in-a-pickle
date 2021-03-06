#!/usr/bin/env python3

import tweepy
import importlib

import os
from datetime import datetime

from multiprocessing import Process

import time

class TweetPusher():
    def __init__(self, data_path, heading="MOO, "):

        self.data_path = data_path
        with open(f"{self.data_path}/twitter-keys","r") as keyf:
            # Getting keys from the file and removing the newline
            keys = [key[0:-1] for key in keyf.readlines()]

            auth = tweepy.OAuthHandler(keys[0], keys[1])
            auth.set_access_token(keys[2], keys[3])

            self.api = tweepy.API(auth)
            print ("Connected to twitter")

        self.heading = heading

        p = Process(target=self.schedule_handler)
        p.start()


    def tweet(self):
        img_path = os.path.join(self.data_path, "images")
        target = os.path.join(img_path, os.listdir(img_path)[-1])
        self.api.update_with_media(target, self.heading)
        ## get rid of the target
        os.remove(target)
        print(f"{datetime.now()} | {target} has been tweeted")

    def schedule_handler(self):
        self.schedule = importlib.import_module("schedule")

        for hour in ["03:00", "09:00", "11:00", "16:00", "19:00"]:
            self.schedule.every().day.at(hour).do(self.tweet)


        while 1:
            n = self.schedule.idle_seconds()
            if n is None:
                break
            elif n > 0:
                time.sleep(n)
            self.schedule.run_pending()
