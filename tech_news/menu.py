import sys
from tech_news.collector.importer import csv_importer
from tech_news.collector.exporter import csv_exporter
from tech_news.collector.scrapper import scrape, fetch_content
from tech_news.analyzer.ratings import top_5_categories, top_5_news
from tech_news.analyzer.search_engine import (
    search_by_category,
    search_by_date,
    search_by_source,
    search_by_title,
)


def show_menu():
    menu_text = """Selecione uma das opções a seguir:
 1 - Importar notícias a partir de um arquivo CSV;
 2 - Exportar notícias para CSV;
 3 - Raspar notícias online;
 4 - Sair."""
    input_answer = input(menu_text)
    return input_answer


def show_submenu(option):
    submenu_options = [
        "Digite o nome do arquivo CSV a ser importado:",
        "Digite o nome do arquivo CSV a ser exportado:",
        "Digite a quantidade de páginas a serem raspadas:",
    ]
    input_answer = input(submenu_options[option])
    return input_answer


def collector_menu():
    create_news()
    functions = [
        lambda csv_path: csv_importer(csv_path),
        lambda csv_path: csv_exporter(csv_path),
        lambda number_of_pages: (
            scrape(fetcher=fetch_content, pages=int(number_of_pages))
        ),
    ]
    answer = show_menu()
    if answer:
        answer = int(answer)

    if answer in range(1, 4):
        submenu_response = show_submenu(option=answer - 1)
        action_response = functions[answer - 1](submenu_response)
        print(action_response)
    else:
        print("Opção inválida", file=sys.stderr)
    print("Encerrando script\n")


def show_analyzer_menu():
    analyzer_menu_text = """Selecione uma das opções a seguir:
 1 - Buscar notícias por título;
 2 - Buscar notícias por data;
 3 - Buscar notícias por fonte;
 4 - Buscar notícias por categoria;
 5 - Listar top 5 notícias;
 6 - Listar top 5 categorias;
 7 - Sair."""
    answer = input(analyzer_menu_text)
    return answer


def analyzer_menu():
    seconde_question = [
        "Digite o título:",
        "Digite a data no formato aaaa-mm-dd:",
        "Digite a fonte:",
        "Digite a categoria:",
        top_5_news(),
        top_5_categories(),
    ]

    functions = [
        lambda search: search_by_title(search),
        lambda search: search_by_date(search),
        lambda search: search_by_source(search),
        lambda search: search_by_category(search),
    ]

    answer = show_analyzer_menu()
    if answer:
        answer = int(answer)
        option = int(answer) - 1

    if answer in range(1, 7):
        print("seocnd" + str(option))
        print(seconde_question[option])
        if answer in range(1, 5):
            query_param = input()
            query_result = functions[option](query_param)
            print(query_result)
    else:
        print("Opção inválida", file=sys.stderr)
    print("Encerrando script\n")


def create_news():
    with open("correct.csv"):
        pass
    pass
