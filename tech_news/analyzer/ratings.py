from tech_news.database import db


def top_5_news():
    rates = []
    query_result = db.news.find()
    for result in query_result:
        result["score"] = result["shares_count"] + result["comments_count"]
        rates.append(result)
    sorted_rates = sorted(rates, key=lambda k: k["score"])

    top_rates = [(rate["title"], rate["url"]) for rate in sorted_rates][:5]
    return top_rates


def top_5_categories():
    sorted_rates = db.news.aggregate(
        [
            {"$unwind": "$categories"},
            {"$group": {"_id": "$categories", "total": {"$sum": 1}}},
            {"$sort": {"_id": 1}},
        ]
    )
    top_ids = [rate["_id"] for rate in sorted_rates][:5]

    return top_ids
