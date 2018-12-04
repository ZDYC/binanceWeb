import logging
import os
import time

from binance.client import Client
from celery import shared_task

from django.conf import settings
from core.models import Platform, CryptoCoin, Account

log = logging.getLogger(__name__)


@shared_task
def sync_binance_exchange_info():
    binance = Platform.objects.get(slug='binance')


@shared_task
def start_ws_process(account_id):
    """启动账号对应的websocket进程"""
    log.info('将启动id为%s的websocket进程' % account_id)
    account = Account.objects.get(pk=account_id)
    if account.platform.slug == 'binance':
        start_binance_ws_process(account)
    else:
        raise Exception('exchange not support yet')


def start_binance_ws_process(account):
    pass
