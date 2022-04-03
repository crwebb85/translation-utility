from pathlib import Path
from typing import Iterable
import fileinput
import os

import os
import sys
from contextlib import ContextDecorator

class RotatingFile(ContextDecorator):
    def __init__(self, directory='', filename='foo', max_files=sys.maxsize,
        max_file_size=50000, encoding='utf-8'):
        self.ii = 1
        self.directory, self.filename      = directory, filename
        self.base_filename, self.file_extension = os.path.splitext(filename)
        self.max_file_size, self.max_files = max_file_size, max_files
        self.finished, self.fh             = False, None
        self.encoding                      = encoding
        self.pending_text                   = None
        self.open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def rotate(self, pending_text_length=0):
        """Rotate the file, if necessary"""
        if (os.stat(self.filename_template).st_size + pending_text_length >self.max_file_size):
            self.fh.flush()
            self.fh.close()
            self.ii += 1
            if (self.ii<=self.max_files):
                self.open()
            else:
                self.close()
                self.finished = True

    def open(self):
        self.fh = open(self.filename_template, 'w', encoding=self.encoding)

    def write(self, text=""):
        if self.pending_text is not None:
            pending_text_length = len(self.pending_text.encode(self.encoding))
            self.rotate(pending_text_length)
            self.commit()
        self.pending_text = text

    def commit(self):
        if(self.pending_text is not None):
            self.fh.write(self.pending_text)
            self.pending_text = None
        self.fh.flush()
        
    def close(self):
        self.commit()
        self.fh.close()

    @property
    def filename_template(self):
        filename = self.base_filename + '_%0.2d' % self.ii + self.file_extension
        return os.path.join(self.directory, filename)

def get_paragraphs(fileobj, separator='\n', include_empty_lines=False):
    if separator[-1:] != '\n': separator += '\n'
    paragraph = []
    for line in fileobj:
        if line == separator:
            if paragraph:
                yield ''.join(paragraph)
                paragraph = []
            if line == separator and include_empty_lines:
                yield line
        else:
            paragraph.append(line)
    if paragraph: 
        yield ''.join(paragraph)


def get_paragraphs_from_files(file_paths: Iterable[Path]):
    resolved_file_paths = [str(file_path.resolve()) for file_path in file_paths]
    for resolved_file_path in resolved_file_paths:
        with open(resolved_file_path, 'r', encoding='utf-8') as f:
            yield from get_paragraphs(f)


def resize_files(all_files: Iterable[Path], output_path, output_file_name="out.txt", max_file_size=1000000):
    output_dir = str(output_path.resolve())
    with RotatingFile(directory = output_dir, filename=output_file_name, max_file_size=max_file_size) as out_file_handler:
        for paragraph in get_paragraphs_from_files(all_files):
            text = paragraph + '\n'
            out_file_handler.write(text)
