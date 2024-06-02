import re
import csv


def format_name(contacts):
    """Функция разделяет имена на Ф+И+О"""
    for person in contacts:
        if len(person[0].split()) == 3:  # обработка ФИО
            surname_split = person[0].split()
            person[0], person[1], person[2] = person[0].split()[0], surname_split[1], surname_split[2]
        if len(person[1].split()) == 2:  # обработка Ф+ИО
            name_split = person[1].split()
            person[1], person[2] = name_split[0], name_split[1]
        if len(person[0].split()) == 2:  # обработка ФИ
            surname_split = person[0].split()
            person[0], person[1] = person[0].split()[0], surname_split[1]

    return contacts


def format_phone(contacts):
    """Функция приводит номера телефонов к одному формату"""
    pattern = r"(\+7|8)?\s?\(?(\d{3}?)\)?[-\s]?(\d{3})[-\s]?(\d{2})-?(\d{2})(\s?)\(?([доб.]{4})?\s?(\d{4})?\)?"
    substitution = r"+7(\2)\3-\4-\5\6\7\8"
    for person in contacts:
        person[5] = re.sub(pattern, substitution, person[5])

    return contacts


def duble(contacts):
    """Функция объединяет дублирующие записи"""
    for person in contacts:
        for another_person in contacts:
            if person[0] in another_person[0]:
                for i in range(7):
                    if person[i] == '':
                        person[i] = another_person[i]

    format_contacts = []
    for person in contacts:
        if len(person) != 7:  # удаляется контакт, длина списка которого отличается от длины списка других
            del person[7:]
        if person not in format_contacts:
            format_contacts.append(person)

    return format_contacts


if __name__ == "__main__":

    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts = list(rows)

    format_name(contacts)
    format_phone(contacts)
    format_contacts = duble(contacts)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(format_contacts)


