import requests
from data import Url

class Order:
    @staticmethod
    def create(body, token=None):
        """Создание заказа"""
        headers = {'Authorization': token} if token else {}
        return requests.post(Url.BASE_URL + Url.ORDERS_URL, json=body, headers=headers)