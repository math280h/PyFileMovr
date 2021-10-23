from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import os
import shutil
from typing import Any, Generator, List, Optional, Union


class PyFileMovr:
    """Main Application."""

    def __init__(
        self,
        file_input: str,
        output: str,
        extension: Optional[str],
        duplicate: Optional[bool],
        debug: Optional[bool],
    ) -> None:
        self.input = file_input
        self.output = output
        self.extension = extension

        if duplicate is None:
            self.duplicate = False
        else:
            self.duplicate = duplicate

        if debug is None:
            self.debug = False
        else:
            self.debug = debug

        if duplicate is True:
            self.hash_list: List[str] = []

    @staticmethod
    def walk_through_files(path: str, file_extension: Optional[str]) -> Generator:
        """Walk through all files in all sub-dirs."""
        try:
            for (dirpath, _, filenames) in os.walk(path):
                for filename in filenames:
                    if file_extension is not None:
                        if filename.endswith(file_extension):
                            yield os.path.join(dirpath, filename)
                    else:
                        yield os.path.join(dirpath, filename)
        except Exception as e:
            print("Error:" + str(e))

    @staticmethod
    def get_date_time() -> str:
        """Get current date_time."""
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y %H:%M:%S")
        return dt

    @staticmethod
    def hash_byte_str_iter(bytes_iter: Union[Any]) -> str:
        """Get hash hex from string."""
        hl = hashlib.sha256()
        for block in bytes_iter:
            hl.update(block)
        return hl.hexdigest()

    @staticmethod
    def file_as_block_iter(file: Any, block_size: int = 65536) -> Generator:
        """Get hash from file in blocks."""
        with file:
            block = file.read(block_size)
            while len(block) > 0:
                yield block
                block = file.read(block_size)

    def move_file(self, file: str) -> None:
        """Move files to output directory."""
        try:
            shutil.move(file, self.output)
        except shutil.Error as err:
            print("Error:" + str(err))

    def handle_queue(self, queue: List) -> None:
        """Handle the queue using threads."""
        with ThreadPoolExecutor(max_workers=12) as worker:
            worker.map(self.move_file, queue)

    def run(self) -> None:
        """Run Application."""
        print(
            "PyFileMovr - Created by: math280h - Found at: https://github.com/math280h/PyFileMovr\n"
        )

        if self.debug:
            print("Input path:", self.input, " Output path:", self.output, "\n")

        queue: List[str] = []

        for file in self.walk_through_files(self.input, file_extension=self.extension):
            print("Current file: {}".format(file))
            if self.debug:
                print("     Hash List:", self.hash_list)

            if self.duplicate is True:
                fh = self.hash_byte_str_iter(self.file_as_block_iter(open(file, "rb")))
                if self.debug:
                    print("     File hash:", fh)
                if fh not in self.hash_list:
                    self.hash_list.append(fh)
                else:
                    print("     Skipped: Duplicate")
                    continue
            queue.append(file)
            print("     Successfully moved file")

        self.handle_queue(queue)
