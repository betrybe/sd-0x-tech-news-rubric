import re
import datetime
from tech_news.database import db


def search_by_title(title):
    title_to_search = re.compile(title, re.IGNORECASE)
    query = (db.news.find({"title": title_to_search},
                          {"title": 1, "url": 1, "_id": 0}))
    result = [(result["title"], result["url"]) for result in query]
    return list(result)


def search_by_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    else:
        date_to_search = re.compile(date, re.IGNORECASE)
        query = db.news.find(
            {"timestamp": date_to_search}, {"title": 1, "url": 1, "_id": 0}
        )
        result = [(result["title"], result["url"]) for result in query]
        return result


def search_by_source(source):
    source_to_search = re.compile(source, re.IGNORECASE)
    unwind = {"$unwind": "$sources"}
    match = {
        "$match": {
            "sources": {
                "$regex": source_to_search,
            }
        }
    }
    query = db.news.aggregate([unwind, match])
    result = [(result["title"], result["url"]) for result in query]
    return list(result)


def search_by_category(category):
    category_to_search = re.compile(category, re.IGNORECASE)
    unwind = {"$unwind": "$categories"}
    match = {
        "$match": {
            "categories": {
                "$regex": category_to_search,
            }
        }
    }
    query = db.news.aggregate([unwind, match])
    result = [(result["title"], result["url"]) for result in query]
    return list(result)