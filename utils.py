import tiktoken

import numpy as np


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def chunks(df, batch_size=100):
        """Yield successive n-sized chunks from df.

        Args:
            df (pd.DataFrame): A pandas dataframe.
            batch_size (int, optional): The size of each batch. Defaults to 100.

        """
        for i in range(0, len(df), batch_size):
            yield df.iloc[i:i + batch_size]


def create_embeddings(input: str, client) -> np.ndarray:
    """Returns a numpy array of embeddings for a text string."""
    # Load model
    model_name = 'text-embeddings-ada-002'
    response = client.embeddings.create(
        model=model_name,
        input=input,
    )
    query_embedding = response.data[0].embedding
    return query_embedding