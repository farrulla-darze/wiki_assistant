from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
import os
import re
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
openai_key = os.getenv('OPENAI_KEY')

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    return l

class Database():

    def __init__(self, api_key=openai_key, descriptions="data/descriptions/INSPECTION_REPORT.pdf/", description_paths="data/descriptions/paths/INSPECTION_REPORT.pdf/"):
        
        embeddings = OpenAIEmbeddings(api_key=api_key)
        
        docs = []
        path_dict = {}


        image_path_files = os.listdir(description_paths)
        image_path_files = sort_nicely(image_path_files)

        description_text_files = os.listdir(descriptions)
        description_text_files = sort_nicely(description_text_files)

        i = 0
        total_files = len(description_text_files)

        for i in range(len(description_text_files)):
            file = description_text_files[i]
            path = image_path_files[i]
            if (i == total_files):
                break
            else: 
                with open(descriptions + file, "r") as f:
                    content = f.read()
                with open(description_paths + path, "r") as f:
                    path = f.read()
                docs.append(Document(page_content=content, metadata={"image_path": path, "source": file}))
                path_dict.update({content: path})
            

        self.embeddings = embeddings
        self.source_path = path_dict
        self.vector_store = Qdrant.from_documents(
            docs,
            embeddings,
            path="/tmp/local_qdrant",
            collection_name="report_collection",
        )

    def search(self, query, k=1):
        found_docs = self.vector_store.similarity_search_with_score(query)
        search_ind = min(k, len(found_docs))
        found_docs = found_docs[0:search_ind]
        documents = [found_doc[0] for found_doc in found_docs]
        description = [document.page_content for document in documents]
        return description
    
    def search_image(self, query, k=1):
        found_docs = self.vector_store.similarity_search_with_score(query)
        search_ind = min(k, len(found_docs))        
        found_docs = found_docs[0:search_ind]
        documents = [found_doc[0] for found_doc in found_docs]

        # Look for the image path in the document
        image_paths = []
        for document in documents:
            if document.metadata["image_path"] not in image_paths:
                image_paths.append(document.metadata["image_path"])
        return image_paths
