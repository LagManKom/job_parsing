from utils.classes import SuperJobAPI, HeadHunterAPI, CreateFileJson
from utils.exception import InputError


def main():
    """
    Основной код программы для запуска
    """
    # спрашиваем у пользователя ключевое слово для поиска
    keyword = input('Введите ключевое слово: ').title()

    vacancies = []

    if len(keyword) == 0:
        raise InputError('Вы ничего не ввели')
    if keyword.lower() == 'exit':
        return print('Выход')

    # создаем экземпляры класса
    hh = HeadHunterAPI(keyword)
    sj = SuperJobAPI(keyword)

    # Спрашиваем через какое Api будет искать вакансии
    while True:
        answer = input('Выберите API: HeadHunter, SuperJob ')

        if len(answer) == 0:
            print(InputError('Вы ничего не ввели'))
        elif answer.lower() == 'exit':
            return print('Выход..')

        if answer.lower() == 'superjob' or answer.lower() == 'sj':
            sj.get_vacancies()  # получаем вакансии
            vacancies.extend(sj.get_formatted_vacancies())  # складываем форматированные вакансии в наш список
            break
        elif answer.lower() == 'headhunter' or answer.lower() == 'hh':
            hh.get_vacancies()
            vacancies.extend(hh.get_formatted_vacancies())
            break
        else:
            print('Нет такого API, попробуйте снова')

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


if __name__ == '__main__':
    main()
