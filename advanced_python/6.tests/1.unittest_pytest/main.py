import requests


def task_1(logs):
    filtered_geo_logs = []
    for visit in logs:
        if 'Россия' in list(visit.values())[0]:
            filtered_geo_logs.append(visit)
    return filtered_geo_logs


def task_2(user_ids):
    set_ids = set()
    for uid in user_ids.values():
        set_ids |= set(uid)
    return list(set_ids)


def task_4(stats):
    return [k for k, v in stats.items() if v == max(stats.values())]


class YaFolder:
    def __init__(self, folder_name):
        self.token = 'y0_AgAEA7qiNyBMAADLWwAAAADgANSMy6vDlXprR8ing8lQdRb7zHYq1UE'
        self.url = 'https://cloud-api.yandex.net'
        self.urn_create_folder = '/v1/disk/resources'
        self.headers = {'Accept': 'application/json',
                        'Authorization': self.token}
        self.params = {'path': folder_name}

    def create(self):
        return requests.put(self.url + self.urn_create_folder, headers=self.headers, params=self.params).status_code

    def check(self):
        return requests.get(self.url + self.urn_create_folder, headers=self.headers, params=self.params).status_code

    def delete(self):
        return requests.delete(self.url + self.urn_create_folder, headers=self.headers, params=self.params).status_code
