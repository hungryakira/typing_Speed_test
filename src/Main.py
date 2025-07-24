# Typing speed is defined as "words" per minute. "word" is defined as 5 characters (including spaces, symbols)
# Corrected CPM only counts correct characters. WPM is CPM / 5

# Import Statements
import json
from random import randint
from tkinter import ttk
import tkinter as tk

# Load text json
# Word list from Corpora - https://github.com/dariusk/corpora/tree/master

words = ""
with open('../data/common.json', 'r') as pw_file:
    data = json.load(pw_file)

for n in range (0, 150):
    words += (data["commonWords"][randint(0, len(data["commonWords"]) - 1)]) + " "

# Constants
STATS_FONT = ('Calibri', '12')
TEXT_FONT = ('Calibri', '16')


class TypeSpeedTest:
    def __init__ (self, root):
        self.root = root
        self.characters_typed = 0
        self.correct_char_count = 0
        self.time_length = 60
        self.timer = ""

        self.setup_ui()

    def setup_ui(self):
        """Function to set up UI"""
        main_frame = ttk.Frame(self.root, padding="10", )
        main_frame.grid(row = 0, sticky="nsew")

        # Stats displays
        stats_frame = ttk.Frame(main_frame, padding="5")
        stats_frame.grid(row = 0)

        # Timer
        time_label = ttk.Label(stats_frame, text = "Time", font = STATS_FONT)
        time_label.grid(padx = 5, row = 0, column =0)
        self.time_counter = ttk.Label(stats_frame, text = self.time_length, font = STATS_FONT, background="white")
        self.time_counter.grid(padx= 1, row = 0, column = 1)

        #Character count
        chara_label = ttk.Label(stats_frame, text="Characters count", font=STATS_FONT)
        chara_label.grid(padx=5, row=0, column=2)

        self.chara_count_label = ttk.Label(stats_frame, text="0", font=STATS_FONT, background="white")
        self.chara_count_label.grid(padx=5, row=0, column=3)

        #Correct character count
        wpm_label = ttk.Label(stats_frame, text="Words per miunte", font=STATS_FONT)
        wpm_label.grid(padx=5, row=0, column=4)

        self.wpm_result = ttk.Label(stats_frame, text="?", font=STATS_FONT, background="white")
        self.wpm_result.grid(padx=5, row=0, column=5)

        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row = 1, sticky="nsew",padx = 5, pady = 5)
        self.textbox = tk.Text(text_frame,
                               relief = "solid",
                               font = TEXT_FONT,
                               width = 50,
                               height = 5,
                               wrap=tk.WORD) # Wrap full words
        self.textbox.insert("1.0", words)
        self.textbox.pack(fill="both", expand=True)

        # input box
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, sticky="ew", padx=5, pady=5)
        self.text_var = tk.StringVar(value="Click here to start test")
        self.typing_box = ttk.Entry(input_frame, textvariable = self.text_var, font = TEXT_FONT)
        self.typing_box.pack(fill="x", expand = True)
        self.text_var.trace_add("write", self.typing)

    def typing(self, *args):
        """Function to handle character count and scrolling the text box based on number of characters typed"""

        current_entry = self.text_var.get()
        self.characters_typed = len(current_entry)
        self.chara_count_label.config(text=self.characters_typed)
        # Keep roughly one line ahead current typing progress in Textbox
        self.textbox.see(f"1.{self.characters_typed}+62 chars")

    def match_text(self):
        """Check Textbox and typing_box for matching blocks of texts and returns total number of matching characters."""
        import difflib

        matcher = difflib.SequenceMatcher(None, words, self.typing_box.get(), autojunk=False)
        match_results = matcher.get_matching_blocks()
        # matcher returns a tuple: (text1 index, text2 index, length of match)
        total_matches = 0

        for i, j, n in match_results:
            if n > 0:  # Skip the last row which is always (len(s1), len(s2), 0)
                total_matches += n

        #Calculate words per minute which is (correct characters/5)
        word_per_min = int(total_matches/5)
        self.wpm_result.config(text=word_per_min)

    def start_counter(self,event):
        """  Upon click on entry box, this function deletes default text and trigger count_down"""
        global first_focus
        if not first_focus: # only trigger when typing box clicked the first time
            self.count_down(self.time_length)

            if self.typing_box.get() == "Click here to start test":
                self.typing_box.delete(0, tk.END)
            first_focus = True

    def count_down(self,count):
        """countdown mechanism starts when textbox is clicked.
        when timer finishes, trigger match_text, disable textbox"""

        if count != 0:
            self.time_counter.config(text=count)
            self.timer = root.after(1000, self.count_down, count-1)
        else:
            root.after_cancel(self.timer)
            self.typing_box.config(state="disabled")
            self.time_counter.config(text="0")
            self.match_text()


if __name__ == "__main__":
    root=tk.Tk()
    root.minsize(585, 240)
    root.maxsize(585, 240)
    first_focus = False
    app=TypeSpeedTest(root)
    app.typing_box.bind("<FocusIn>", app.start_counter)
    root.mainloop()
