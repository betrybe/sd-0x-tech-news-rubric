import requests
from parsel import Selector
from time import sleep


def fetch_content(url, timeout=3, delay=0.5):
    sleep(delay)
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ReadTimeout):
        return ""
    else:
        return response.text


def get_data(fetcher, link):
    selector = Selector(text=fetcher(link))
    data = {}
    data['url'] = link
    data['title'] = selector.css(
                    ".tec--article__header__title::text"
                ).get()
    data["timestamp"] = selector.css(
                    "#js-article-date::attr(datetime)"
                ).get()
    data["writer"] = selector.css(
                    ".tec--author__info__link::text"
                ).get()
    data["shares_count"] = int(selector.css(
                    ".tec--toolbar__item::text"
                ).re_first(r"\d"))
    data["comments_count"] = int(selector.css(
                    "#js-comments-btn::attr(data-count)"
                ).get())
    data["summary"] = selector.css(
                    ".tec--article__body p *::text"
                ).get()
    data["sources"] = selector.css(
                    ".z--mb-16 .tec--badge::text"
                ).getall()
    data["categories"] = selector.css(
                    "#js-categories .tec--badge::text"
                ).getall()

    return data


def get_links(selector):
    return selector.css(
            ".tec--list__item .tec--card__title__link::attr(href)"
        ).getall()




def scrape(fetcher, pages=1):
    page_list = []
    BASE_URL = 'https://www.tecmundo.com.br/novidades'
    for page in range(pages):
        response = fetcher(
            f"{BASE_URL}?page={page}"
        )
        selector = Selector(text=response)
        links = get_links(selector)
        for link in links:
            page_list.append(get_data(fetcher=fetcher, link=link))
    return page_list