# flake8: noqa

from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_date,
    search_by_source,
    search_by_category,
)
import pytest
from pymongo import MongoClient
from decouple import config

DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default="27017")

client = MongoClient(host=DB_HOST, port=int(DB_PORT))
db = client.tech_news

NEW_NOTICE = {
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

LIST = [("Vamoscomtudo", "https://www.tecmundo.com.br/vamos.htm")]


def test_buscar_noticia_pelo_titulo_com_sucesso():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_title("Vamoscomtudo") == LIST


def test_buscar_titulo_que_nao_existe_deve_retornar_vazio():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_title("titulo_invalido") == []


def test_buscar_noticia_pelo_titulo_com_sucesso_com_sentive_case():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_title("VAMOSCOMTUDO") == LIST


def test_buscar_noticia_pela_data_com_sucesso():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_date("2020-11-23") == LIST


def test_buscar_data_que_nao_existe_deve_retornar_vazio():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_date("2019-12-12") == []


def test_buscar_data_que_com_formato_invalido_deve_retornar_erro():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    with pytest.raises(ValueError, match="Data inválida"):
        search_by_date("21-12-1980")


def test_buscar_noticia_pela_fonte_com_sucesso():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_source("ResetEra") == LIST


def test_buscar_fonte_que_nao_existe_deve_retornar_vazio():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_source("fonte_invalida") == []


def test_buscar_noticia_pela_fonte_com_sucesso_com_sentive_case():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_source("RESETERA") == LIST


def test_buscar_noticia_pela_categoria_com_sucesso():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_category("Console") == LIST


def test_buscar_categoria_que_nao_existe_deve_retornar_vazio():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_category("categoria_invalida") == []


def test_buscar_noticia_pela_categoria_com_sucesso_com_sentive_case():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_category("CONSOLE") == LIST
