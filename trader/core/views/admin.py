from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import logging

log = logging.getLogger(__name__)


@csrf_exempt
def login_view(request):
	pass
