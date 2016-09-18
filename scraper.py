# https://kazan.hh.ru/search/vacancy?text=&specialization=1.221&area=88&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=&items_on_page=20&no_magic=true

from bs4 import BeautifulSoup
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# REPLACE IT
address = 'https://kazan.hh.ru/search/vacancy?text=' \
          '&specialization=1.221' \
          '&area=88' \
          '&salary=30000' \
          '&currency_code=RUR' \
          '&only_with_salary=true' \
          '&experience=doesNotMatter' \
          '&employment=full' \
          '&order_by=relevance' \
          '&search_period=' \
          '&items_on_page=20' \
          '&no_magic=true'
# REPLACE IT
file_name = "D:\output.csv"

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


def export_csv(filename, head, list_rows):
    """
    Export in csv file
    :param filename:
    :param head:
    :param list_rows:
    """
    with open(filename, "wb") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(head)
            writer.writerows(list_rows)


isNext = True

list_vacancies = []
header = ["Title", "Link", "Description", "Requirement", "Company", "Date"]

while isNext:

    html = get_page(address, count_per_page)
    soup = BeautifulSoup(html, "html.parser")
    vacancies = soup.find_all('div', attrs={'class': "search-result-description"})

    # check next page command state
    isNext = soup.find('span', attrs={'class': "b-pager__next-text",
                                      'data-qa': "pager-next-disabled"}) is not None

    row = []

    # the extraction of useful data
    for vacancy in vacancies:
        # Vacancy title
        row.append(vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title"}).text)
        # Vacancy link
        row.append(vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title"}).get('href'))
        # Vacancy short description
        row.append(vacancy.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_responsibility"}).text)
        # Vacancy requirement
        row.append(vacancy.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_requirement"}).text)
        # Company name
        row.append(vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-employer"}).text)
        # Date
        row.append(vacancy.find('span', attrs={'data-qa': "vacancy-serp__vacancy-date"}).text.replace("&nbsp;", ""))

    list_vacancies.append(row)
    count_per_page += 1


export_csv(file_name, header, list_vacancies)

