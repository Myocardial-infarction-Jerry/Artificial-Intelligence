import time


class counter(object):

    def __init__(self):
        self.refresh()

    def refresh(self):
        self.basetime = time.time()

    def print(self):
        return time.time() - self.basetime
