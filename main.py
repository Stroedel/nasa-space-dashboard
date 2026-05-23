from datetime import date

from nasa_client import NasaClient
from utils import clear_screen, print_header, print_menu, pause


def show_apod(client):
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


def show_mars_photos(client):
    print("\nBeschikbare rovers:")
    print("1. curiosity")
    print("2. opportunity")
    print("3. spirit")
    print("4. perseverance")

    rovers = {
        "1": "curiosity",
        "2": "opportunity",
        "3": "spirit",
        "4": "perseverance"
    }

    choice = input("Kies rover: ")
    rover = rovers.get(choice)

    if not rover:
        print("Ongeldige rover.")
        return

    chosen_date = input("Geef datum (YYYY-MM-DD): ")
    data = client.get_mars_photos(rover, chosen_date)

    if not data:
        return

    photos = data.get("photos", [])

    if not photos:
        print("Geen foto's gevonden.")
        return

    print(f"\nAantal gevonden foto's: {len(photos)}")

    for photo in photos[:5]:
        print("-" * 45)
        print(f"Rover: {photo['rover']['name']}")
        print(f"Camera: {photo['camera']['full_name']}")
        print(f"Sol: {photo['sol']}")
        print(f"Foto: {photo['img_src']}")


def show_asteroids(client):
    chosen_date = input("Geef datum (YYYY-MM-DD) of Enter voor vandaag: ")

    if chosen_date == "":
        chosen_date = date.today().isoformat()

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
            show_mars_photos(client)
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