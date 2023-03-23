import json
import re
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = Headers(browser='firefox', os='windows', headers=True).generate()
sought_keywords = ('Django', 'Flask')


def get_title(tag):
    return tag.find('a', {'data-qa': 'serp-item__title'}).text


def get_link(tag):
    return tag.find('a', {'data-qa': 'serp-item__title'})['href']


def get_city(tag):
    vacancy_view_raw_address = tag.findAll('div', {'data-qa': 'vacancy-serp__vacancy-address'})[0].text
    city_pattern = re.compile(r'^(\w+\s?-?)+')
    return city_pattern.search(vacancy_view_raw_address).group(0)


def get_key_skills(ad_htm):
    """
        В ключевых навыках может быть указано, например, "Framework Django" для того, чтобы не пропустить такие
        вакансии разобъем все ключевые навыки на отдельные слова. Для того чтобы исключить дублирование слов
        преобразуем в множество.
        """
    skills = BeautifulSoup(ad_htm.text, 'lxml').findAll('span', {'data-qa': 'bloko-tag__text'})
    return set(sum(list(map(str.split, (s.text.strip().lower() for s in skills))), []))


def get_salary(ad_htm):
    return BeautifulSoup(ad_htm.text, 'lxml').find('div', {'data-qa': 'vacancy-salary'}).text


def get_company(ad_htm):
    return BeautifulSoup(ad_htm.text, 'lxml').find('a', {'data-qa': 'vacancy-company-name'}).text


def skills_is_found(needles, heystack):
    return any(list(map(lambda x: x.lower() in heystack, needles)))


def save_to_json(data):
    with open('json.txt', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


html = requests.get(URL, headers=headers)
vacancy_bodies = BeautifulSoup(html.text, 'lxml').findAll('div', class_='vacancy-serp-item-body__main-info')

vacancies_list = []
for body in vacancy_bodies:
    ad_html = requests.get(get_link(body), headers=headers)
    skill_words = get_key_skills(ad_html)
    if skills_is_found(needles=sought_keywords, heystack=skill_words):
        vacancy_dict = {get_title(body): {'href': get_link(body),
                                          'salary': get_salary(ad_html),
                                          'company': get_company(ad_html),
                                          'city': get_city(body)}}
        vacancies_list.append(vacancy_dict)
save_to_json(vacancies_list)
