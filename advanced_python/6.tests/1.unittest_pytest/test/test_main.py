import pytest
from unittest import TestCase

from main import task_1, task_2, task_4, YaFolder


class TestTask1:
    @pytest.mark.parametrize("logs, expected", (
            ([{'visit1': ['Москва', 'Россия']},
              {'visit2': ['Дели', 'Индия']},
              {'visit3': ['Владимир', 'Россия']},
              {'visit4': ['Лиссабон', 'Португалия']},
              {'visit5': ['Париж', 'Франция']},
              {'visit6': ['Лиссабон', 'Португалия']},
              {'visit7': ['Тула', 'Россия']},
              {'visit8': ['Тула', 'Россия']},
              {'visit9': ['Курск', 'Россия']},
              {'visit10': ['Архангельск', 'Россия']}],
             [{'visit1': ['Москва', 'Россия']},
              {'visit3': ['Владимир', 'Россия']},
              {'visit7': ['Тула', 'Россия']},
              {'visit8': ['Тула', 'Россия']},
              {'visit9': ['Курск', 'Россия']},
              {'visit10': ['Архангельск', 'Россия']}]),
            ([{'visit2': ['Дели', 'Индия']},
              {'visit4': ['Лиссабон', 'Португалия']},
              {'visit5': ['Париж', 'Франция']},
              {'visit6': ['Лиссабон', 'Португалия']}],
             [])
    ))
    def test_task_1(self, logs, expected):
        result = task_1(logs)
        assert result == expected


class TestTask2(TestCase):
    def test_task_2(self):
        ids = {'user1': [213, 213, 213, 15, 213],
               'user2': [54, 54, 119, 119, 119],
               'user3': [213, 98, 98, 35]}
        result = task_2(ids)
        expected = [35, 98, 213, 54, 15, 119]

        self.assertCountEqual(result, expected)


class TestTask4:
    @pytest.mark.parametrize("stats, expected", (
            ({'facebook': 55, 'yandex': 120, 'vk': 115, 'google': 99, 'email': 42, 'ok': 98}, {'yandex'}),
            ({'facebook': 55, 'yandex': 120, 'vk': 120, 'google': 99, 'email': 42, 'ok': 98}, {'yandex', 'vk'})
    ))
    def test_task_4(self, stats, expected):
        result = task_4(stats)
        assert set(result) == expected


class TestYaFolderCreate(TestCase):
    def setUp(self):
        self.folder_name = 'test_folder'

    def tearDown(self):
        YaFolder(self.folder_name).delete()

    def test_positive_create_folder(self):
        result = YaFolder(self.folder_name).create()
        expected = 201
        self.assertEqual(result, expected)

    def test_negative_1_create_folder(self):
        YaFolder(self.folder_name).create()
        result = YaFolder(self.folder_name).create()
        expected = 409
        self.assertEqual(result, expected)

    def test_negative_2_create_folder(self):
        """В этом тесте пытаемся создать папку по заведомо несуществующему пути. Но яндекс почему-то выдает:
        "409 Ресурс "{path}" уже существует"
        """
        result = YaFolder('not_exist_folder/test_folder_2').create()
        expected = 409
        self.assertEqual(result, expected)

    def test_check_folder(self):
        YaFolder(self.folder_name).create()
        result = YaFolder(self.folder_name).check()
        expected = 200
        self.assertEqual(result, expected)
