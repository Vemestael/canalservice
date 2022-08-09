from django.contrib import admin

import main.models as models


@admin.register(models.OrderList)
class OrderListAdmin(admin.ModelAdmin):
    """
    Регистрация модели для показа в админ панели Django
    """
    list_display = ('id', 'order_id', 'cost_usd', 'cost_rub', 'delivery_time')
