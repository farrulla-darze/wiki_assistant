import os
import dotenv
import pandas as pd
import pinecone
import pinecone_datasets
import time
from utils import chunks, num_tokens_from_string

class VectorDB:
    def __init__(self, pinecone_key, pinecone_environment='gcp-starter'):
        self.pinecone_key = pinecone_key
        self.pinecone_environment = pinecone_environment
        pinecone.init(api_key=self.pinecone_key, environment=pinecone_environment)


    def list_datasets(self):
        """Returns a list of available datasets."""
        datasets_list = pinecone_datasets.list_datasets()
        return datasets_list

    def get_dataset(self, dataset_name) -> pd.DataFrame:
        """Returns a pandas dataframe of the dataset.

        Args:
            dataset_name (str): The name of the dataset to load.

        Returns:
            pd.DataFrame: A pandas dataframe of the dataset.
        """
        self.dataset = pinecone_datasets.load_dataset(dataset_name)
        self.df: pd.DataFrame = self.dataset.documents
        return self.df


if __name__ == '__main__':
    dotenv.load_dotenv()
    pinecone_key=os.getenv('PINECONE_API_KEY')

    #pine = VectorDB(pinecone_key=pinecone_key, pinecone_environment='gcp-starter')

    # Init Pinecone
    pinecone.init(api_key=pinecone_key, environment='gcp-starter')

    # List indexes
    active_indexes = pinecone.list_indexes()
    print(active_indexes)

    # Create index
    name='wiki-pages'
    dimension=1536  #  returned dim from text-embeddings-ada-002 openai model
    metric='cosine'
    if name not in active_indexes:
        pinecone.create_index(name=name, dimension=dimension, metric=metric)
        print(pinecone.list_indexes())

        # Wait for index to be created
        time.sleep(2)
    else:
        print(f'Index {name} already exists.')


    # connect to index
    index = pinecone.Index(name)
    print(index.describe_index_stats())  # describe index stats

    # Load dataset
    dataset_name = 'wikipedia-simple-text-embedding-ada-002-100K'
    pine = VectorDB(pinecone_key=pinecone_key, pinecone_environment='gcp-starter')
    df = pine.get_dataset(dataset_name=dataset_name)
    df = df.head(300)

    # upsert vectors
    for chunk in chunks(iterable=df, batch_size=100):
        print(chunk)

    # Wait for index to be updated
    time.sleep(2)
    # describe index stats
    print(index.describe_index_stats())

