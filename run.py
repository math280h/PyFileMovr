import argparse

from pyfilemovr.pyfilemovr import PyFileMovr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move all files from one destination to the other"
    )
    parser.add_argument(
        "-i", "--input", type=str, help="Destination to move files from"
    )
    parser.add_argument("-o", "--output", type=str, help="Destination to move files to")
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        help="Only move files with this extension (Default: *)",
    )
    parser.add_argument(
        "-d",
        "--duplicates",
        type=bool,
        help="If true all file hashes will be compared and only the "
        "first in a series of duplicates will be moved ("
        "Default: False)",
    )
    parser.add_argument(
        "--debug", type=bool, help="Toggles debug mode (Default: False)"
    )
    args = parser.parse_args()

    if args.input is None or args.output is None:
        exit(1)

    app = PyFileMovr(
        args.input, args.output, args.extension, args.duplicates, args.debug
    )
    app.run()
