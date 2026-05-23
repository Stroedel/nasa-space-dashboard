import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nDruk op Enter om verder te gaan...")

def print_header():
    print("=" * 45)
    print("        NASA SPACE DASHBOARD 🚀")
    print("=" * 45)

def print_menu():
    print("1. Astronomy Picture of the Day")
    print("2. Mars Rover foto's zoeken")
    print("3. Asteroïden bekijken")
    print("4. Stoppen")
    print("-" * 45)