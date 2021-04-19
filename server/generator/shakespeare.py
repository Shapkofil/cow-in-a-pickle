#!/usr/bin/env python3

import numpy as np
import os
import time
import random

import importlib
from tqdm import trange

from pqueue import Queue


class TextGenerator():
    def __init__(self, data_path, initial = 'Moo ,'):
        self.tf = importlib.import_module("tensorflow")
        self.one_step_model = self.tf.saved_model.load(f'{data_path}/one_step')
        self.initial = initial

    def gentext(self):
        states = None
        next_char = self.tf.constant([self.initial])
        result = [next_char]

        tweet_len = random.randint(12, 104)
        self.one_step_model.temperature = random.random()*2.0 + .6
        i = 0
        next_char, states = self.one_step_model.generate_one_step(next_char, states=states)
        while (not next_char in [' ', '\n']) or i<tweet_len:
            result.append(next_char)
            i+=1
            next_char, states = self.one_step_model.generate_one_step(next_char, states=states)

        result = self.tf.strings.join(result)[0]
        return result.numpy()

    def text_generator(self, batch_size):
        for i in trange(batch_size):
            yield self.gentext()

def fillqueue(data_path, count, initial = 'Moo ,'):
    try:
        os.mkdir(f"{data_path}/vault")
        os.mkdir(f"{data_path}/tmp")
    except OSError as error:
        print("Appending to an existent queue")

    q = Queue(f"{data_path}/vault", tempdir=f"{data_path}/tmp")
    model_wrap = TextGenerator(data_path, initial)
    for output in model_wrap.text_generator(count):
        q.put(output)
