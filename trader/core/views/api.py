import json
import time
import logging

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


log = logging.getLogger(__name__)


@csrf_exempt
def login_view(request):
	name = request.POST.get('name', '')
	password = request.POST.get('password', '')
	if '' in (name, password):
		return error_rsp(5001, 'no name or no password')
	user = authenticate(request, name='name', password='password')
	if not user:
		return error_rsp(5002, 'invalid name or password or can not use!')
	if not.user.account:
		return error_rsp(5003, 'no account for this name, can not login!')
	login(request, user)
	return rsp(1)
