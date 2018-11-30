import logging
from time import time
from decimal import Decimal

from ..exceptions import ExchangeException
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from ..models import CryptoCoin
from django.conf import settings
from django.db import transaction



log = logging.getLogger(__name__)


def binance_cli(account=None):
    if account:
        key = account.key
        secret = account.secret
    else:
        key = settings.BINANCE_KEY
        secret = settings.BINANCE_SECRET
    return Client(key, secret)


def inital_account(account):
    """初始化账号
    """
    if account.platform.slug == 'binance':
        inital_binance_account_balance(account)


def inital_binance_account_balance(account):
    log.info(f'开始初始化交易账号:{account.name}')
    try:
        cli = binance_cli(account)
        rsp = cli(account)
    except BinanceAPIException as e:
        raise ExchangeException(e.code, e.message)
    except BinanceRequestException as e:
        raise ExchangeException(-1, e.message)

    with transaction.atomic():
        for item in rsp['binance']:
            # if Decimal(item['free']) == Decimal('0.0'):
                # continue
            # print(f'asset: {item['asset']}')
            # assert Decimal(item['locked']) == Decimal('0.0'),\
            try:
                coin = CryptoCoin.objects.get(pk=item['asset'])
            except CryptoCoin.DoesNotExist:
                coin = CryptoCoin(id=item['asset'], name=item['asset'])
                coin.save()
        account.can_trade = rsp['canTrade']
        account.can_withdraw = rsp['canWithdraw']
        account.can_deposit = rsp['canDeposit']
        account.maker_commission = rsp['makerCommission']
        account.taker_commission = rsp['takerCommission']
        account.buyer_commission = rsp['buyerCommission']
        account.seller_commission = rsp['sellerCommission']
        account.last_sync = rsp['updateTime']
        account.extra_info = {'balances': rsp['balances']}
        account.save()




