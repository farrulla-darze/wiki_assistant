from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
import os
import re

api_key = "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"


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

    def __init__(self, api_key=api_key, descriptions="data/descriptions/", description_paths="data/descriptions_paths.txt"):
        
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        
        docs = []
        description_text = []
        description_text_files = []
        path_dict = {}


        image_paths = []
        with open(description_paths, "r") as f:
            image_paths = f.readlines()

        image_paths = [image_path.strip() for image_path in image_paths]
        
        description_text_files = os.listdir(descriptions)
        description_text_files = sort_nicely(description_text_files)
        print(len(description_text_files))
        print(len(image_paths))

        # Sort description based on number
        for i,file in enumerate(description_text_files):
            print("Prefile = ",description_text_files[i])

        i = 0
        total_files = len(description_text_files)

        for file in description_text_files:
            if (i == total_files):
                print("File = ", i)
                break
            else: 
                print("File before = ", i, description_text_files[i])
                with open(descriptions + file, "r") as f:
                    content = f.read()
                    description_text.append(content)
                    description_text_files.append(file)
                    docs.append(Document(page_content=content, metadata={"image_path": image_paths[i], "source": file}))
                    path_dict.update({file: image_paths[i]})
            i+=1
        # print(path_dict)

        loader = TextLoader(descriptions)
        image_paths = ["data/doc_images/" + image for image in os.listdir("data/doc_images/")] 
        # add image path to metadata
        loader.metadata = image_paths
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=0,
            length_function=len
        )

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

        # image_paths = [document.metadata["image_path"] for document in documents]
        # Look for the image path in the description_dict
        image_paths = []
        for document in documents:
            print("Document = ",document.metadata)
            image_paths.append(self.source_path[document.metadata["source"]])
        return image_paths

d = Database()
# print(d.search("multimeter", 1))
print("IMAGE PATH =====",d.search_image("multimeter", 1))
# a = ["data/descriptions/" + text for text in os.listdir("data/descriptions/")]
# print(sort_nicely(a))
