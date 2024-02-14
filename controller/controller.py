class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def generate_with_text(self, text):
        return self.model.search(text)
    
    def generate_with_image(self, text):
        return self.model.search_image(text)
