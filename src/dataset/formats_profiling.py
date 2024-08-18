import numpy as np
import pandas as pd
from utils import time_profile, file_profile


def test_csv(data: pd.DataFrame):
    with file_profile('CSV', '.csv') as file_path:
        with time_profile('CSV save'):
            data.to_csv(file_path)
        with time_profile('CSV read'):
            pd.read_csv(file_path)


def test_json(data: pd.DataFrame):
    with file_profile('JSON', '.json') as file_path:
        with time_profile('JSON save'):
            data.to_json(file_path, orient='records')
        with time_profile('JSON sead'):
            pd.read_json(file_path, orient='records')


def test_json_lines(data: pd.DataFrame):
    with file_profile('JSONL', '.jsonl') as file_path:
        with time_profile('JSONL save'):
            data.to_json(file_path, orient='records', lines=True)
        with time_profile('JSONL read'):
            pd.read_json(file_path, orient='records', lines=True)


def test_hdf(data: pd.DataFrame):
    with file_profile('HDF', '.h5') as file_path:
        with time_profile('HDF save'):
            data.to_hdf(file_path, key='data')
        with time_profile('HDF read'):
            pd.read_hdf(file_path)


def test_pickle(data: pd.DataFrame):
    with file_profile('Pickle', '.pickle') as file_path:
        with time_profile('Pickle save'):
            data.to_pickle(file_path)
        with time_profile('Pickle read'):
            pd.read_pickle(file_path)


def test_feather(data: pd.DataFrame):
    with file_profile('Feather', '.feather') as file_path:
        with time_profile('Feather save'):
            data.to_feather(file_path)
        with time_profile('Feather read'):
            pd.read_feather(file_path)


def test_parquet(data: pd.DataFrame):
    with file_profile('Parquet', '.parquet') as file_path:
        with time_profile('Parquet save'):
            data.to_parquet(file_path)
        with time_profile('Parquet read'):
            pd.read_parquet(file_path)


def test_npy(data: pd.DataFrame):
    with file_profile('Numpy', '.npy') as file_path:
        with time_profile('Numpy save'):
            np.save(file_path, data.to_numpy())
        with time_profile('Numpy read'):
            np.load(file_path, allow_pickle=True)


def main():
    data = pd.read_csv('data/fraud-email.csv')
    test_csv(data)
    test_json(data)
    test_json_lines(data)
    test_hdf(data)
    test_pickle(data)
    test_feather(data)
    test_parquet(data)
    test_npy(data)


if __name__ == '__main__':
    main()