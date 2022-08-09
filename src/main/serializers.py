from rest_framework.serializers import HyperlinkedModelSerializer

import main.models as models


class OrderListSerializer(HyperlinkedModelSerializer):
    """
    Сериализатор данных модели OrderList в JSON
    """
    class Meta:
        model = models.OrderList
        fields = '__all__'
