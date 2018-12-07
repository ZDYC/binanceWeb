import json
import time
import logging

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import transaction

from core.views import rsp, error_rsp


log = logging.getLogger(__name__)


def index_view(request):
	return rsp('welcome to web of binance')


@csrf_exempt
def login_view(request):
	"""login
	"""
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	if '' in (username, password):
		return error_rsp(5001, 'no name or no password')
	user = authenticate(request, username=username, password=password)
	if not user:
		return error_rsp(5002, 'invalid name or password or can not use!')
	if not user.account:
		return error_rsp(5003, 'no account for this name, can not login!')
	login(request, user)
	return rsp(1)


@csrf_exempt
@login_required
def logout_view(request):
	"""logout
	"""
	logout(request)
	return rsp(1)


@login_required
def system_status_view(request):
	"""system status
	"""
	redis_client = get_redis_connection('default')
	status = 'NORMAL'
	if (redis_client.get('trader:maintaining')):
		status = 'MAINTAINING'
	return rsp({'time': time.time(), 'status': status})


@login_required
def exchange_info(request):
	"""information of platform
	"""
	platform_id = request.user.account.platform_id
	markets = Market.objects.filter(platform_id=platform_id)
	symbols = []
	for market in markets:
		pass


@csrf_exempt
@login_required
def create_order_view(request):
	symbol = request.POST.get('symbol', '').strip().upper()
	order_type = request.POST.get('order_type')
	side = request.POST.get('side', '')
	time_in_force = request.POST.get('time_in_force', '')
	price = request.POST.get('price')
	price = Decimal(price) if price else Dzero
	quantity = request.POST.get('quantity')
	quantity = Decimal(quantity) if quantity else Dzero
	user = request.user
	# local order
	# with transaction.atomic():
	# 	try:
	# 		pass