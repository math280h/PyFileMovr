import hashlib
import os
import shutil
from datetime import datetime
import argparse


def walk_through_files(path, file_extension):
    try:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if file_extension is not None:
                    if filename.endswith(file_extension):
                        yield os.path.join(dirpath, filename)
                else:
                    yield os.path.join(dirpath, filename)
    except Exception as e:
        print("Error:" + str(e))


def get_date_time():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt


def hash_byte_str_iter(bytes_iter):
    hl = hashlib.sha256()
    for block in bytes_iter:
        hl.update(block)
    return hl.hexdigest()


def file_as_block_iter(file, block_size=65536):
    with file:
        block = file.read(block_size)
        while len(block) > 0:
            yield block
            block = file.read(block_size)


def main():
    parser = argparse.ArgumentParser(description='Move all files from one destination to the other')
    parser.add_argument('-i', '--input', type=str, help="Destination to move files from")
    parser.add_argument('-o', '--output', type=str, help="Destination to move files to")
    parser.add_argument('-e', '--extension', type=str, help="Only move files with this extension (Default: *)")
    parser.add_argument('-d', '--duplicates', type=bool, help="If true all file hashes will be compared and only the "
                                                              "first in a series of duplicates will be moved ("
                                                              "Default: False)")
    parser.add_argument('--debug', type=bool, help="Toggles debug mode (Default: False)")
    args = parser.parse_args()

    if args.input is None or args.output is None:
        exit(1)
    if args.duplicates is None:
        args.duplicates = False
    if args.debug is None:
        args.debug = False

    if args.duplicates is True:
        hash_list = []

    print("______     ______ _ _     ___  ___                \n"
          "| ___ \    |  ___(_) |    |  \/  |                \n"
          "| |_/ /   _| |_   _| | ___| .  . | _____   ___ __ \n"
          "|  __/ | | |  _| | | |/ _ \ |\/| |/ _ \ \ / / '__|\n"
          "| |  | |_| | |   | | |  __/ |  | | (_) \ V /| |   \n"
          "\_|   \__, \_|   |_|_|\___\_|  |_/\___/ \_/ |_|\n"
          "       __/ |\n"
          "      |___/  \n")
    print("PyFileMovr - Created by: math280h - Found at: https://github.com/math280h/PyFileMovr\n")

    if args.debug:
        print("Input path:", args.input, " Output path:", args.output, "\n")

    for file in walk_through_files(args.input, file_extension=args.extension):
        print("Current file: {}".format(file))
        if args.debug:
            print("     Hash List:", hash_list)
        try:
            if args.duplicates is True:
                fh = hash_byte_str_iter(file_as_block_iter(open(file, 'rb')))
                if args.debug:
                    print("     File hash:", fh)
                if fh not in hash_list:
                    hash_list.append(fh)
                else:
                    print("     Skipped: Duplicate")
                    continue
            shutil.move(file, args.output)
            print("     Successfully moved file")
        except shutil.Error as err:
            print("Error:" + str(err))


if __name__ == "__main__":
    main()
