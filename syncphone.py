import argparse
import os
import subprocess
import sys

BASE_DIR = "/storage/emulated/0/"


def main():
    parser = argparse.ArgumentParser(
        description="Copy files from phone to local system",
    )
    parser.add_argument("source", help="Source folder on the phone")
    parser.add_argument("destination", help="Destination folder on local system")

    args = parser.parse_args()

    try:
        copy_files(args.source, args.destination)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def copy_files(source, destination):
    subprocess.run([
        "adb",
        "pull",
        os.path.join(BASE_DIR, source),
        destination,
    ], check=True)


if __name__ == "__main__":
    main()
