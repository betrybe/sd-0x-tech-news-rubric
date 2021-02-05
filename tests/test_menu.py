# flake8: noqa

from unittest.mock import patch
from tech_news.menu import collector_menu, analyzer_menu
from tech_news.collector.scrapper import fetch_content
from pymongo import MongoClient
from decouple import config

DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default="27017")

client = MongoClient(host=DB_HOST, port=int(DB_PORT))
db = client.tech_news

NEW_NOTICE = {
    "url": "https://www.tecmundo.com.br/brincadeira-levadaserio.htm",
    "title": "Yakuza Like a Dragon era beat em up",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "André Luis Dias Custodio",
    "shares_count": 0,
    "comments_count": 0,
    "summary": "Sumario da noticia",
    "sources": ["ResetEra"],
    "categories": ["Plataformas", "PC", "Console"],
}

NEW_NOTICE_ANALYZER = {
    "url": "https://www.tecmundo.com.br/vamos.htm",
    "title": "Vamoscomtudo",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Leonardo",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario 2",
    "sources": ["ResetEra"],
    "categories": ["PC", "Console"],
}

NEW_NOTICE_1 = {
    "url": "https://www.tecmundo.com.br/noticia_1.htm",
    "title": "noticia_1",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_1",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_1",
    "sources": ["Fonte_1"],
    "categories": ["PC_1", "Console_1"],
}

NEW_NOTICE_2 = {
    "url": "https://www.tecmundo.com.br/noticia_2.htm",
    "title": "noticia_2",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_2",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_2",
    "sources": ["Fonte_2"],
    "categories": ["PC_2", "Console_2"],
}

NEW_NOTICE_3 = {
    "url": "https://www.tecmundo.com.br/noticia_3.htm",
    "title": "noticia_3",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_3",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_3",
    "sources": ["Fonte_3"],
    "categories": ["PC_3", "Console_3"],
}

NEW_NOTICE_4 = {
    "url": "https://www.tecmundo.com.br/noticia_4.htm",
    "title": "noticia_4",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_4",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_4",
    "sources": ["Fonte_4"],
    "categories": ["PC_4", "Console_4"],
}

NEW_NOTICE_5 = {
    "url": "https://www.tecmundo.com.br/noticia_5.htm",
    "title": "noticia_5",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_5",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_5",
    "sources": ["Fonte_5"],
    "categories": ["PC_5", "Console_5"],
}

NEW_NOTICE_6 = {
    "url": "https://www.tecmundo.com.br/noticia_6.htm",
    "title": "noticia_6",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_6",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_6",
    "sources": ["Fonte_6"],
    "categories": ["PC_6", "Console_6"],
}


def test_validar_saida_do_console_collector_menu(capsys):
    def fake_input(prompt=""):
        print(prompt, end=" ")
        return ""

    with patch("builtins.input", fake_input):
        collector_menu()
    out, err = capsys.readouterr()
    assert (
        "Selecione uma das opções a seguir:\n 1 - Importar notícias a partir de um arquivo CSV;\n 2 - Exportar notícias para CSV;\n 3 - Raspar notícias online;\n 4 - Sair."
        in out
    )


def test_executar_opcao_sair_collector_menu(capsys):
    with patch("builtins.input") as mocked_input:
        mocked_input.side_effect = ["4", ""]
        collector_menu()
    out, err = capsys.readouterr()
    assert "Encerrando script\n" in out


def test_executar_opcao_invalida_do_collector_menu(capsys):
    with patch("builtins.input") as mocked_input:
        mocked_input.side_effect = ["5", ""]
        collector_menu()
    out, err = capsys.readouterr()
    assert err == "Opção inválida\n"


def test_executar_opcao_importar_collector_menu(capsys):
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.csv_importer"
    ) as mock_importer, patch("tech_news.menu.create_news") as create_news:
        mocked_input.side_effect = ["1", "correct.csv"]
        collector_menu()
        mock_importer.assert_called_once_with("correct.csv")
        create_news.assert_called_once()


