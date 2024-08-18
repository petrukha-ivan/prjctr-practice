import os
import time
import tempfile
import contextlib


@contextlib.contextmanager
def time_profile(label=''):
    start_time = time.time()
    try:
        yield start_time
    finally:
        elapsed_time = time.time() - start_time
        print(f'{label} time: {elapsed_time:.6f} seconds')


@contextlib.contextmanager
def file_profile(label='', suffix=''):
    with tempfile.NamedTemporaryFile('w+', suffix=suffix) as file:
        file_path = file.name
        try:
            yield file_path
        finally:
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            print(f'{label} size: {file_size} MB')