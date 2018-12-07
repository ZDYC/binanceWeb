# from django.test import TestCase
from binance.client import Client
import requests
import json


class ApiException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class Api(object):

    url = 'http://127.0.0.1:8000/trade/'
    cookies = None
    key = 'pw6xPzMtyyY3fWL2l2AEod1cLr1VBni21almeVxFTpWLtgJJd5mEE46SUKB9hpN2'
    secret = 'wtA7Hr54fDEMssePXIDkPye7eafSIVuUmPcW4TkVok9dwU59K6GQ3hTW7e1kSrKG'

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

    def create_order(self, symbol, price, quantity, side, order_type, time_in_force):
        return self.__post(
            method='create_order',
            symbol=symbol,
            price=price,
            quantity=quantity,
            side=side,
            order_type=order_type,
            time_in_force=time_in_force
        )

    def test_binance(self):
        client = Client(self.key, self.secret)
        res = client.get_account()
        print(res)


if __name__ == '__main__':
    api = Api()
    api.login('0001', '123456')
    # print(api.logout().text)
    # print(api.cookies)
    res = api.create_order(symbol='EOSBTC', price='0.00123',
                           quantity=1, side='BUY',
                           order_type='LIMIT', time_in_force='GTC')
    print(res.text)
