import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nDruk op Enter om verder te gaan...")