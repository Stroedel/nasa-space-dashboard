import tkinter as tk
from tkinter import messagebox
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


def show_apod():
    chosen_date = apod_date_entry.get().strip()

    if chosen_date == "":
        data = client.get_apod()
    else:
        data = client.get_apod(chosen_date)

    if not data:
        messagebox.showerror(
            "Fout",
            "Kon APOD data niet ophalen."
        )
        return

    clear_result()

    image_url = data.get("url")

    result_text.insert(
        tk.END,
        "Astronomy Picture of the Day\n"
    )

    result_text.insert(tk.END, "-" * 60 + "\n")

    result_text.insert(
        tk.END,
        f"Titel: {data.get('title')}\n"
    )

    result_text.insert(
        tk.END,
        f"Datum: {data.get('date')}\n"
    )

    result_text.insert(
        tk.END,
        f"Type: {data.get('media_type')}\n"
    )

    result_text.insert(
        tk.END,
        f"URL: {image_url}\n\n"
    )

    result_text.insert(
        tk.END,
        data.get("explanation")
    )

    if data.get("media_type") == "image":
        show_image_from_url(image_url)


def search_images():
    global current_images
    global current_index

    query = search_entry.get().strip()
    year = image_year_entry.get().strip()

    if query == "":
        messagebox.showwarning(
            "Leeg veld",
            "Geef eerst een zoekterm in."
        )
        return

    if year == "":
        data = client.search_images(query)
    else:
        data = client.search_images(query, year)

    if not data:
        messagebox.showerror(
            "Fout",
            "Kon afbeeldingen niet ophalen."
        )
        return

    items = data.get(
        "collection",
        {}
    ).get(
        "items",
        []
    )

    clear_result()

    current_images = []
    current_index = 0

    for item in items[:20]:
        links = item.get("links", [])

        if links:
            image_url = links[0].get("href")

            if image_url:
                current_images.append(image_url)

    if not current_images:
        result_text.insert(
            tk.END,
            "Geen bruikbare afbeeldingen gevonden."
        )
        return

    display_current_image()


root = tk.Tk()
root.title("NASA Space Dashboard")

root.mainloop()