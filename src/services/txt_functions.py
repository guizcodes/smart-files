from utils import clear
import os


def show_txt_files():
    print("📁-----Seus arquivos-----📁\n".center(56))
    try:
        for file in os.listdir("./documents/txt"):
            if file.endswith(".txt"):
                print(f"📙 - {file}".center(56))
        print("=" * 58)
    except Exception:
        print("R: Falha ao carregar arquivos...")


from utils import clear
import os


def show_txt_files():
    print("📁-----Seus arquivos-----📁\n".center(56))
    try:
        for file in os.listdir("./documents/txt"):
            if file.endswith(".txt"):
                print(f"📙 - {file}".center(56))
        print("=" * 58)
    except Exception:
        print("R: Falha ao carregar arquivos...")


def search_word(file):
    word = input("-> Qual palavra quer procurar?: ").strip().lower()

    try:
        with open(file, "r", encoding="utf-8") as opened_file:
            texts = []
            count = 0
            found = False
            for line in opened_file:
                line_lower = line.lower()
                words = line_lower.split()
                if word in words:
                    texts.append(line.strip())
                    count += words.count(word)
                    found = True

        if found:
            print(
                f"\nR: A palavra '{word}' foi encontrada {count} vezes e apareceu nos seguintes trechos: \n"
            )
            for text in texts:
                print(f">>>\n{text}... \n<<< \n\n")
        else:
            print("R: A palavra não foi encontrada.")
        print("=" * 58)

    except FileNotFoundError:
        print("R: Arquivo não encontrado na pasta.")
    except TypeError:
        print("R: Erro. (cheque seu arquivo)")
