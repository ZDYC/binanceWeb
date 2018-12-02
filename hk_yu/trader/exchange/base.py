"""交易平台的api实现
"""
from binance.exceptions import BinanceAPIException, BinanceRequestException
from core.exceptions import ExchangeException


def exception_haneler(func):
    """异常统一处理，转成ExchangeException
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BinanceAPIException as e:
            raise ExchangeException(e.code, e.message)
        except BinanceRequestException as e:
            raise ExchangeException(-1, '币安服务器异常，稍后重试!')
    return wrapper


class Exchange(object):


    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def create_order(self, symbol, side, quantity, price, client_order_id,
                     order_type='LIMIT', time_in_force='GTC',
                     iceberg_qty=0.0, stop_price=None):
        raise NotImplementedError()

    def cancel_order(self, symbol, order_id):
        raise NotImplementedError()

    def latest_prices(self):
        raise NotImplementedError()

    def get_symbol_info(self, symbol):
        raise NotImplementedError()

    def get_account_info(self):
        raise NotImplementedError()

    def get_order_book(self):
        raise NotImplementedError()

    def get_close_price(self, symbol, date):
        raise NotImplementedError()

    def get_klines(self, symbol, interval, **params):
        """查询 K 线数据"""
        raise NotImplementedError()

    def get_historical_trades(self, symbol, limit=500):
        raise NotImplementedError()
