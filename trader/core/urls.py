from django.conf.urls import url
from . views import api, admin


urlpatterns = [
      url(r'^login/$', api.login_view),
      url(r'^logout/$', api.logout_view),
      url(r'^system_status/$', api.system_status_view),

]