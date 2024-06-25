import tkinter as tk
from essential_generators import MarkovTextGenerator

class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()

        # main setup
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.paragraph = MarkovTextGenerator()
        print(self.paragraph.gen_text(max_len=50))
        # run
        self.mainloop()