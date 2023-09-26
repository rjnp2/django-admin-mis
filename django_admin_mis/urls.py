from django.urls import include, path
from rest_framework import routers
from .views import AdminModelViewSet

router = routers.DefaultRouter()

router.register('admin', AdminModelViewSet, 'admin')

app_name = 'admin_mis'
urlpatterns = [
    path('', include(router.urls)),
]

