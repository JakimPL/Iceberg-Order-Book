from time import time


class Timer:
    current_time: float

    def __call__(self):
        new_time = time()
        delta_time = new_time - self.current_time
        self.current_time = new_time
        return delta_time

    def __init__(self):
        self.current_time = time()
