"""
Quick test for data logging.
"""

import time

max = 10
i = 0

f = open("data.csv", "w")
f.close()

f = open("data.csv", "a")

while i < max:
    f.write(str(i) + "\n")
    i += 1
    time.sleep(1)

f.close()

