import lancedb
import pandas as pd
from sentence_transformers import SentenceTransformer


def write_embeddings():
    data = pd.read_csv('data/fraud-email.csv')
    model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
    embeddings = model.encode(data['Text'], show_progress_bar=True)

    data = [
        {
            'id': i,
            'text': data.iloc[i]['Text'],
            'vector': embeddings[i],
            'class': data.iloc[i]['Class'],
        }
        for i in range(len(data))
    ]

    db = lancedb.connect('.lancedb')
    lance_table = db.create_table('emails', data=data)
    lance_table.create_index()


def search_query(query):
    model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
    embedding = model.encode(query)

    db = lancedb.connect('.lancedb')
    table = db.open_table('emails')

    results = table.search(embedding).limit(3).to_list()
    for result in results:
        print('---')
        print(result['text'])
        print(result['class'])
        print('---')


def main():
    write_embeddings()
    search_query('urgent pay')


if __name__ == '__main__':
    main()