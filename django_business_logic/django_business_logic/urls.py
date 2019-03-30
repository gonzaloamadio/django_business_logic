from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers


# django rest framework router
router = routers.DefaultRouter()
# end of django rest framework router

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
]
