import json
from django.http import HttpResponse


# class ExtendJSONEncoder(json.JSONEncoder):
	# def default(self, db):
	# 	try:
	# 		return c


def rsp(data):
	"""normal response
	"""
	return HttpResponse(
		content=json.dumps({
			"errno": 0,
			'data': data},))
		# content_type='application/json')
	# )


def error_rsp(code, message):
	"""error resqonse
	"""
	return HttpResponse(
		content=json.dumps({
			'errno': code,
			'message': message
			}),
		content_type='application/json'
	)