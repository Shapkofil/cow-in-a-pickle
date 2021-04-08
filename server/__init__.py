#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', tweet_text="Iuno man")

@app.route('/accept')
def accept():
    return redirect('/')

@app.route('/deny')
def deny():
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")