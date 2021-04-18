#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request
from multiprocessing import Process
import os
import sys

from .text_handler import TextHandler
from .tweet_pusher import TweetPusher
from .generator.pilcowsay import gen_tweet_image
from .generator.shakespeare import fillqueue

app = Flask(__name__)


DATA_DIR=os.path.join(
    os.path.dirname(sys.modules['__main__'].__file__),
    "data")

text_handler = TextHandler(DATA_DIR)
tweet_pusher = TweetPusher(DATA_DIR)

@app.route('/')
def root_url():
    return redirect('/feed')

@app.route('/feed')
def feed():
    return render_template('feed.html', tweet_text=text_handler.text)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',
                           inqueue=text_handler.q.qsize(),
                           ready=len(os.listdir(f"{DATA_DIR}/images"))
                           )


@app.route('/accept', methods=['GET', 'POST'])
def accept():
    tweet_txt = request.args.get("text")
    text_handler.save(tweet_txt)
    text_handler.refresh()

    if not tweet_txt == None:
       p = Process(target=gen_tweet_image, args=(tweet_txt, os.path.join(DATA_DIR,"images")))
       p.start()

    return redirect('/feed')

@app.route('/deny')
def deny():
    text_handler.refresh()
    return redirect('/feed')

@app.route("/dashboard/force-tweet")
def forcetweet():
    tweet_pusher.tweet()
    return redirect('/dashboard')

@app.route("/dashboard/fill-feed")
def fillfeed():
    p = Process(target=fillqueue, args=(DATA_DIR, 200))
    p.start()
    return redirect('/dashboard')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
