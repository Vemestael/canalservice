from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from main import models, serializers


class OrderListAPI(ModelViewSet):
    """
    Rest API для взаимодействия с моделью OrderList
    Имеет ограничение только на чтение для неавторизованных пользователе
    Предоставляет поиск по полю "Номер заказа"
    Предоставляет фильтрацию по полям "Стоимость в долларах США, Стоимость в российских рублях и Срок поставки"
    """
    queryset = models.OrderList.objects.all()
    serializer_class = serializers.OrderListSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['cost_usd', 'cost_rub', 'delivery_time']
    search_fields = ['order_id']
