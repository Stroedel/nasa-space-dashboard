from nasa_client import NasaClient
from utils import clear_screen, print_header, print_menu, pause


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

        if choice == "4":
            print("Programma gestopt.")
            break