from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain_core.documents import Document
import torch, os
import numpy as np

model_id = "openai/clip-vit-base-patch32"

processor = CLIPProcessor.from_pretrained(model_id)
model = CLIPModel.from_pretrained(model_id)

# move model to device if possible
device = 'cuda' if torch.cuda.is_available() else 'cpu'

model.to(device)


data = ["data/doc_images/INSPECTION_REPORT.pdf/"+img for img in os.listdir("data/doc_images/INSPECTION_REPORT.pdf/")]

# batch = data["image"]

batch = [Image.open(img) for img in data]

images = processor(images=batch, return_tensors="pt")['pixel_values'].to(device)
images.shape

img_emb = model.get_image_features(images)
# detach text emb from graph, move to CPU, and convert to numpy array
img_emb = img_emb.detach().cpu().numpy()
img_emb = img_emb.T / np.linalg.norm(img_emb, axis=1)
# transpose back to (21, 512)
img_emb = img_emb.T

documents = []

for i in range(len(img_emb)):
    documents.append(Document(page_content=images, metadata={"image_path": data[i]}))


# vec_db = Qdrant.from_documents(
#     documents,
#     model,
#     path="/tmp/local_img_emb_qdrant",
#     collection_name="img_emb_collection",
# )

client = QdrantClient()
collection_name = "img_emb_collection"
qdrant = Qdrant(client, collection_name, embeddings=img_emb)
