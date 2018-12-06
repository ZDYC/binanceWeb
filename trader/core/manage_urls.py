from rest_framework.routers import DefaultRouter

from . views import admin, manage


router = DefaultRouter()
router.register(r'trader', manage.TraderViewSet, base_name='trader')


urlpatterns = [
    url(r'^admin/login/$', admin.login_view())
]