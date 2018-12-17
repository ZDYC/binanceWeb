import logging

from binance.client import Client

from .. models import Market, CryptoCoin

from django.conf import settings
from django.db import transaction


log = logging.getLogger(__name__)


def binance_client():
    return Client(settings.BINANCE_KEY, settings.BINANCE_SECRET)


@transaction.atomic
def sync_binance_platform_info(platform):
    result = binance_client().get_exchange_info()
    new_symbols = set([])
    symbols = result['symbols']
    # print(symbols)
    for symbol in symbols:
        coin = CryptoCoin.objects.filter(coinId=symbol['baseAsset'])
        if not coin:
            coin = CryptoCoin(coinId=symbol['baseAsset'], name=symbol['baseAsset'])
            coin.save()

        currency = CryptoCoin.objects.filter(coinId=symbol['quoteAsset'])
        if not currency:
            currency = CryptoCoin(coinId=symbol['quoteAsset'],
                                  name=symbol['quoteAsset'])
            currency.save()

        market = Market(
            platform=platform,
            symbol=symbol['symbol'],
            status=symbol['status'],
            coin=symbol['baseAsset'],
            currency=symbol['quoteAsset'],
            order_types='.'.join(symbol['orderTypes']),
            iceberg_allowed=symbol['icebergAllowed'],
            extra_info={'filters': symbol['filters']},
            # last_checksum=new_checksum
        )
        market.save()
        continue
