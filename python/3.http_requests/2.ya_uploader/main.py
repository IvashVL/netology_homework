import requests


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        # Тут ваша логика
        # Функция может ничего не возвращать
        url = 'https://cloud-api.yandex.net'
        urn = '/v1/disk/resources/upload'
        headers = {'Accept': 'application/json',
                   'Authorization': self.token}
        params = {'path': file_path,
                  'overwrite': 'true'}
        href = requests.get(url + urn, headers=headers, params=params).json()['href']
        with open(file_path, 'rb') as file:
            requests.put(href, files={'file': file})


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = 'test.txt'
    token = ''
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)

