from django.conf.urls import url
from . views import api, admin


urlpatterns = [
      url(r'^login$', api.login_view),
]