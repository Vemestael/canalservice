import json
import os.path
from datetime import datetime

import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from cbrf.models import DailyCurrenciesRates

from config.settings import BASE_DIR
from main import models, serializers


@method_decorator(csrf_exempt, name='dispatch')
class GSheetsAPI(View):
    """
    Класс предоставляет API для работы с Google Sheets
    """

    # Авторизация и инициализация Google Sheets API
    CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credits.json')
    spreadsheet_id = '1NALt6qqAdDEoGBq3jAXlqV9kjj8wE4qs27qq009xNh4'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Получает актуальные данные о курсе доллара США через API ЦБР
    currency_rate = DailyCurrenciesRates().get_by_id('R01235').value

    def get_sheet_data(self):
        """
        Выполняет запрос к Google Sheets Api для получения всех данных из листа
        Возвращает кортеж данных по строкам листа
        """
        sheet_data = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range='A2:D',
                                                              majorDimension='ROWS', ).execute()
        return tuple(sheet_data['values'])

    def update_data_in_db(self, sheet_row):
        """
        При вызове функции обновляются или добовляются записи в бд
        """
        _id = int(sheet_row[0])
        updated_values = {'order_id': int(sheet_row[1]), 'cost_usd': float(sheet_row[2]),
                          'cost_rub': float(sheet_row[2]) * float(self.currency_rate),
                          'delivery_time': datetime.strptime(sheet_row[3], '%d.%m.%Y').date()}
        models.OrderList.objects.update_or_create(id=_id, defaults=updated_values)

    def get(self, request):
        """
        При вызове выполняется ручной запрос к Google Sheets Api и добавляет/обновляет данные в БД
        Возвращает перенаправление на API таблицы БД для просмотра данных
        """
        sheet_data = self.get_sheet_data()

        last_id_in_db = models.OrderList.objects.last()
        # Если существуют записи в таблице, получить id последней
        if last_id_in_db:
            last_id_in_db = last_id_in_db.id
        else:
            last_id_in_db = 0
        request_len = len(sheet_data)

        if last_id_in_db > request_len:
            counter = 0
            for _id in range(1, last_id_in_db):
                # если в запросе существует строка с таким id, то обновить запись, и перейти к следующей строке запроса
                if int(sheet_data[counter][0]) == _id:
                    self.update_data_in_db(sheet_data[counter])
                    counter += 1
                # если в запросе не существует строки с таким id и существует запись в бд, удалить её
                else:
                    order_obj = models.OrderList.objects.filter(id=_id)
                    if order_obj:
                        order_obj.delete()
                    # если записи не существует, просто продолжить выполнение кода
                    else:
                        continue
        # если длина запроса больше чем id последней записи в бд, то обновить/добавить данные в бд
        else:
            for sheet_row in sheet_data:
                self.update_data_in_db(sheet_row)
        return redirect('/order-list')

    def post(self, request):
        """
        Веб-хук, который принимает изменившуюся строку и обновляет данные в БД
        Возвращает код ответа статуса 204 No Content
        Веб-хук работает через Google Drive API, отслеживая изменение файла
        """

        """Сервис, через который настраиваются веб-хуки, присылает каждую измененную строку отдельным запросом,
        поэтому проанализировать данные на предмет удаленных строк не возможно, в таком случает вызывается get метод
        который анализирует весь набор данных"""
        values = json.loads(request.body)
        if (int(values['row_id']) - 1) != int(values['id']):
            self.get('')
        else:
            updated_values = {'order_id': int(values['order_id']), 'cost_usd': float(values['cost_usd']),
                              'cost_rub': float(values['cost_usd']) * float(self.currency_rate),
                              'delivery_time': datetime.strptime(values['delivery_time'], '%d.%m.%Y').date()}
            models.OrderList.objects.update_or_create(id=values['id'], defaults=updated_values)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class OrderListAPI(ModelViewSet):
    """
    Rest API для взаимодействия с моделью OrderList
    Имеет ограничение только на чтение для неавторизованных пользователей
    Предоставляет поиск по полю "order_id"
    Предоставляет фильтрацию по полям "cost_usd", "cost_rub" и "delivery_time"
    """
    queryset = models.OrderList.objects.all()
    serializer_class = serializers.OrderListSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['cost_usd', 'cost_rub', 'delivery_time']
    search_fields = ['order_id']
