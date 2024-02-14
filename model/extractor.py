import pdfplumber
import matplotlib.pyplot as plt

class Extractor:
    def __init__(self, path):
        self.path = path
        self.document = pdfplumber.open(path)

    def extract_text(self):
        # check if is a list or single file
        if isinstance(self.path, list):
            text = ""
            for path in self.path:
                with pdfplumber.open(path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text()
        else:
            with pdfplumber.open(self.path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
        return text
    
    def extract_images(self):
        # check if is a list or single file
        if isinstance(self.path, list):
            images = []
            for path in self.path:
                with pdfplumber.open(path) as pdf:
                    for page in pdf.pages:
                        images += page.images
        else:
            with pdfplumber.open(self.path) as pdf:
                images = []
                for page in pdf.pages:
                    images += page.images
        return images
    
    def save_images(self):
        for i,page in enumerate(self.document.pages):
            images = page.images
            page_height = page.height
            for im, image in enumerate(images):
                image_bbox = (image['x0'], page_height - image['y1'], image['x1'], page_height - image['y0'])
                cropped_page = page.crop(image_bbox)
                img_obj = cropped_page.to_image(resolution=1200)
                img_obj.save(f"data/doc_images/page_{i}image_{im}.png",format="png")

e = Extractor("INSPECTION_REPORT.pdf")
# print(e.extract_images())
# plt.imshow(e.extract_images()[0])
e.save_images()