import os
from .menus import *
from utils import *
from services import *


def run():
    while True:
        initial_menu()
        main_menu_option = input("Opção: ")
        menu_checked_option = it_is_number(main_menu_option)

        match menu_checked_option:
            case "1":
                try:
                    clear()
                    show_pdf_files()
                    pdf_options()
                    pdf_user_option = input("Opção: ")
                    selected_function = it_is_number(pdf_user_option)

                    functions = {
                        "1": lambda: manage_summary(get_file()),
                        "2": extract_pdf_to_txt,
                        "3": merge_pdfs,
                        "4": clear,
                    }

                    if selected_function in functions:
                        functions[selected_function]()
                    else:
                        print("Opção Inválida.")
                        clear()
                except Exception as e:
                    print(f"Erro. [{e}]")

            case "2":
                clear()
                break

            case _:
                print("Opção Inválida.")
                clear()
