import os
import base64
import requests
import json
import re
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
openai_key = os.getenv('OPENAI_KEY')


class Vision():

    def __init__(self, api_key=openai_key, image_paths=None):
        self.api_key = api_key
        self.image_paths = image_paths 

    def encode_image(self, image_path):
        with open(image_path, "rb") as f:
            image = f.read()
            base64_image = base64.b64encode(image).decode("utf-8")
        return base64_image
    
    def describe_images(self, image_paths, prompt="What is in this image?",new_gen=False, save_gen=True, save_path="data/descriptions.txt", save_image_paths="data/descriptions_paths.txt",test=False):
        
        if (os.path.exists("data/descriptions.txt") and not new_gen and test):
            # Use pre-generated descriptions
            print("Using pre-generated descriptions")
            if (test):
                with open("data/descriptions_inspect.txt", "r") as f:
                    descriptions = f.read()
                    descriptions_dict = {}
                    json_matches = re.findall(r"```json(.*?)```", descriptions, re.DOTALL)
                    for i,match in enumerate(json_matches):
                        try:
                            json_dict = json.loads(match)
                            # print(json_dict)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                        descriptions_dict.update({image_paths[i]: json_dict})
                    # print(descriptions_dict)
            else:
                with open("data/descriptions.txt", "r") as f:
                    if (test):
                        descriptions = f.readlines()
                    else:
                        descriptions = f.readlines()
                    descriptions_dict = {image_path: description for image_path, description in zip(image_paths, descriptions)}
        else:
            # Generate new descriptions
            print("Generating new descriptions")
            # Use gpt model to generate text
            descriptions = []
            descriptions_dict = {}
            for image_path in image_paths:
                print(image_path)      
                base64_image = self.encode_image(image_path)


                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }

                payload = {
                    "model": "gpt-4-vision-preview",
                    "messages": [ {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }],
                    # ]
                    "max_tokens": 500
                }

                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                print(response.json())
                model_output = response.json().get("choices")[0].get("message").get("content")

                descriptions.append(model_output)
                descriptions_dict.update({image_path: model_output})
            
        # Save descriptions to a file
        if (save_gen):
            if (type(save_path) == list):
                for i, path in enumerate(save_path):
                    with open(path, "w") as f:
                        f.write(descriptions[i])
                for i, path in enumerate(save_image_paths):
                    # create file if non existent
                    with open(path, "w") as f:
                        f.write(image_paths[i])
                    # with open(path, "w") as f:
                    #     f.write(image_paths[i])
            else:
                with open(save_path, "w") as f:
                    for description in descriptions:
                        f.write(description + "\n")
                with open(save_path[:-4]+"_paths.txt", "w") as f:
                    for image_path in image_paths:
                        f.write(image_path + "\n")

        return descriptions_dict

# v = Vision()
# imgs = ["data/doc_images/INSPECTION_REPORT.pdf/"+img for img in os.listdir("data/doc_images/INSPECTION_REPORT.pdf/")]


# save_paths = []
# save_image_paths = []

# for img in imgs:
#     save_paths.append("data/descriptions/INSPECTION_REPORT.pdf/"+img.split("/")[-1][:-4]+".txt")
#     save_image_paths.append("data/descriptions/paths/INSPECTION_REPORT.pdf/"+img.split("/")[-1][:-4]+"_path.txt")


# # imgs.sort()
# # print(imgs)
# prompt = """You are analyzing an inspection report of a industrial setting of valve manufacturing. 
# Your job is to analyze images in this report. If the image shows any captions or text, incorporate that into your description.
# If the image appears shows any machinery, equipment, or tools, attempt to name the machinery.
# If the image shows any sensor readings, write down the readings and the sensor type."""
# print(v.describe_images(imgs,prompt=prompt, new_gen=True, save_gen=True, save_path=save_paths, save_image_paths=save_image_paths))
