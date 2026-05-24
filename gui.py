import tkinter as tk

from nasa_client import NasaClient


client = NasaClient()

current_images = []
current_index = 0


root = tk.Tk()
root.title("NASA Space Dashboard")

root.mainloop()