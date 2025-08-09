import os


def get_file():
    file = input("-> Qual arquivo?: ")
    if ".pdf" in file:
        file = file.replace(".pdf", "")
        return f"./documents/pdf/{file}"
        
    elif ".txt" in file:
      return f"./documents/txt/{file}"