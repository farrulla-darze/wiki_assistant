from vision import Vision
from datetime import datetime
import matplotlib.pyplot as plt
from database import Database

v = Vision()
files = ["data/doc_images/page_4image_1.png", "data/doc_images/page_4image_2.png", "data/doc_images/page_4image_3.png", "data/doc_images/page_4image_4.png", "data/doc_images/page_4image_5.png","data/doc_images/page_4image_6.png"]

save_gen = True
save_path = "data/multi_image.txt"
new_gen = True

# image_descriptions = v.describe_images(files, prompt=r"Describe the following image, and finish with the output being the description and whatever overlay text data in a JSON file format. Example {'description':'This is image','overlay':{'DATA':'01012011','TIME':'011241}}", save_gen=save_gen, save_path=save_path,new_gen=new_gen, test=True)
image_descriptions = v.describe_images(files, prompt=r"Describe the image with the output being the description and whatever overlay text data in a JSON file format. Example {'description':'This is image','overlay':{'DATA':'01012011','TIME':'011241}}", save_gen=save_gen, save_path=save_path,new_gen=new_gen, test=True)
