import os
import tempfile
from contextlib import contextmanager


@contextmanager
def temporary_file_path(suffix=""):
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        os.close(fd)
        yield path
    finally:
        os.remove(path)
