import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class View(ttk.Frame):
    # Create interface with textbox, a label written Prompt and button wrtiiten Submit

    def __init__(self, parent):
        super().__init__(parent)
        self.textbox = tk.Entry(self)
        self.textbox.pack()

        self.label = tk.Label(self, text="Prompt")
        self.label.pack()

        self.button = tk.Button(self, text="Submit", command=self.submit)
        self.button.pack()

        self.button_image = tk.Button(self, text="Submit Image", command=self.submit_image)
        self.button_image.pack()

        path = "place.jpg"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(self, image = img)
        # panel.
        panel.image = img # keep a reference!
        panel.pack()
        self.image = panel

        self.controller = None
    
    def set_controller(self, controller):
        self.controller = controller 

    def submit(self):
        # When the button is clicked, the text in the textbox is displayed in the label
        if self.controller is not None:
            self.label.config(text=self.controller.generate_with_text(self.textbox.get()))

    def submit_image(self):
        if self.controller is not None:
            self.image.text = ""
            image_paths = self.controller.generate_with_image(self.textbox.get())
            image_path = image_paths[0]
            print(image_path)
            sized_image = ImageTk.PhotoImage(Image.open(image_path).resize((400, 300)))
            self.image.image = sized_image
            self.image.config(image = self.image.image)
            self.image.pack()
