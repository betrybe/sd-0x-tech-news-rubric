# flake8: noqa

import pytest
from tech_news.collector.importer import csv_importer

DICT = [
    dict(
        [
            ("url", "https://www.tecmundo.com.br/mobilidade-urbana.htm"),
            ("title", "Alemanha já trabalha na regulamentação de carros"),
            ("timestamp", "2020-07-20T15:30:00"),
            ("writer", "Reinaldo Zaruvni"),
            ("shares_count", "0"),
            ("comments_count", "0"),
            ("summary", "Recentemente, a Alemanha fez a Tesla pisar no freio"),
            ("sources", "AutomotiveNewsEurope"),
            ("categories", "carros"),
        ]
    )
]


def test_sera_validado_importar_arquivo_invalido_ira_mostrar_erro():
    with pytest.raises(ValueError, match="Formato invalido"):
        assert csv_importer("tests/file_incorrect.json")


def test_sera_validado_importar_arquivo_inexistente_com_formato_invalido_ira_mostrar_erro():
    with pytest.raises(ValueError, match="Formato invalido"):
        assert csv_importer("tests/file_not_exist.json")


def test_sera_validado_importar_arquivo_inexistente_ira_mostrar_erro():
    with pytest.raises(
        ValueError, match="Arquivo tests/file_not_exist.csv não encontrado"
    ):
        assert csv_importer("tests/file_not_exist.csv")


def test_sera_validado_importar_arquivo_com_sucesso():
    assert csv_importer("correct.csv") == DICT