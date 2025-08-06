from PyPDF2 import PdfReader, PdfMerger
from utils import clear
import os
import requests
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
config_path = os.path.join(BASE_DIR, "config.json")

with open(config_path, "r") as c:
    config = json.load(c)

user_api = config["API"]
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {user_api}"}


def show_pdf_files():
    print("📁-----Seus arquivos-----📁\n".center(50))
    try:
        for file in os.listdir("./documents/pdf"):
            if file.endswith(".pdf"):
                print(f"📙 - {file}".center(50))
        print("=" * 54)
    except Exception:
        print("Falha ao carregar arquivos...")


def save_txt(content):
    title = str(input("Titulo para o seu arquivo txt: "))
    try:
        path = f"./documents/txt/{title}.txt"
        with open(path, "w") as f:
            f.write(content)
        print(f"Pronto! o arquivo {title}.txt foi salvo.")
    except Exception as e:
        print(f"Falha ao salvar {title}.txt")


def extract_pdf_to_txt():
    option = input(
        """
      [1] Conversão única
      [2] Conversão multipla
      Opção: """
    )
    if option == "1":
        filename = input("Qual arquivo?: ")
        file_directory = f"./documents/pdf/{filename}.pdf"
        if file_directory.endswith(".pdf"):
            try:
                reader = PdfReader(file_directory)
                content = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"
                save_txt(content)
            except Exception as e:
                print("Falha ao extrair texto. (cheque seu arquivo)")
    elif option == "2":
        number_of_files = input("Quantos arquivos?: ")
        if number_of_files.isnumeric():
            try:
                counter = 0
                files = []
                number_of_files = int(number_of_files)
                for counter in range(0, number_of_files):
                    file = str(input(f"Arquivo {counter + 1}: "))
                    file_directory = f"./documents/pdf/{file}.pdf"
                    if file_directory.endswith(".pdf"):
                        files.append(file_directory)
                    else:
                        print("Esse arquivo não é um PDF!")
                for file in files:
                    reader = PdfReader(file)
                    content = ""
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            content += text + "\n"
                    save_txt(content)
                if counter >= 20:
                    print("Talvez possa demorar um pouco para fazer o resumo. Aguarde!")
            except Exception:
                print("Falha ao extrair os textos.")
        else:
            print("Opção Inválida.")
    else:
        print("Opção Inválida.")


def split_text(text, max_words=300):
    words = text.split()
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i : i + max_words])
        if chunk.strip():
            yield chunk


def summarize_text(content):
    try:
        payload = {"inputs": content}
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result[0]["summary_text"]
        else:
            if response.status_code == 400:
                print(f"...")
                return None
    except Exception:
        print("Erro desconhecido.")


def summarize_chunks(content):
    try:
        parts = []
        for chunk in split_text(content):
            summary = summarize_text(chunk)
            if summary:
                parts.append(summary)

        if not parts:
            print("Nenhuma parte pôde ser resumida.")
            return ""

        full_summary = " ".join(parts)
        final_summary = summarize_text(full_summary)
        if final_summary:
            return final_summary
        else:
            print("Erro ao resumir a parte final. O resumo está parcialmente completo.")
            return full_summary
    except Exception as e:
        print("Erro ao resumir seu arquivo.")
        return ""


def manage_summary(file):
    if file.endswith(".pdf"):
        try:
            reader = PdfReader(file)
            content = ""
            counter = 1
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"
                print(f"Página {counter} carregada.", end="\r")
                counter += 1
            option = input(
                """
            [1] Visualizar o resumo agora
            [2] Exportar o resumo para um arquivo txt
            [3] Voltar sem visualizar
            Option: """
            )
            if option.isnumeric():
                match option:
                    case "1":
                        summary = summarize_chunks(content)
                        print("\nResumo:\n", summary)
                    case "2":
                        save_txt(summarize_chunks(content))
                    case "3":
                        clear()
                        return

        except Exception as e:
            print(f"Erro: {e}")
            return ""
    else:
        print("Esse arquivo não é um PDF!")
        return ""


def merge_pdfs():
    merger = PdfMerger()
    try:
        num = int(input("Quantos arquivos?: "))
        c = 0
        pdfs = []
        while c < num:
            filename = input(f"arquivo {c + 1}: ")
            if ".pdf" in filename:
                filename = filename.replace(".pdf", "")
            file = f"./documents/pdf/{filename}.pdf"
            pdfs.append(file)
            c += 1

        for pdf_file in pdfs:
            merger.append(pdf_file)

        pdf_merger_name = input("Nome para o novo PDF: ")
        if ".pdf" in pdf_merger_name:
            pdf_merger_name = pdf_merger_name.replace(".pdf", "")

        merger.write(f"./documents/pdf/{pdf_merger_name}.pdf")
        merger.close()
        print(f"Salvo em smart-files/src/documents/pdf/{pdf_merger_name}.pdf")

    except Exception as e:
        print(f"Erro: {e}")
