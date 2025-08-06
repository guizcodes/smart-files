import os


def clear():
    return os.system("cls" if os.name == "nt" else "clear")
