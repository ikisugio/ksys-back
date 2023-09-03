import time
from datetime import datetime


def wait(wait_time):
    return time.sleep(wait_time)

def today(data_format):
    return datetime.now().strftime(data_format)