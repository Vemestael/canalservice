from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
]
urlpatterns += router.urls
