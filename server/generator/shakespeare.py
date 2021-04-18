#!/usr/bin/env python3

import tensorflow as tf
import numpy as np
import os
import time
import random

from tqdm import trange

from pqueue import Queue


class TextGenerator():
    def __init__(self, data_path):
        self.one_step_model = tf.saved_model.load(f'{data_path}/one_step')

    def gentext(self, initial = ['Moo ,'], ):
        states = None
        next_char = tf.constant(initial)
        result = [next_char]

        tweet_len = random.randint(12, 104)
        self.one_step_model.temperature = random.random()*2.0 + .6
        i = 0
        next_char, states = self.one_step_model.generate_one_step(next_char, states=states)
        while (not next_char in [' ', '\n']) or i<tweet_len:
            result.append(next_char)
            i+=1
            next_char, states = self.one_step_model.generate_one_step(next_char, states=states)

        result = tf.strings.join(result)[0]
        return result.numpy()

    def text_generator(self, batch_size):
        for i in trange(batch_size):
            yield self.gentext()

def fillqueue(data_path, count):
    try:
        os.mkdir(f"{data_path}/vault")
        os.mkdir(f"{data_path}/tmp")
    except OSError as error:
        print("Appending to an existent queue")

    q = Queue(f"{data_path}/vault", tempdir=f"{data_path}/tmp")
    model_wrap = TextGenerator(data_path)
    for output in model_wrap.text_generator(count):
        q.put(output)
