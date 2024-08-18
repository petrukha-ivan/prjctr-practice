import pandas as pd
from streaming import MDSWriter
from streaming import StreamingDataset
from minio import Minio
from pathlib import Path
from tempfile import TemporaryDirectory


def write_dataset(data: pd.DataFrame, client: Minio):
    with TemporaryDirectory() as dir:
        writer = MDSWriter(out=dir, columns={'text': 'str', 'class': 'int'})    
        with writer as output:
            for i, row in data.iterrows():
                output.write({
                    'id': i,
                    'text': row['Text'],
                    'class': row['Class']
                })

        for file_path in Path(dir).iterdir():
            client.fput_object('dataset', f'v1/{file_path.name}', file_path)


def main():
    # Write dataset to bucket
    data = pd.read_csv('data/fraud-email.csv')
    data = pd.concat([data, data, data, data, data, data, data, data, data]) # Repeat data just for test
    client = Minio(endpoint='0.0.0.0:9000', access_key='minioadmin', secret_key='minioadmin', secure=False)
    write_dataset(data, client)

    # Read dataset stream from bucket
    dataset = StreamingDataset(remote='s3://dataset/v1', local='.cache/dataset')
    print(dataset[0])


if __name__ == '__main__':
    main()