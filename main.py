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

        elif choice == "4":
            print("Programma gestopt.")
            break

        else:
            print("Ongeldige keuze.")
            pause()


if __name__ == "__main__":
    main()