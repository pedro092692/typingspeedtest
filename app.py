import tkinter as tk
from tkinter import Text, WORD, Button
from tkinter import ttk, Label
from essential_generators import MarkovTextGenerator

PARAGRAPH_LENT = 70
TIME = 59


class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()

        # main setup
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.resizable(False, False)
        self.option_add('*Label.Font', 'Helvetica 20')
        self.option_add('*Text.Font', 'Helvetica 20')
        # main
        self.main_text = Paragraph(self)
        self.input_text = TextInput(self)
        self.timer = Timer(self)

        # run
        self.mainloop()

    @staticmethod
    def get_paragraph():
        paragraph = MarkovTextGenerator()
        random_paragraph = paragraph.gen_text(max_len=PARAGRAPH_LENT)
        return random_paragraph


class Paragraph(ttk.Frame):
    def __init__(self, parent: App):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=0.8, relheight=0.5)
        self.create_widget(parent)

    def create_widget(self, parent: App):
        global principal_text
        global text_wrote
        text = parent.get_paragraph()
        principal_text = Label(self, text=text.lower(), fg='black', wraplength=700, justify='left')
        text_wrote = Label(self, text='', fg='black', wraplength=700, justify='left')
        principal_text.place(relx=0, rely=0, relwidth=1, relheight=1)


class TextInput(ttk.Frame):
    def __init__(self, parent: App):
        super().__init__(parent)
        self.place(relx=0, rely=0.5, relwidth=0.8, relheight=0.5)
        self.create_widget(parent)
        self.parent = parent
        global passed_seconds
        global writeable
        writeable = True
        passed_seconds = 0

    def create_widget(self, parent: App):
        global main_text_input
        main_text_input = Text(self, padx=50, pady=50, wrap=WORD)
        main_text_input.place(relx=0, rely=0, relwidth=1, relheight=1)
        main_text_input.bind('<Key>', self.count_word)

    def restart_text(self):
        new_text = self.parent.get_paragraph()
        principal_text.configure(text=new_text)

    def start_timer(self):
        global passed_seconds
        passed_seconds += 1
        time.configure(text=f'{passed_seconds} seconds')

        if passed_seconds <= TIME:
            self.after(1000, self.start_timer)
        else:
            self.end_test()
            global wpm
            global reset_button
            amount_words = len(text_wrote.cget('text').split(' '))
            wpm = Label(self.parent, text=f'WPM: {amount_words}', fg='black', font='helvetica 50')
            wpm.place(rely=0.3, relx=0.5, anchor='center')
            reset_button = Button(self.parent, text='Reset', font='helvetica 30', command=self.reset)
            reset_button.place(rely=0.5, relx=0.5, anchor='center')


    def count_word(self, event):
        # start timer
        if passed_seconds == 0:
            self.start_timer()
        try:
            if event.char.lower() == principal_text.cget('text')[0]:
                principal_text.configure(text=principal_text.cget('text')[1:])

                # update text wrote
                text_wrote.configure(text=text_wrote.cget('text') + event.char)
        except IndexError:
            self.restart_text()

    def end_test(self):
        time.destroy()
        principal_text.destroy()
        main_text_input.destroy()

    def reset(self):
        reset_button.destroy()
        wpm.destroy()
        Paragraph(parent=self.parent)
        TextInput(parent=self.parent)
        Timer(parent=self.parent)


class Timer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)
        self.create_widget(parent)

    def create_widget(self, parent):
        global time
        time = Label(self, text=f'0 Seconds', fg='black')
        time.place(rely=0, relx=0, relwidth=1)



