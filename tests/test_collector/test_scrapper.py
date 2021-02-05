# flake8: noqa

from tech_news.collector.scrapper import fetch_content, scrape

from unittest.mock import patch


def test_sera_validado_que_fetch_retorna_requisicao_com_sucesso():
    expected = (
        "Aprenda a programar com uma formação de alta"
        " qualidade e só comece a pagar quando conseguir um bom"
        " trabalho."
    )
    assert expected in fetch_content("https://app.betrybe.com/")


def test_sera_validado_fetch_com_tempo_de_resposta_maior_que_3():
    assert "" == fetch_content("https://httpbin.org/delay/10")


def test_sera_validado_resposta_fetch_com_status_diferente_de_200():
    assert "" == fetch_content("https://httpbin.org/status/404")


def test_validar_tempo_sleep_do_fecth():
    with patch("tech_news.collector.scrapper.sleep") as mocked_sleep:
        fetch_content("https://app.betrybe.com/")
        mocked_sleep.assert_called_with(0.5)


def test_validar_scrape_default_retorna_a_primeira_pagina():
    def fetcher(url, timeout=3, delay=0.5):
        if url.startswith("https://www.tecmundo.com.br/novidades"):
            file_name = "tests/test_collector/index.html"
        else:
            file_name = "tests/test_collector/notice.html"
        with open(file_name, encoding="utf-8") as file:
            return file.read()

    assert len(scrape(fetcher=fetcher)) == 20
    notices = scrape(fetcher=fetcher)
    assert notices[0] == {
        "url": "https://www.tecmundo.com.br/voxel/204798-xbox-series-x-lista-jogos-otimizados-divulgada-mes.htm",
        "title": "Nova York vai proibir venda de carros à gasolina em 2035",
        "timestamp": "2020-10-05T16:30:01",
        "writer": " Adriano Camacho Vieira Júnior ",
        "shares_count": 0,
        "comments_count": 0,
        "summary": "No último dia 25 de setembro, o estado de Nova York, nos Estados Unidos, apresentou uma lei que proibirá a venda de novos carros movidos a combustão em 2035. O anúncio foi feito por Pete Harckham, senador norte-americano criador da proposta, e também determina que a venda de caminhões movidos pela queima de combustíveis fósseis seja proibida em 2045.",
        "sources": [" Electrek ", " Senado de Nova York "],
        "categories": [
            " Mobilidade Urbana/Smart Cities ",
            " Elétricos ",
            " Carro ",
        ],
    }


def test_validar_scrape_retorna_noticias_de_N_paginas():
    def fetcher(url, timeout=3, delay=0.5):
        if url.startswith("https://www.tecmundo.com.br/novidades"):
            file_name = "tests/test_collector/index.html"
        else:
            file_name = "tests/test_collector/notice.html"
        with open(file_name, encoding="utf-8") as file:
            return file.read()

    assert len(scrape(fetcher=fetcher, pages=2)) == 40


def test_validar_formato_da_lista():
    def fetcher(url, timeout=3, delay=0.5):
        if url.startswith("https://www.tecmundo.com.br/novidades"):
            file_name = "tests/test_collector/index.html"
        else:
            file_name = "tests/test_collector/notice.html"
        with open(file_name, encoding="utf-8") as file:
            return file.read()

    notices = scrape(fetcher=fetcher)
    assert type(notices[0]["url"]) == str
    assert type(notices[0]["title"]) == str
    assert type(notices[0]["timestamp"]) == str
    assert type(notices[0]["writer"]) == str
    assert type(notices[0]["shares_count"]) == int
    assert type(notices[0]["comments_count"]) == int
    assert type(notices[0]["summary"]) == str
    assert type(notices[0]["sources"]) == list
    assert type(notices[0]["categories"]) == list
