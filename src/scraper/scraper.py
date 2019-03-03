import requests
from bs4 import BeautifulSoup


class HeadHunterScraper(object):
    __default_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                       'Chrome/52.0.2743.116 Safari/537.36'}
    __base = 'https://{0}.hh.ru/search/vacancy?{1}'

    __default_params = {
        'search_field': '',
        'area': 88,
        'salary': '',
        'currency_code': 'RUR',
        'experience': 'doesNotMatter',
        'order_by': 'relevance',
        'search_period': '',
        'items_on_page': 20,
        'no_magic': 'true',
        'from': 'suggest_post'
    }

    __delimeter = ';'

    def __get_html(self, url):
        return requests \
            .get(url, self.__default_headers) \
            .content

    def __get_page(self, url, number):
        return self.__get_html(url + '&page=' + str(number))

    def __url_resolver(self, city, **params):
        query = '&'.join(['{0}={1}'.format(k, v) for k, v in params.iteritems()])
        return self.__base \
            .format(city, query)

    def __fill_vacancy_properties(self, vacancy):
        # Vacancy title
        yield vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title"}).text
        # Vacancy link
        yield vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title"}).get('href')
        # Vacancy short description
        yield vacancy.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_responsibility"}).text
        # Vacancy requirement
        yield vacancy.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_requirement"}).text
        # Company name
        yield vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-employer"}).text
        # Date
        yield vacancy.find('span', attrs={'data-qa': "vacancy-serp__vacancy-date"}).text.replace("&nbsp;", "")

    def validate(fn):
        def wrapper(self, city, **params):
            if not params.has_key('text'):
                raise Exception('Missing text property')
            return fn(self, city, **params)

        return wrapper

    def merge_params(fn):
        def wrapper(self, city, **params):
            merged_params = dict(self.__default_params)
            merged_params.update(params)
            return fn(self, city, **merged_params)

        return wrapper

    @validate
    @merge_params
    def parse(self, city, **params):
        page = 0
        is_next = True
        vacancies = []
        url = self.__url_resolver(city, **params)
        while is_next:
            html = self.__get_page(url, page)
            soup = BeautifulSoup(html, "html.parser")
            raw_vacancies = soup.find_all('div', attrs={'class': "search-result-description"})

            # check next page exists
            is_next = soup.find('span', attrs={'class': "b-pager__next-text",
                                               'data-qa': "pager-next-disabled"}) is not None

            # the extraction of useful data
            for vacancy in raw_vacancies:
                vacancies.append(self.__delimeter.join(self.__fill_vacancy_properties(vacancy)))
            page += 1
        return vacancies

