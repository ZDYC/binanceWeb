from django.conf.urls import url

from core.views import api

from core.views import admin


urlpatterns = [
    # url(r'', api.index_view),
    url(r'^login/$', api.login_view),
    url(r'^logout/$', api.logout_view),
    url(r'^system_status/$', api.system_status_view),
    url(r'^create_order/$', api.create_order_view)
]