#!/usr/bin/env python3
#

from pqueue import Queue

class TextHandler():
    def generator(self):
        while True:
            if self.q.empty():
                yield "empty queue".encode()
            result = self.q.get()
            self.q._saveinfo()
            yield result

    def __init__(self, data_dir):
        self.q = Queue(f"{data_dir}/vault", tempdir=f"{data_dir}/tmp")
        self.data_dir = data_dir
        self.refresh()

    def refresh(self):
        self.q = Queue(f"{self.data_dir}/vault", tempdir=f"{self.data_dir}/tmp")
        self.text = next(self.generator()).decode("UTF-8")
        self.text = self.text[6:] + ", Moo"

    def save(self, text):
        self.text = "save"
