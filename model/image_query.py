from vision import Vision
from datetime import datetime
import json
import requests
from openai import OpenAI
import matplotlib.pyplot as plt
    
v = Vision()
api_key = v.key

client = OpenAI(api_key=api_key)

files = ["data/doc_images/page_4image_1.png", "data/doc_images/page_4image_2.png", "data/doc_images/page_4image_3.png", "data/doc_images/page_4image_4.png", "data/doc_images/page_4image_5.png","data/doc_images/page_4image_6.png"]
save_gen = False
save_path = "data/multi_image.txt"
new_gen = False

image_descriptions = v.describe_images(files, prompt=r"Describe the following image, and finish with the output being the description and whatever overlay text data in a JSON file format. Example {'description':'This is image','overlay':{'DATA':'01012011','TIME':'011241}}", save_gen=save_gen, save_path=save_path,new_gen=new_gen, test=True)

# Translate prompt into dictionary values
search_query = "Translate the following request into a JSON: Images after 01012011"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

# OpenAI API endpoint
api_endpoint = 'https://api.openai.com/ v1/chat/gpt-3.5-turbo/completions'

# User query
user_query = 'Translate the following text into a json of the described filters: Give me images which date after 01-01-2011'

# Format the query into a JSON structure
json_data = {
    "prompt": user_query,
    "max_tokens": 100,
    "model": "gpt-3.5-turbo",
    # Add any other relevant parameters as needed for your use case
}



# Convert the JSON data to a string
payload = json.dumps(json_data)

# Set up headers with the API key
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": user_query}],
    stream=True,
)

response_dict_str = ""
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
        response_dict_str += chunk.choices[0].delta.content

response_dict = json.loads(response_dict_str)
print("\n",response_dict["filters"]["date"]["after"])

last_date = datetime.strptime(response_dict["filters"]["date"]["after"], '%d-%m-%Y')

for description in image_descriptions:
    # print(f"Image: {path}")
    overlay_info = image_descriptions[description]["overlay"]

    try:

        captioned_date = datetime.strptime(overlay_info["DATA"], '%d%m%Y')
        if captioned_date:
            if captioned_date > last_date:
                print(f"{captioned_date} Date after last date")
                # Show image
                plt.imshow(plt.imread(description))
                plt.show()
        else:
            print("Date before last date")
    except:
        captioned_date = "Date not in format DDMMYYYY"
