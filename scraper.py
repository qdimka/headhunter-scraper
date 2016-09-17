# https://kazan.hh.ru/search/vacancy?text=&specialization=1.221&area=88&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=&items_on_page=20&no_magic=true

from bs4 import BeautifulSoup
import requests

# REPLACE IT
address = 'https://kazan.hh.ru/search/vacancy?text=&area=88&salary=&currency_code=RUR&experience=between1And3' \
          '&order_by=relevance&search_period=&items_on_page=20&no_magic=true'

count_per_page = 0


def get_html(url):
    """
    Get HTML string from url
    :param url:
    :return HTML string:
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    req = requests.get(url, headers)
    return req.content


def get_page(url, number):
    """
    Get page HTML string by page number
    :param url:
    :param number:
    :return HTML string:
    """
    addr = url + '&page=' + str(number)
    return get_html(addr)


while True:
    global count_per_page

    html = get_page(address, count_per_page)
    soup = BeautifulSoup(html, "html.parser")
    vacancies = soup.find_all('div', attrs={'class': "search-result-description"})

    # check next page command state
    isNext = soup.find('span', attrs={'class': "b-pager__next-text",
                                      'data-qa': "pager-next-disabled"}) is not None

    if isNext:
        break

    # the extraction of useful data
    for vacancy in vacancies:
        # Vacancy title
        print vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title"}).text
        # Vacancy link
        print vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title"}).get('href')
        # Vacancy short description
        print vacancy.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_responsibility"}).text
        # Vacancy requirement
        print vacancy.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_requirement"}).text
        # Company name
        print vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-employer"}).text
        print '************************************************'
    count_per_page += 1
