from datetime import datetime

from django.db import models


class OrderList(models.Model):
    """
    Модель БД для отображения списка заказов
    Содержит номер заказа, стоимость в долларах США, стоимость в российских рублях, срок поставки
    """
    order_id = models.IntegerField(verbose_name="Order ID", default=0.00)
    cost_usd = models.DecimalField(verbose_name="Cost in USD", default=0.00, max_digits=19, decimal_places=3)
    cost_rub = models.DecimalField(verbose_name="Cost in RUB", default=0.00, max_digits=19, decimal_places=3)
    delivery_time = models.DateField(verbose_name="Delivery Time",
                                     default=datetime.strptime('01.01.1970', '%d.%m.%Y').date())
