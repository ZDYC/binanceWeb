"""币安接口
"""
import logging
from decimal import Decimal
import datetime

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .base import Exchange, exception_haneler
from core.models import Order


log = logging.getLogger(__name__)


class BinanceExchange(Exchange):

    @property
    def client(self):
        if not getattr(self, '_client', None):
            self._client = Client(self.key, self.secret)
        return self._client

    def create_order(self, symbol, side, quantity, price, client_order_id,
                     order_type='LIMIT', time_in_force='GTC',
                     iceberg_qty=0.0, stop_price=None):
        """创建订单
        """
        log.info('stop_price: %s' % stop_price)
        try:
            if order_type == Order.ORDER_TYPE_MARKET:
