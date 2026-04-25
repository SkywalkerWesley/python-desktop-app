import random
import time
import os

""" Copy's EZView file line by line to EZView DataCopy in a way similar to the Machine
    run this program then selcect the EZview data copy file as the EZview folder in the Lab view program
    """

SOURCE_FILE = "Data/Test Data/EZView_DataGood.txt"
DEST_FILE = "Data/Test Data/EZView_DataCopy.txt"

# Delete destination file if it exists
if os.path.exists(DEST_FILE):
    os.remove(DEST_FILE)

# Open source file in read mode and destination file in append mode
with open(SOURCE_FILE, "r") as src, open(DEST_FILE, "a") as dest:
    # Optional: start at beginning
    src.seek(0)

    while True:
        num = random.randint(80, 100)
        for i in range(num):
            line = src.readline()
            if line:
                dest.write(line)
                dest.flush()  # Make sure it's written to disk immediately
                print("Copied line:", line.strip())
        time.sleep(0.08)
