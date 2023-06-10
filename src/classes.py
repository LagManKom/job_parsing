import json
import os
from abc import ABC, abstractmethod

import requests


class WorkingAPI(ABC):
    @abstractmethod
    def get_vacancies(self, profession):
        pass

    @abstractmethod
    def get_request(self):
        pass


class HeadHunterAPI(WorkingAPI):
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, keyword):
        self.vacancies = []
        self.params = {
            'per_page': 100,
            'page': None,
            'text': keyword
        }

    def get_request(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f'Статус код: {response.status_code}')
        return response.json()['items']

    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params['page'] = page
            print(f'Парсинг страницы {page} ')
            try:
                page_vacancies = self.get_request()
            except Exception as error:
                print(f'Ошибка {error}')
            else:
                self.vacancies.extend(page_vacancies)
                print('Вакансии загружены')
            if len(page_vacancies) == 0:
                break


class SuperJobAPI(WorkingAPI):
    url = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword):
        self.vacancies = []
        self.params = {
            'count': 100,
            'page': None,
            'keyword': keyword
        }
        self.headers = {
            'Api': os.getenv('SuperJobAPI')
        }

    def get_vacancies(self, profession):
        pass

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f'Статус код: {response.status_code}')
        return response.json()['items']


class CreateFileJson:
    def __init__(self, keyword, vacancies_json):
        self.filename = f'{keyword}_vacancies.json'
        self.creature(vacancies_json)

    def creature(self, vacancies_json):
        with open(self.filename, 'w', 'utf-8') as file:
            json.dump(vacancies_json, file, indent=4)

    def read(self):
        with open(self.filename, 'r', 'utf-8') as file:
            vacancies = json.load(file)
            return [Vacancy(x) for x in vacancies]

    def sort_by_salary(self):
        sorting = True if input('"Low" - сортировка по наименьшей зарплате\n'
                                '"high" - сортировка по наибольшей зарплате\n').lower() == 'high' else False
        vacancies = self.read()

        return sorted(vacancies, key=lambda x: (x.salary_form if x.salary_from else 0,
                                                x.salary_to if x.salary_to else 0), reverse=sorting)


class Vacancy:

    def __init__(self, vacancy):
        self.emloyer = vacancy['employer']
        self.title = vacancy['title']
        self.url = vacancy['url']
        # self.api = vacancy['api']
        self.salary_from = vacancy['salary_rom']
        self.salary_to = vacancy['salary_to']
        self.currency = vacancy['currency']
        # self.currency_value = vacancy['currency_value']

    def __str__(self):
        salary = ''
        if not self.salary_from and not self.salary_to:
            salary = 'Не указана'
        else:
            if self.salary_from and self.salary_to:
                salary = f'От {self.salary_from} до {self.salary_to} {self.currency}'
            else:
                if self.salary_from:
                    salary = f'От {self.salary_from} {self.currency}'

                elif self.salary_to:
                    salary = f'До {self.salary_to}'
        return f'''
        Вакансия: {self.title}
        Ссылка: {self.url}
        Зарплата: {salary}
        Работодатель: {self.emloyer}
        '''
