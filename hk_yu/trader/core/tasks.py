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
    log.info(f'将启动id为{account_id}的websocket进程')
    account = Account.objects.get(pk=account_id)
    if account.platform.slug == 'binance':
        start_binance_ws_process(account)
    else:
        raise Exception(f'exchange {account.platform.slug} not support yet')


def start_binance_ws_process(account):
    pass
