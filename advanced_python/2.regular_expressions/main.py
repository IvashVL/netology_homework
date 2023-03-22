from pprint import pprint
import csv
import re


class Phonebook:
    def __init__(self):
        self.phonebook = {}

    def add_contact(self, raw_data):
        """
        Функция add_contact() добавляет данные контакта из входного файла в словарь self.phonebook

        :param raw_data: необработанная строка с данными контакта из входного файла
        """
        contact = self.get_contact_from_raw(raw_data)
        name = ''.join(contact[:2])
        if name in self.phonebook.keys():
            self.phonebook.update({name: self.update_contact_from_raw(self.phonebook[name], raw_data)})
        else:
            self.phonebook.update({name: contact})

    def get_list(self):
        """
        Функция get_list() возвращает список контактов
        """
        return (cont for cont in self.phonebook.values())

    def get_contact_from_raw(self, raw_data):
        """
        Функция get_contact_from_raw() возвращает список с обработанными данными контакта.
        :param raw_data: необработанная строка с данными контакта из входного файла
        """
        contact = self.get_name_from_raw(raw_data)
        if len(contact) == 2:
            contact += [''] * 5
        elif len(contact) == 3:
            contact += [''] * 4
        return self.update_contact_from_raw(contact, raw_data)

    def get_name_from_raw(self, raw_data):
        """
        Функция get_name_from_raw() возвращает список с именем и с именем, фамилией и отчеством (если есть) контакта.
        :param raw_data: необработанная строка с данными контакта из входного файла
        """
        name_pattern = re.compile(r'\w+')
        name = name_pattern.findall(' '.join(raw_data[0:3]))
        if len(name) not in (2, 3):
            print(f'Ошибка обработки имени контакта: {name}')
            name = [''] * 3
        return name

    def update_contact_from_raw(self, contact, raw_data):
        """
        Функция update_contact_from_raw() обновляет данные существующего в self.phonebook контакта
        :param contact: список с данными существующего (обновляемого) контакта
        :param raw_data: необработанная строка с данными контакта из входного файла
        """
        upd_contact = contact
        if len(contact) == 7:
            if len(self.get_name_from_raw(raw_data)) == 3:
                upd_contact[2] = self.get_name_from_raw(raw_data)[2]
            if raw_data[3]:
                upd_contact[3] = raw_data[3]
            if raw_data[4]:
                upd_contact[4] = raw_data[4]
            if raw_data[5]:
                phone_pattern = re.compile(r'(\+7|8)\s?\(?(\d{3})\)?[\s|-]?(\d{3})-?(\d{2})-?'
                                           r'(\d{2})-?\s?\(?(доб.)?\ ?(\d{4})?\)?')
                phone = phone_pattern.search(re.sub(r'\b8', '+7', raw_data[5]))
                upd_contact[5] = f'{phone[1]}({phone[2]}){phone[3]}-{phone[4]}-{phone[5]}'
                if phone[7]:
                    upd_contact[5] += f' доб.{phone[7]}'
            if raw_data[6]:
                upd_contact[6] = raw_data[6]
        else:
            print(f'Ошибка обновления контакта: {contact}')
        return upd_contact

    def save_to_csv(self, file, contacts_list):
        ## Код для записи файла в формате CSV:
        with open(file, "w", newline='', encoding='utf-8') as f:
            datawriter = csv.writer(f, delimiter=',')

            ## Вместо contacts_list подставьте свой список:
            datawriter.writerow(('lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email'))
            datawriter.writerows(contacts_list)

    def read_from_csv(self, file):
        with open(file, encoding='utf-8') as f:
            rows = csv.reader(f, delimiter=",")
            contacts_list = list(rows)
        return contacts_list


phonebook = Phonebook()

## Читаем адресную книгу в формате CSV в список contacts_list:
raw_contacts_list = phonebook.read_from_csv("phonebook_raw.csv")
# pprint(raw_contacts_list)

## 1. Выполните пункты 1-3 задания.


for raw_contact in raw_contacts_list[1:]:
    phonebook.add_contact(raw_contact)

## 2. Сохраните получившиеся данные в другой файл.
phonebook.save_to_csv("phonebook.csv", phonebook.get_list())
