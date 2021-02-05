from tech_news.database import find_news
import csv


def csv_exporter(filepath):
    if not filepath.endswith(".csv"):
        raise ValueError("Formato invalido")

    with open(filepath, mode="w") as file:
        writer = csv.writer(file, delimiter=";")
        top_row = [
            "url",
            "title",
            "timestamp",
            "writer",
            "shares_count",
            "comments_count",
            "summary",
            "sources",
            "categories",
        ]
        second_row = find_news()

        writer.writerow(top_row)

        for item in second_row:
            writer.writerow(
                [
                    item["url"],
                    item["title"],
                    item["timestamp"],
                    item["writer"],
                    item["shares_count"],
                    item["comments_count"],
                    item["summary"],
                    ",".join(item["sources"]),
                    ",".join(item["categories"]),
                ]
            )
