import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        to_bool = {'true': True, 'false': False}
        for phone in phones:
            # TODO: Добавьте сохранение модели
            phone_record = Phone(id=int(phone['id']),
                                 name=phone['name'],
                                 price=int(phone['price']),
                                 image=phone['image'],
                                 release_date=phone['release_date'],
                                 lte_exists=to_bool[phone['lte_exists'].lower()])
            phone_record.save()
