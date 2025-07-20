# Typing speed is defined as "words" per minute. "word" is defined as 5 characters (including spaces, symbols)
# Accuracy is % of correct words


#TODO separate text into... 8 words / line?
#   find out how many characters / line fits in the given text box size
#   Parse text to separate characters into lines without words being out of bounds
#   Finding out words/line is also create indexing for scrolling text

#TODO Highlight one word at a time. Highlight next word after finished

#TODO Typing changes existing text color. Red if incorrect.

#TODO Can go back to previous character?

#TODO After each line is completed, the line is pushed up, new one loaded

#TODO Corrected CPM only counts correct characters. WPM is CPM / 5

# Import Statements
import json
from random import randint
from tkinter import ttk
import tkinter as tk

# Load text json
# Word list found in Corpora - https://github.com/dariusk/corpora/tree/master
with open('../data/common.json', 'r') as pw_file:
    # reading old data
    data = json.load(pw_file)

words = ""

for n in range (0, 100):
    words += (data["commonWords"][randint(0, len(data["commonWords"]) - 1)]) + " "


# setup UI

class TypeSpeedTest:
    def __init__ (self, root):
        self.root = root
        self.setup_ui()
        self.characters_typed = 0


    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10", )
        main_frame.grid(row = 0, sticky="nsew")

        # for resizing
        self.root.grid_rowconfigure(0, weight=1) #for resizing
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)

        #Stats display
        stats_frame = ttk.Frame(main_frame, padding="5")
        stats_frame.grid(row = 0)
        stats_font = ('Calibri', '12')

        #timer
        time_label = ttk.Label(stats_frame,text = "time left", font = stats_font)
        time_label.grid(padx = 5, row = 0, column =0)
        time_counter = ttk.Label(stats_frame, text = "60", font = stats_font, background="white")
        time_counter.grid(padx= 1, row = 0, column = 1)

        #character count
        chara_label = ttk.Label(stats_frame, text="Characters count", font=stats_font)
        chara_label.grid(padx=5, row=0, column=2)

        self.chara_count = ttk.Label(stats_frame, text="0", font=stats_font, background="white")
        self.chara_count.grid(padx=5, row=0, column=3)

        # Text display https://tkdocs.com/tutorial/text.html
        text_font = ('Calibri', '16')
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row = 1, sticky="nsew",padx = 5, pady = 5)
        self.textbox = tk.Text(text_frame,
                          relief = "solid",
                          font = text_font,
                          width = 50,
                          height = 3,
                          wrap=tk.WORD) # Wrap full words
        self.textbox.insert("1.0", words)
        self.textbox.pack(fill="both", expand=True)

        # input box
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, sticky="ew", padx=5, pady=5)
        self.text_var = tk.StringVar(value="Type here!")
        self.typing_box = ttk.Entry(input_frame, textvariable = self.text_var, font = text_font)
        self.typing_box.pack(fill="x", expand = True)
        self.text_var.trace_add("write", self.update_char_count)


    def update_char_count(self, *args):
        char_count = len(self.text_var.get())
        self.chara_count.config(text=char_count)

    def clear_placeholder(self, event):
        if self.typing_box.get() == "Type here!":
            self.typing_box.delete(0, tk.END)

    def typing(self):
        #count number of letters typed
        #count each letter typed
        #check if letter is correct per letter typed.
        #TODO change color of letter typed
        #TODO track character progress
        #TODO track character correctness
        pass

    def next_word(self):
        #TODO Scroll text
        #TODO highlight word
        #use "see" which takes an index.
        #self.text.see(index)
        pass





if __name__ == "__main__":
    root=tk.Tk()
    root.minsize(610, 200)
    root.maxsize(610, 200)
    app=TypeSpeedTest(root)
    app.typing_box.bind("<FocusIn>", app.clear_placeholder)
    root.mainloop()
