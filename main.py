from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
MAIN_LANGUAGE = "English"
# ------------------------ LOAD DATA -------------------------
current_card = {}
study_language = ""
words_dict = {}

language_code = input("Please enter language code: ")

if language_code == "ko":
    study_language = "Korean"
else:
    study_language = "Portuguese"

word_data = input("Please enter word data: ")

file_path = f"data/{language_code}_{word_data}_words_to_learn.csv"
original_file_path = f"data/{language_code}_{word_data}.csv"

try:
    data = pandas.read_csv(file_path)
except FileNotFoundError:
    original_data = pandas.read_csv(original_file_path)
    words_dict = original_data.to_dict(orient="records")
else:
    words_dict = data.to_dict(orient="records")


def flip_card():
    canvas.itemconfig(card_title, text=MAIN_LANGUAGE, fill="white")
    canvas.itemconfig(card_word, text=current_card[MAIN_LANGUAGE], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)


# ------------------------ GET NEW WORD -------------------------
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_dict)
    canvas.itemconfig(card_title, text=study_language, fill="black")
    canvas.itemconfig(card_word, text=current_card[study_language], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, flip_card)


# ------------------------ REMOVE KNOWN WORD FROM DATA -------------------------
def known_card():
    words_dict.remove(current_card)
    words_to_learn_data = pandas.DataFrame(words_dict)
    words_to_learn_data.to_csv(f"data/{language_code}_{word_data}_words_to_learn.csv", index=False)
    next_card()


# ------------------------ WINDOW SETUP -------------------------
window = Tk()
window.title("Flash card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)
# ------------------------ IMAGES -------------------------
correct_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")

# ------------------------ BUTTONS -------------------------
correct_button = Button(image=correct_image, highlightthickness=0, command=known_card)
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)

# ------------------------ CANVAS -------------------------
canvas = Canvas(width=800, height=526)
card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

# ------------------------ GRID -------------------------
canvas.grid(row=0, column=0, columnspan=2)
wrong_button.grid(row=1, column=0, )
correct_button.grid(row=1, column=1)

next_card()

window.mainloop()
