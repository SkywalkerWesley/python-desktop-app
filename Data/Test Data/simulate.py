import os
import shutil
import time

source_folder = r"Acquisition-4971"

destination_folder = r"test"

os.makedirs(destination_folder, exist_ok=True)

os.makedirs(destination_folder, exist_ok=True)

for filename in os.listdir(destination_folder):
    file_path = os.path.join(destination_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

for c in range(1,10000):
    filename = f"{c}.csv"
    src_path = os.path.join(source_folder, filename)
    dest_path = os.path.join(destination_folder, filename)

    try:
        shutil.copy2(src_path, dest_path)
        print(f"Copied {filename} to {destination_folder}")
    except PermissionError as e:
        print(f"Permission error copying {filename}: {e}")
        continue
    except Exception as e:
        print(f"Error copying {filename}: {e}")
        continue

    # Wait 1 second before copying the next file
    time.sleep(0.1)



print("Done copying all CSVs!")