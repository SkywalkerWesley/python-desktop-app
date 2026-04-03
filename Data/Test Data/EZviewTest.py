import time
import os

SOURCE_FILE = "Data/Test Data/EZView DataGood.txt"
DEST_FILE = "Data/Test Data/EZView DataCopy.txt"

# Delete destination file if it exists
if os.path.exists(DEST_FILE):
    os.remove(DEST_FILE)

# Open source file in read mode and destination file in append mode
with open(SOURCE_FILE, "r") as src, open(DEST_FILE, "a") as dest:
    # Optional: start at beginning
    src.seek(0)

    while True:
        line = src.readline()
        if line:
            dest.write(line)
            dest.flush()  # Make sure it's written to disk immediately
            print("Copied line:", line.strip())
        else:
            # No new line, wait 1 second
            time.sleep(0.5)