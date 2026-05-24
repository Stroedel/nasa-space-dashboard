import tkinter as tk
from urllib.request import urlopen
from io import BytesIO

from PIL import Image, ImageTk

from nasa_client import NasaClient


client = NasaClient()

current_images = []
current_index = 0


def clear_result():
    result_text.delete("1.0", tk.END)


def reset_image_area():
    image_label.pack(pady=10)
    result_text.config(height=8)


def show_image_from_url(url):
    try:
        reset_image_area()

        image_bytes = urlopen(url).read()
        data_stream = BytesIO(image_bytes)

        pil_image = Image.open(data_stream)
        pil_image.thumbnail((480, 360))

        tk_image = ImageTk.PhotoImage(pil_image)

        image_label.config(image=tk_image)
        image_label.image = tk_image

    except Exception:
        image_label.config(image="")
        image_label.image = None


def display_current_image():
    if not current_images:
        return

    image_url = current_images[current_index]
    show_image_from_url(image_url)

    clear_result()

    result_text.insert(
        tk.END,
        f"Afbeelding {current_index + 1} van {len(current_images)}\n"
    )

    result_text.insert(tk.END, "-" * 60 + "\n")
    result_text.insert(tk.END, f"URL: {image_url}\n")


root = tk.Tk()
root.title("NASA Space Dashboard")

root.mainloop()