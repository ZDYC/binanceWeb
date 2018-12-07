# from django.test import TestCase
import requests
import json


class ApiException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class Api(object):

    url = 'http://127.0.0.1:8000/trade/'
    cookies = None

    def __post(self, method, **kwargs):
        url = self.url + method + '/'
        if method == 'login':
            res = requests.post(url, data=kwargs)
            if isinstance(res.text, str):
                data = json.loads(res.text)
                if data['errno'] == 0 and data['data'] == 1:
                    self.cookies = res.cookies
                    return res.text
        else:
            return requests.post(
                url=url,
                data=kwargs,
                cookies=self.cookies
            )

    def __get(self, method, **kwargs):
        url = self.url + method + '/'
        if self.cookies:
            try:
                res = requests.get(
                    url=url,
                    params=kwargs,
                    cookies=self.cookies)
            except Exception as e:
                return {'error': 'error of inet!'}
            else:
                if method == 'logout':
                    self.cookies = None
                return res
        else:
            return {'errno': 'please login!'}

    def login(self, username, password):
        return self.__post(
            method='login',
            username=username,
            password=password
        )

    def logout(self):
        return self.__get(
            method='logout',
            cookies=self.cookies
        )


if __name__ == '__main__':
    api = Api()
    api.login('0001', '123456')
    print(api.logout().text)
    print(api.cookies)
