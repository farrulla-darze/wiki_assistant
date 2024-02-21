from tkinter import Tk

from view.interface import View
from model import Model
from controller.controller import Controller


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter MVC Demo')
        self.geometry('800x600')
        

        # create a model
        model = Model.instance()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()