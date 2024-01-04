import os
import subprocess
import sys
from collections import defaultdict
from pprint import pp


SOURCE_PATH = "/storage/self/primary"
TARGET_DIR_NAME = "DCIM"
SOURCE_DIR = os.path.join(SOURCE_PATH, TARGET_DIR_NAME)
OUT_DIR = os.path.join(os.path.expanduser("~"), "saved")


def _execute(command):
    process = subprocess.Popen(command)
    while True:
        if process.poll() is not None:
            break


def act_on_batch(batch, entries, dry_run=False):
    print(f"Starting batch #{batch}:")
    for entry in entries:
        try:
            out_dir = f"{OUT_DIR}/{TARGET_DIR_NAME}_{batch}"
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir, exist_ok=True)
            command = [
                "adb",
                "pull",
                f"{SOURCE_DIR}/{entry}",
                out_dir,
            ]
            if dry_run:
                print(f"Executing: `{command!r}`")
            else:
                _execute(command)
        except KeyboardInterrupt:
            print("\nInterrupted by the user.")
            break


def iterate_over(filepath):
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


def check_all_batches_total(batches):
    return sum(
        len(batches[batch])
        for batch
        in batches
    )


def main():
    batch_size = 1000
    batches = defaultdict(list)
    current_batch = c = lines = 0
    filepath = "./files_list.txt"  # you must create this on the phone, see .sh

    for line in iterate_over(filepath):
        c += 1
        batches[current_batch].append(line)
        if c % batch_size == 0:
            c = 0
            current_batch += 1
        lines += 1

        # if check_all_batches_total(batches) == 1000:
        #     break

    # print(lines)
    # exit(0)

    # pp(batches, width=20)

    assert check_all_batches_total(batches) == lines

    filename, *args = sys.argv
    if len(args) == 1:
        arg = args[0]
        try:
            batch = int(arg)
            if 0 <= batch <= max(batches.keys()):
                act_on_batch(batch, batches[batch])
        except (TypeError, ValueError) as e:
            print(str(e))
            exit(1)


if __name__ == "__main__":
    main()