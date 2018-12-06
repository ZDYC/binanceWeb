import json
import time
import logging

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core.views import rsp, error_rsp


log = logging.getLogger(__name__)


@csrf_exempt
def login_view(request):
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
