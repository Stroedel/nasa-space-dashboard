import tkinter as tk

from nasa_client import NasaClient


client = NasaClient()


root = tk.Tk()
root.title("NASA Space Dashboard")

root.mainloop()