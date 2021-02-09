import requests
from time import sleep
from parsel import Selector


"""
Deve ser capaz de realizar uma requisição HTTP e retornar o conteúdo como
resposta.
- Caso a resposta tenha o código de status diferente de 200, deve-se
retornar uma str vazia;

- O tempo máximo de resposta do servidor deve ser configurado como
parâmetro e por padrão será 3 segundos;

- Para evitar um problema de Rate Limit faça um sleep com tempo obtido por
parâmetro, mas que por padrão seja 0.5 segundos;

- Caso a requisição seja bem sucedida retorne seu conteúdo de texto;
"""


def fetch_content(url, timeout=3, delay=0.5):
    while True:
        try:
            response = requests.get(url, timeout=timeout)
            sleep(delay)
            return response.text
        except requests.ReadTimeout:
            return ""


def fetcher(url, timeout=3, delay=0.5):
    if url.startswith("https://www.tecmundo.com.br/novidades"):
        file_name = "tests/test_collector/index.html"
    else:
        file_name = "tests/test_collector/notice.html"
    with open(file_name, encoding="utf-8") as file:
        return file.read()


def scrape(fetcher, pages=1):
    BASE_URL = "https://www.tecmundo.com.br/"
    START_URL = "novidades"

    next_page_url = START_URL

    page_counter = 0
    notices = []

    while page_counter != pages:

        if not next_page_url:
            next_page_url = START_URL

        notices_response = fetcher(BASE_URL + next_page_url)

        notices_selector = Selector(notices_response)

        page_counter += 1

        for list_item in notices_selector.css(".tec--list__item"):

            notice = {}

            notice["url"] = list_item.css(
                "article .tec--card__info h3 a::attr(href)"
            ).get()

            inner_response = fetcher(BASE_URL + notice["url"])
            inner_selector = Selector(inner_response)

            notice["title"] = inner_selector.css(
                "#js-article-title::text"
            ).get()

            notice["timestamp"] = inner_selector.css(
                "#js-article-date::attr(datetime)"
            ).get()

            notice["writer"] = inner_selector.css(
                "#js-author-bar  div  p.z--m-none.z--truncate.z--font-bold \
                a::text"
            ).get()

            share_counter_string = inner_selector.css(
                "#js-author-bar nav div:nth-child(1)::text"
            ).get()
            notice["shares_count"] = int(share_counter_string.split()[0])

            notice["comments_count"] = int(
                inner_selector.css("#js-comments-btn::attr(data-count)").get()
            )

            notice["summary"] = inner_selector.css(
                "#js-main div.z--container article div.tec--article__body-grid \
                div.tec--article__body.z--px-16.p402_premium \
                p:nth-child(1)::text"
            ).get()

            notice["sources"] = list(
                inner_selector.css(
                    "#js-main div.z--container article \
                    div.tec--article__body-grid \
                    div.z--mb-16.z--px-16 div a::text"
                ).getall()
            )

            notice["categories"] = inner_selector.css(
                "#js-categories > a::text"
            ).getall()

            notices.append(notice)

        next_page_url = notices_selector.css(".next a::attr(href)").get()

    return notices


scrape(fetcher=fetcher, pages=2)
