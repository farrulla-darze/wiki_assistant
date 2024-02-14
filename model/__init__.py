from model.extractor import Extractor
from model.database import Database
from model.vision import Vision
import os
# Path: model/model.py

class Model:

    _instance = None

    def __init__(self, path):
        self.extractor = Extractor(path)
        self.database = Database(descriptions="data/descriptions.txt", description_paths="data/description_paths.txt")
        self.vision = Vision()
    
    @classmethod
    def instance(cls,path="data/"):
        if cls._instance is None:
            cls._instance = cls(path)
        return cls._instance
    
    def search(self, text):
        return self.database.search(text)
    
    def search_image(self, text):
        return self.database.search_image(text)
