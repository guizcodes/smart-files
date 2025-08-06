import os


def get_file():
    file = input("Qual arquivo?: ")
    if ".pdf" in file:
        file = file.replace(".pdf", "")
    elif ".PDF" in file:
        file = file.replace(".PDF", "")
    return f"./documents/pdf/{file}.pdf"
