from datasets import load_dataset
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import numpy as np
import torch

model_id = "openai/clip-vit-base-patch32"

processor = CLIPProcessor.from_pretrained(model_id)
model = CLIPModel.from_pretrained(model_id)

# move model to device if possible
device = 'cuda' if torch.cuda.is_available() else 'cpu'

model.to(device)


data = load_dataset(
    "jamescalam/image-text-demo",
    split="train"
)

batch = data["image"]

images = processor(images=data["image"], return_tensors="pt")['pixel_values'].to(device)
images.shape

img_emb = model.get_image_features(images)
print(img_emb.shape)
print(img_emb.min(), img_emb.max())


# detach text emb from graph, move to CPU, and convert to numpy array
img_emb = img_emb.detach().cpu().numpy()

img_emb = img_emb.T / np.linalg.norm(img_emb, axis=1)
# transpose back to (21, 512)
img_emb = img_emb.T
print(img_emb.shape)
print(img_emb.min(), img_emb.max())
