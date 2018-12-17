from django.http import HttpResponse


def index(request):
	return HttpResponse("Weclome to dennis's web of binance!")