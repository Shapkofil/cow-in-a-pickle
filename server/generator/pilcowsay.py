from PIL import Image, ImageDraw, ImageFont

import numpy as np
import subprocess
import random
import os
import time
from datetime import datetime
import sys


class PilCowsay():
    def __init__(self,
                 text="",
                 img_size=(1200, 675),
                 font="SourceCodePro-Bold.otf",
                 font_size=42):

        self.fnt = ImageFont.truetype(font, font_size)
        self.img_size = img_size

        if not text == "":
            self.gen_text(text)

    def gen_text(self, content):
        output = os.popen(f"""echo "{content}" | cowsay""").read()
        self.content = output
        return self.content

    def gen_img(self, linespacing=1.5):

        self.img = Image.new("RGB", self.img_size, (20, 20, 20))

        gradient = Image.new("HSV", self.img_size, (255, 255, 255))
        d = ImageDraw.Draw(gradient)
        hue = random.randrange(256)
        lerp = lambda x, y, a: int(x * a + y * (1 - a)) % 255
        for i in range(self.img_size[0] * 2):
            d.line([(i, 0), (0, i)],
                   (lerp(hue, hue + 100,
                         float(i) / (self.img_size[0] * 2)), 255, 255),
                   width=1)
        gradient = gradient.convert("RGB")

        text_mask = Image.new("L", self.img_size, 255)
        d = ImageDraw.Draw(text_mask)
        w, h = d.textsize(self.content, font=self.fnt)
        d.text(((self.img_size[0] - w) / 2, (self.img_size[1] - h) / 2),
               self.content,
               fill=0,
               font=self.fnt,
               align="left")

        self.img = Image.composite(self.img, gradient, text_mask)

        return self.img


def gen_tweet_image(text, path = "../../data/images"):
    pilcowsay = PilCowsay(text=text)

    timestamp = str(datetime.now().strftime("%Y%m%d_%H-%M-%S"))

    img = pilcowsay.gen_img()

    img.save(f"{path}/{timestamp}.png");
    print(f"Tweet generated {timestamp}")
    return img
