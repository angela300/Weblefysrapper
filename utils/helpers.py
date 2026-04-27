import time
import random

def human_delay(min_sec=3, max_sec=7):
    time.sleep(random.uniform(min_sec, max_sec))