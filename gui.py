import tkinter as tk

from nasa_client import NasaClient


client = NasaClient()

current_images = []
current_index = 0


def clear_result():
    result_text.delete("1.0", tk.END)


root = tk.Tk()
root.title("NASA Space Dashboard")

root.mainloop()