# flake8: noqa

import pytest
from tech_news.collector.exporter import csv_exporter
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

NEW_NOTICE_UPDATE = {
    "url": "https://www.tecmundo.com.br/vamos.htm",
    "title": "Vamoscomtudo",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Leonardo",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia 2",
    "sources": ["ResetEra2"],
    "categories": ["PC", "Console"],
}


FILE_CSV = "file_csv.csv"
with open(FILE_CSV, encoding="utf-8") as f:
    file_csv_file = f.readlines()

FILE_CSV_UPDATE = "file_csv_update.csv"
with open(FILE_CSV_UPDATE, encoding="utf-8") as f:
    file_csv_update_file = f.readlines()


def test_sera_validado_exportar_arquivo_invalido_ira_mostrar_erro():
    with pytest.raises(ValueError, match="Formato invalido"):
        assert csv_exporter("file_incorrect.json")


def test_sera_validado_exportar_arquivo_com_sucesso():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    csv_exporter("export_correct.csv")
    filename = "export_correct.csv"
    with open(filename, encoding="utf-8") as f:
        content = f.readlines()
    assert content == file_csv_file


def test_sera_validado_atualizar_arquivo_com_mesmo_nome_com_sucesso():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE_UPDATE)
    csv_exporter("export_correct.csv")
    filename = "export_correct.csv"
    with open(filename, encoding="utf-8") as f:
        content = f.readlines()
    assert content == file_csv_update_file
