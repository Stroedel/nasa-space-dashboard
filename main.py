from datetime import date

from nasa_client import NasaClient
from utils import clear_screen, print_header, print_menu, pause, loading


def show_apod(client):
    loading("Foto van de dag ophalen")
    data = client.get_apod()

    if not data:
        return

    print("\nAstronomy Picture of the Day")
    print("-" * 45)
    print(f"Titel: {data.get('title')}")
    print(f"Datum: {data.get('date')}")
    print(f"Type: {data.get('media_type')}")
    print(f"URL: {data.get('url')}")
    print(f"\nUitleg:\n{data.get('explanation')}")


def show_image_search(client):
    query = input("Waar wil je NASA afbeeldingen van zoeken? ")

    if query == "":
        print("Je moet een zoekterm ingeven.")
        return

    loading("Afbeeldingen zoeken")
    data = client.search_images(query)

    if not data:
        return

    items = data.get("collection", {}).get("items", [])

    if not items:
        print("Geen afbeeldingen gevonden.")
        return

    print(f"\nGevonden resultaten voor '{query}':")

    for item in items[:5]:
        info = item.get("data", [{}])[0]
        links = item.get("links", [{}])

        print("-" * 45)
        print(f"Titel: {info.get('title')}")
        print(f"Datum: {info.get('date_created')}")
        print(
            f"Beschrijving: "
            f"{info.get('description', 'Geen beschrijving')[:150]}..."
        )

        if links:
            print(f"Afbeelding: {links[0].get('href')}")
        else:
            print("Afbeelding: geen link beschikbaar")


def show_asteroids(client):
    chosen_date = input("Geef datum (YYYY-MM-DD) of Enter voor vandaag: ")

    if chosen_date == "":
        chosen_date = date.today().isoformat()

    loading("Asteroïden ophalen")
    data = client.get_asteroids(chosen_date)

    if not data:
        return

    objects = data.get("near_earth_objects", {}).get(chosen_date, [])

    if not objects:
        print("Geen asteroïden gevonden.")
        return

    print(f"\nAsteroïden op {chosen_date}: {len(objects)}")

    for asteroid in objects[:5]:
        diameter = asteroid["estimated_diameter"]["meters"]
        approach = asteroid["close_approach_data"][0]

        print("-" * 45)
        print(f"Naam: {asteroid['name']}")
        print(f"Gevaarlijk: {asteroid['is_potentially_hazardous_asteroid']}")
        print(
            f"Diameter: {diameter['estimated_diameter_min']:.2f} - "
            f"{diameter['estimated_diameter_max']:.2f} meter"
        )
        print(f"Afstand: {approach['miss_distance']['kilometers']} km")


def main():
    client = NasaClient()

    if not client.api_key:
        print("Geen NASA API key gevonden.")
        print("Maak een .env bestand met NASA_API_KEY=je_key")
        return

    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("Kies een optie: ")

        if choice == "1":
            show_apod(client)
            pause()

        elif choice == "2":
            show_image_search(client)
            pause()

        elif choice == "3":
            show_asteroids(client)
            pause()

        elif choice == "4":
            print("Programma gestopt.")
            break

        else:
            print("Ongeldige keuze.")
            pause()


if __name__ == "__main__":
    main()