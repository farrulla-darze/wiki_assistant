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

        self.image = tk.Label(self, text="Image")
        self.image.pack()

        self.controller = None
    
    def set_controller(self, controller):
        self.controller = controller 

    def submit(self):
        # When the button is clicked, the text in the textbox is displayed in the label
        if self.controller is not None:
            self.label.text = self.controller.generate_with_text(self.textbox.get())

    def submit_image(self):
        if self.controller is not None:
            self.image.text = ""
            image_path = self.controller.generate_with_image(self.textbox.get())
            print(image_path)
            self.image.image = tk.PhotoImage(file = image_path)
