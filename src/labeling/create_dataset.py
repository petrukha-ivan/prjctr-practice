import pandas as pd
import argilla as rg


client = rg.Argilla(
    api_url='http://0.0.0.0:6900', 
    api_key='admin.apikey'
)


def create_dataset():
    guidelines = '''
    Check is email fraudent and have following triggers: require urgent answer, asks to perform some action on untrusted website, asks for confidential information or financial transfer.
    '''

    dataset_name = 'is-fraud-email'
    settings = rg.Settings(
        guidelines=guidelines,
        fields=[
            rg.TextField(
                name='text',
                title='Text',
                use_markdown=False,
            )
        ],
        questions=[
            rg.LabelQuestion(
                name='class',
                title='Identify is this text fraudent (1) or not (0)',
                required=True,
                labels=['fraud', 'benign']
            )
        ],
    )

    dataset = rg.Dataset(
        name=dataset_name,
        workspace='admin',
        settings=settings,
        client=client,
    )

    dataset.create()
    dataset = client.datasets(name=dataset_name)

    records = []
    data = pd.read_csv('data/fraud-email.csv')
    for i, row in data.iterrows():
        records.append(
            rg.Record(
                fields={
                    'text': row['Text']
                }
            )
        )
    
    dataset.records.log(records, batch_size=1000)


if __name__ == '__main__':
    create_dataset()