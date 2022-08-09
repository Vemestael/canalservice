from django.urls import path, include
from rest_framework import routers

from main import views

router = routers.DefaultRouter()
router.register(r'order-list', views.OrderListAPI)
urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
]
urlpatterns += router.urls
