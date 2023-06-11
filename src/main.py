from src.classes import SuperJobAPI, HeadHunterAPI, CreateFileJson
from src.exception import InputError


def main():
    vacancies = []

    keyword = input('Введите ключевое слово: ').title()
    try:
        if len(keyword) == 0:
            raise InputError
        if keyword.lower() == 'exit':
            return print('Выход')

        hh = HeadHunterAPI(keyword)
        sj = SuperJobAPI(keyword)

        answer = input('Выберите API: HeadHunter, SuperJob ')
        if len(answer) == 0:
            raise InputError
        while True:
            try:
                page_count = input('Какое количество страниц вы хотите просмотреть? ')
                if page_count.isdigit():
                    pages_count = int(page_count)
                    break
                else:
                    raise InputError
            except InputError:
                print('Введите число')

        if answer.lower() == 'superjob':
            sj.get_vacancies(pages_count=pages_count)
            vacancies.extend(sj.get_formatted_vacancies())
        elif answer.lower() == 'headhunter' or answer.lower() == 'hh':
            hh.get_vacancies(pages_count=pages_count)
            vacancies.extend(hh.get_formatted_vacancies())

        file = CreateFileJson(keyword=keyword, vacancies_json=vacancies)

        while True:
            answer = input(f'1: Показвать вакансии: \n'
                           f'2: сортировать\n'
                           f'exit: выход\n'
                           f'')
            if answer.lower() == '1':
                for x in file.read():
                    print(x)
            elif answer.lower() == '2':
                print(file.sort_by_salary())
            elif answer.lower() == 'exit':
                break
    except InputError:
        print('Вы ничего не ввели, попробуйте снова')


if __name__ == '__main__':
    main()
