import json
import os
import requests

from utils.abstract_classes import FormattedVacancies


class HeadHunterAPI(FormattedVacancies):
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, keyword):
        self.vacancies = []
        self.params = {
            'per_page': 10,
            'page': None,
            'text': keyword
        }

    def get_request(self):
        """
        Отправляет запрос на url класса
        :return: данные в формате json по ключу items
        """
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f'Статус код: {response.status_code}')
        return response.json()['items']

    def get_vacancies(self, pages_count=2):
        """
        Получает вакансии по страницам и складывает их в атрибут класса vacancies
        :param pages_count: количество страниц для парсинга
        """
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params['page'] = page
            print(f'Парсинг страницы {page + 1} ')
            page_vacancies = self.get_request()
            if len(page_vacancies) == 0:
                break
            self.vacancies.extend(page_vacancies)
            print('Вакансии загружены')
            print('---')

    def get_formatted_vacancies(self):
        """
        Форматирует полученные вакансии из get_vacancies в удобный для нас формат
        :return: список словарей с данными о каждой вакансии
        """
        formatted_vacancies = []

        for vacancy in self.vacancies:
            formatted_vacancy = {
                'employer': vacancy['employer']['name'],
                'title': vacancy['name'],
                'url': vacancy['alternate_url'],
                'api': 'HeadHunter',
                'salary_from': vacancy['salary']['from'] if vacancy['salary'] else None,
                'salary_to': vacancy['salary']['to'] if vacancy['salary'] else None,
                'currency': vacancy['salary']['currency'] if vacancy['salary'] else None
            }
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies


class SuperJobAPI(FormattedVacancies):
    url = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword):
        self.vacancies = []
        self.params = {
            'count': 10,
            'page': None,
            'keyword': keyword
        }
        self.headers = {
            'api': os.getenv('SUPERJOB_API')
        }

    def get_request(self):
        """
        Отправляет запрос на url класса
        :return: данные в формате json по ключу items
        """
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f'Статус код: {response.status_code}')
        return response.json()['items']

    def get_vacancies(self, pages_count=2):
        """
        Получает вакансии по страницам и складывает их в атрибут класса vacancies
        :param pages_count: количество страниц для парсинга
        """
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params['page'] = page
            print(f'Парсинг страницы {page + 1} ')
            page_vacancies = self.get_request()
            if len(page_vacancies) == 0:
                break
            self.vacancies.extend(page_vacancies)
            print('Вакансии загружены')
            print('---')

    def get_formatted_vacancies(self):
        """
        Форматирует полученные вакансии из get_vacancies в удобный для нас формат
        :return: список словарей с данными о каждой вакансии
        """

        # создаем список вакансий
        formatted_vacancies = []

        # форматируем каждую вакансию в удобный для нас вид
        for vacancy in self.vacancies:
            formatted_vacancy = {
                'employer': vacancy['first_name'],
                'title': vacancy['profession'],
                'url': vacancy['link'],
                'api': 'SuperJob',
                'salary_from': vacancy['payment_from'],
                'salary_to': vacancy['payment_to'],
                'currency': vacancy['currency']
            }

            # добавляем в наш список созданный словарь
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies


class CreateFileJson:
    def __init__(self, keyword, vacancies_json):
        self.filename = f'{keyword}_vacancies.json'
        self.creature(vacancies_json)

    def creature(self, vacancies_json):
        """
        Создает файл и кладет в него список вакансий в формате json
        :param vacancies_json: Список формата json
        """
        with open(self.filename, mode='w', encoding='utf-8') as file:
            json.dump(vacancies_json, file, indent=2)

    def read(self):
        """
        Читает созданный файл, создает экземпляр класса Vacancy для каждой вакансии в файле
        :return: Список экземпляров класса Vacancy
        """
        with open(self.filename, mode='r', encoding='utf-8') as file:
            vacancies = json.load(file)
            return [Vacancy(x) for x in vacancies]

    def sort_by_salary(self):
        """
        Предлагает пользователю выбор, как сортировать вакансии, после чего читает данные с файла и сортирует
        :return: Отсортированный список вакансий
        """
        sorting = True if input('"Low" - сортировка по наименьшей зарплате\n'
                                '"high" - сортировка по наибольшей зарплате\n').lower() == 'high' else False
        vacancies = self.read()

        return sorted(vacancies, key=lambda x: (x.salary_from if x.salary_from else 0,
                                                x.salary_to if x.salary_to else 0), reverse=sorting)


class Vacancy:

    def __init__(self, vacancy):
        self.employer = vacancy['employer']
        self.title = vacancy['title']
        self.url = vacancy['url']
        self.api = vacancy['api']
        self.salary_from = vacancy['salary_from']
        self.salary_to = vacancy['salary_to']
        self.currency = vacancy['currency']
        self.__salary = None

    def __repr__(self):
        """
        :return: Возвращаем информацию в удобном формате для пользователя
        """

        # проверяем указана ли зарплата
        salary = ''
        if not self.salary_from and not self.salary_to:
            salary = 'Не указана'
        else:
            if self.salary_from and self.salary_to:
                salary = f'От {self.salary_from} до {self.salary_to} {self.currency}'
                self.__salary = self.salary_to
            else:
                if self.salary_from:
                    salary = f'От {self.salary_from} {self.currency}'
                    self.__salary = self.salary_from
                elif self.salary_to:
                    salary = f'До {self.salary_to}{self.currency}'
                    self.__salary = self.salary_to

        return f'Вакансия: {self.title}\n' \
               f'Ссылка: {self.url}\n' \
               f'Зарплата: {salary}\n' \
               f'Работодатель: {self.employer}\n'

    def __eq__(self, other):
        return self.__salary == other.__salary
