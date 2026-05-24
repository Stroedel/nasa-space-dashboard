import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta
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
    result_text.insert(tk.END, f"Afbeelding {current_index + 1} van {len(current_images)}\n")
    result_text.insert(tk.END, "-" * 60 + "\n")
    result_text.insert(tk.END, f"URL: {image_url}\n")


def show_apod():
    chosen_date = apod_date_entry.get().strip()

    if chosen_date == "":
        data = client.get_apod()
    else:
        data = client.get_apod(chosen_date)

    if not data:
        messagebox.showerror("Fout", "Kon APOD data niet ophalen.")
        return

    clear_result()

    image_url = data.get("url")

    result_text.insert(tk.END, "Astronomy Picture of the Day\n")
    result_text.insert(tk.END, "-" * 60 + "\n")
    result_text.insert(tk.END, f"Titel: {data.get('title')}\n")
    result_text.insert(tk.END, f"Datum: {data.get('date')}\n")
    result_text.insert(tk.END, f"Type: {data.get('media_type')}\n")
    result_text.insert(tk.END, f"URL: {image_url}\n\n")
    result_text.insert(tk.END, data.get("explanation"))

    if data.get("media_type") == "image":
        show_image_from_url(image_url)


def search_images():
    global current_images
    global current_index

    query = search_entry.get().strip()
    year = image_year_entry.get().strip()

    if query == "":
        messagebox.showwarning("Leeg veld", "Geef eerst een zoekterm in.")
        return

    if year == "":
        data = client.search_images(query)
    else:
        data = client.search_images(query, year)

    if not data:
        messagebox.showerror("Fout", "Kon afbeeldingen niet ophalen.")
        return

    items = data.get("collection", {}).get("items", [])

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
        result_text.insert(tk.END, "Geen bruikbare afbeeldingen gevonden.")
        return

    display_current_image()


def next_image():
    global current_index

    if current_images:
        current_index = (current_index + 1) % len(current_images)
        display_current_image()


def previous_image():
    global current_index

    if current_images:
        current_index = (current_index - 1) % len(current_images)
        display_current_image()


def show_asteroids_week():
    start = date.today()
    end = start + timedelta(days=6)

    start_date = start.isoformat()
    end_date = end.isoformat()

    clear_result()

    image_label.pack_forget()
    result_text.config(height=24)

    result_text.insert(
        tk.END,
        f"Bezig met asteroïden ophalen van {start_date} tot {end_date}...\n\n"
    )

    root.update()

    data = client.get_asteroids_week(start_date, end_date)

    clear_result()

    if not data:
        result_text.insert(tk.END, "Geen data ontvangen van NASA.\n")
        return

    near_objects = data.get("near_earth_objects", {})
    total = sum(len(objects) for objects in near_objects.values())

    result_text.insert(
        tk.END,
        f"Asteroïden van {start_date} tot {end_date}: {total}\n\n"
    )

    for day, objects in near_objects.items():
        result_text.insert(tk.END, f"Datum: {day}\n")
        result_text.insert(tk.END, "-" * 60 + "\n")

        for asteroid in objects[:3]:
            diameter = asteroid["estimated_diameter"]["meters"]
            approach_data = asteroid.get("close_approach_data", [])

            result_text.insert(tk.END, f"Naam: {asteroid['name']}\n")
            result_text.insert(
                tk.END,
                f"Gevaarlijk: {asteroid['is_potentially_hazardous_asteroid']}\n"
            )
            result_text.insert(
                tk.END,
                f"Diameter: {diameter['estimated_diameter_min']:.2f} - "
                f"{diameter['estimated_diameter_max']:.2f} meter\n"
            )

            if approach_data:
                approach = approach_data[0]
                result_text.insert(
                    tk.END,
                    f"Afstand: {approach['miss_distance']['kilometers']} km\n"
                )

            result_text.insert(tk.END, "\n")


root = tk.Tk()
root.title("NASA Space Dashboard")
root.geometry("1050x850")
root.resizable(False, False)
root.configure(bg="#0b1020")

title_label = tk.Label(
    root,
    text="NASA Space Dashboard 🚀",
    font=("Arial", 26, "bold"),
    bg="#0b1020",
    fg="white"
)
title_label.pack(pady=15)

subtitle_label = tk.Label(
    root,
    text="APOD bekijken • NASA afbeeldingen zoeken • Asteroïden deze week",
    font=("Arial", 11),
    bg="#0b1020",
    fg="#b8c1ec"
)
subtitle_label.pack(pady=2)

control_frame = tk.Frame(root, bg="#151b2e", padx=20, pady=15)
control_frame.pack(pady=15)

apod_label = tk.Label(
    control_frame,
    text="APOD datum (YYYY-MM-DD, leeg = vandaag)",
    bg="#151b2e",
    fg="white"
)
apod_label.grid(row=0, column=0, padx=8, pady=4)

apod_date_entry = tk.Entry(control_frame, width=28)
apod_date_entry.grid(row=1, column=0, padx=8, pady=4)

apod_button = tk.Button(
    control_frame,
    text="APOD tonen",
    command=show_apod,
    width=24,
    bg="#4f46e5",
    fg="white"
)
apod_button.grid(row=2, column=0, padx=8, pady=8)

search_label = tk.Label(
    control_frame,
    text="Zoekterm afbeelding",
    bg="#151b2e",
    fg="white"
)
search_label.grid(row=0, column=1, padx=8, pady=4)

search_entry = tk.Entry(control_frame, width=28)
search_entry.grid(row=1, column=1, padx=8, pady=4)
search_entry.insert(0, "moon")

year_label = tk.Label(
    control_frame,
    text="Jaar afbeelding",
    bg="#151b2e",
    fg="white"
)

year_label.grid(
    row=0,
    column=2,
    padx=8,
    pady=4
)

image_year_entry = tk.Entry(
    control_frame,
    width=20
)

image_year_entry.grid(
    row=1,
    column=2,
    padx=8,
    pady=4
)

image_year_entry.insert(0, "1969")

search_button = tk.Button(
    control_frame,
    text="NASA afbeeldingen zoeken",
    command=search_images,
    width=24,
    bg="#2563eb",
    fg="white"
)

search_button.grid(
    row=2,
    column=1,
    columnspan=2,
    padx=8,
    pady=8
)

root.mainloop()