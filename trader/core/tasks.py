import logging
import os
import time

from binance.client import Client
from celery import shared_task

from django.conf import settings
from core.models import Platform, CryptoCoin, Account
from core.services import platform as services_platform

from django_redis import get_redis_connection
from fabric import Connection

log = logging.getLogger(__name__)


@shared_task
def sync_binance_exchange_info():
    """update information of binance"""
    binance = Platform.objects.get(slug='binance')
    services_platform.sync_binance_platform_info(binance)


@shared_task
def start_ws_process(account_id):
    """启动账号对应的websocket进程"""
    log.info('将启动id为%s的websocket进程' % account_id)
    account = Account.objects.get(pk=account_id)
    if account.platform.slug == 'binance':
        start_binance_ws_process(account)
    else:
        raise Exception('exchange not support yet')


@shared_task
def remove_ws_process(account_id):
	account = Account.objects.get(pk=account_id)
	if account.platform.slug == 'binance':
		remove_binance_ws_process(account)
	else:
		raise Exception('exchange %s not support yet' % account.platform.slug)

def start_binance_ws_process(account):
    conn = Connection(
    	'localhost',
    	connect_kwargs={'key_filename': 'src/keys/root_id'})
    result = conn.run('supervisorctl status')
    processes = result.stdout.split('\n')
    running = False
    name = account.name
    for pro in processes:
    	log.info(pro)
    	if 'binance_account_socket_%s' % name in pro:
    		log.info('%s progaming is running, no add yet!' % name)
    		running = True
    		break
    	if running:
    		return
    	log.info('perparing to add a new config_file for run websocket progaming for %s! ' % name)

    	# tpl = """"""

    	# df = '/etc/supervisor/conf.d/binance_account_socket_%s.conf' % name
    	# tmp_file = 'socket_%s.conf' % name
     #    with open('tmp_file', 'w') as sf:
     #    	sf.write(tpl)
     #    # log.info('template file path')
     #    conn.put(os.path.abspath(tmp_file), df)
     #    os.remove(tmp_file)
     #    conn.run('supervisorctl update')

     #    conn.close()
     #    log.info('%s websocket is running!' % name)


def remove_binance_ws_process(account):
	df = '/etc/supervisor/conf.d/binance_account_socket_%s.conf' % account.name
	if not os.path.exists(df):
		log.info('no found the conf of supervisor, is over!')
	os.remove(df)
	conn = Connection(
		'localhost',
		connect_kwargs={'key_filename': '/src/keys/root_id'})
	con.run('supervisorctl update')
	conn.close()
	log.info('%s websocket process is removed' % account.name)