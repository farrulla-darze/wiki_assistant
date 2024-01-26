from langchain.vectorstores import Chroma
import chromadb
from chromadb import Documents, Embeddings, EmbeddingFunction
import pandas as pd
import time
from tqdm import tqdm

class ChromaDB:
    """
    Class for interacting with ChromaDB.
    """
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./data/wiki-chromadb")

    def list_collections(self):
        """
        List all collections in ChromaDB.
        """
        return self.client.list_collections()

    def create_collection(self, name: str):
        """
        Create a collection in ChromaDB.
        """
        return self.client.create_collection(name=name)

    def get_collection(self, name: str):
        """
        Get a collection in ChromaDB.
        """
        return self.client.get_collection(name=name)

    def get_or_create_collection(self, name: str):
        """
        Get or create a collection in ChromaDB.
        """
        return self.get_or_create_collection(name=name)

    def upsert(self, collection, df: pd.DataFrame):
        """
        upsert documents into a collection in ChromaDB.
        add if not exists, update if exists.
        """
        start = time.time()
        for i, row in df.iterrows():
            print(f"Adding document {i}")
            collection.upsert(
                ids=row["id"],
                embeddings=row["values"].tolist(),
                metadatas=[row["metadata"]],  # encapsulate dict in a list
            )
        end = time.time()
        duration = (end - start)
        print(f"Adding documents took {(duration // 60):.0f} min {(duration % 60):.2f} sec")

    def delete_collection(self, name: str):
        """
        Delete a collection in ChromaDB.
        """
        return self.client.delete_collection(name=name)

    def query(self, collection, query_embed: list, top_k: int) -> dict:
        """
        Query a collection in ChromaDB.
        """
        res = collection.query(
            query_embeddings=query_embed,
            n_results=top_k,
        )
        # print structured results
        for i in range(len(res['ids'][0])):
            print(f"{i + 1} - {res['ids'][0][i]} - {(res['distances'][0][i]):.2f}")
            print(f"{res['metadatas'][0][i]['title']}")
            print(f"{res['metadatas'][0][i]['text'][:300]}...\n")

        return res




if __name__ == "__main__":
    db = ChromaDB()
    name = "wiki-pages"

    for collection in db.list_collections():
        if name == collection.name:
            print(f"Collection {name} already exists.")
            break
    else:
        db.create_collection(name=name)
        print(f"Collection {name} created.")
        time.sleep(2)
    collection = db.get_collection(name=name)
    print(f"List of Collections: {db.list_collections()}")

    # get data from pkl
    df = pd.read_pickle("./data/wikipedia-simple-text-embedding-ada-002-100K.pkl")
    df = df.drop(columns=['sparse_values', 'metadata'])
    df = df.rename(columns={'values': 'embeddings', 'blob': 'metadatas'})

    # make embeddings list
    df["embeddings"] = df["embeddings"].apply(lambda x: x.tolist())
    # make metadatas list
    df["metadatas"] = df["metadatas"].apply(lambda x: [x])


    # upsert data
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        collection.upsert(
            ids=[row["id"]],
            embeddings=row["embeddings"],
            metadatas=row["metadatas"],
        )

    time.sleep(2)
    print(f"Total documents: {collection.count()}")
    for item in collection.peek():
        print(item)



