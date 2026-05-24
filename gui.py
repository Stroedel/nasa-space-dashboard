import tkinter as tk

from nasa_client import NasaClient


client = NasaClient()

current_images = []
current_index = 0


def clear_result():
    result_text.delete("1.0", tk.END)


def reset_image_area():
    image_label.pack(pady=10)
    result_text.config(height=8)


root = tk.Tk()
root.title("NASA Space Dashboard")

root.mainloop()