def test_executar_opcao_exportar_collector_menu(capsys):
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.csv_exporter"
    ) as mock_exporter:
        mocked_input.side_effect = ["2", "export_correct.csv"]
        collector_menu()
        mock_exporter.assert_called_once_with("export_correct.csv")


def test_executar_opcao_raspar_collector_menu(capsys):
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.scrape"
    ) as scraper, patch("tech_news.menu.create_news") as create_news:
        mocked_input.side_effect = ["3", "1"]
        collector_menu()
        scraper.assert_called_once_with(fetcher=fetch_content, pages=1)
        create_news.assert_called_once()


def test_validar_saida_do_console_analyzer_menu(capsys):
    def fake_input(prompt=""):
        print(prompt, end=" ")
        return "0"

    with patch("builtins.input", fake_input):
        analyzer_menu()
    out, err = capsys.readouterr()
    assert (
        "Selecione uma das opções a seguir:\n 1 - Buscar notícias por título;\n 2 - Buscar notícias por data;\n 3 - Buscar notícias por fonte;\n 4 - Buscar notícias por categoria;\n 5 - Listar top 5 notícias;\n 6 - Listar top 5 categorias;\n 7 - Sair."
        in out
    )


def test_executar_opcao_sair_do_console_analyzer_menu(capsys):
    with patch("builtins.input") as mocked_input:
        mocked_input.side_effect = ["7", ""]
        analyzer_menu()
    out, err = capsys.readouterr()
    assert "Encerrando script\n" in out


def test_executar_opcao_invalida_do_analyzer_menu(capsys):
    with patch("builtins.input") as mocked_input:
        mocked_input.side_effect = ["8", ""]
        analyzer_menu()
    out, err = capsys.readouterr()
    assert err == "Opção inválida\n"


def test_executar_opcao_titulo_do_console_analyzer_menu(capsys):
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE_ANALYZER)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.search_by_title"
    ) as mock_search_by_title:
        mocked_input.side_effect = ["1", "Vamoscomtudo"]
        analyzer_menu()
        mock_search_by_title.assert_called_once_with("Vamoscomtudo")


def test_executar_opcao_data_do_console_analyzer_menu(capsys):
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE_ANALYZER)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.search_by_date"
    ) as mock_search_by_date:
        mocked_input.side_effect = ["2", "2020-11-23"]
        analyzer_menu()
        mock_search_by_date.assert_called_once_with("2020-11-23")


def test_executar_opcao_fonte_do_console_analyzer_menu(capsys):
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE_ANALYZER)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.search_by_source"
    ) as mock_search_by_source:
        mocked_input.side_effect = ["3", "ResetEra"]
        analyzer_menu()
        mock_search_by_source.assert_called_once_with("ResetEra")


def test_executar_opcao_categoria_do_console_analyzer_menu(capsys):
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE_ANALYZER)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.search_by_category"
    ) as mock_search_by_category:
        mocked_input.side_effect = ["4", "Console"]
        analyzer_menu()
        mock_search_by_category.assert_called_once_with("Console")


def test_executar_opcao_top5_noticias_do_console_analyzer_menu(capsys):
    db.news.delete_many({})
    db.news.insert_many(
        [
            NEW_NOTICE_1,
            NEW_NOTICE_2,
            NEW_NOTICE_3,
            NEW_NOTICE_4,
            NEW_NOTICE_5,
            NEW_NOTICE_6,
        ]
    )
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.top_5_news"
    ) as mock_top_5_news:
        mocked_input.side_effect = ["5", ""]
        analyzer_menu()
        mock_top_5_news.assert_called_once()


def test_executar_opcao_top5_categorias_do_console_analyzer_menu(capsys):
    db.news.delete_many({})
    db.news.insert_many(
        [
            NEW_NOTICE_1,
            NEW_NOTICE_2,
            NEW_NOTICE_3,
            NEW_NOTICE_4,
            NEW_NOTICE_5,
            NEW_NOTICE_6,
        ]
    )
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.top_5_categories"
    ) as mock_top_5_categories:
        mocked_input.side_effect = ["6", ""]
        analyzer_menu()
        mock_top_5_categories.assert_called_once()
