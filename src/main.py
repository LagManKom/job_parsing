from utils.classes import SuperJobAPI, HeadHunterAPI, CreateFileJson
from utils.exception import InputError


def main():
    """
    Основной код программы для запуска
    """
    vacancies = []

    # спрашиваем у пользователя ключевое слово для поиска
    keyword = input('Введите ключевое слово: ').title()
    try:
        if len(keyword) == 0:
            raise InputError
        if keyword.lower() == 'exit':
            return print('Выход')

        # создаем экземпляры класса
        hh = HeadHunterAPI(keyword)
        sj = SuperJobAPI(keyword)

        # Спрашиваем через какое Api будет искать вакансии
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
            sj.get_vacancies(pages_count=pages_count)  # получаем вакансии
            vacancies.extend(sj.get_formatted_vacancies())  # складываем форматированные вакансии в наш список
        elif answer.lower() == 'headhunter' or answer.lower() == 'hh':
            hh.get_vacancies(pages_count=pages_count)
            vacancies.extend(hh.get_formatted_vacancies())

        # Создаем экземпляр класса для работы с файлом
        file = CreateFileJson(keyword=keyword, vacancies_json=vacancies)

        while True:
            answer = input(f'1: Показать вакансии: \n'
                           f'2: Сортировать\n'
                           f'exit: Выход\n'
                           f'')
            if answer.lower() == '1':
                for x in file.read():
                    print(x)
            elif answer.lower() == '2':
                for x in file.sort_by_salary():
                    print(x)
            elif answer.lower() == 'exit':
                break
    except InputError:
        print('Вы ничего не ввели, попробуйте снова')


# запуск кода
if __name__ == '__main__':
    main()
