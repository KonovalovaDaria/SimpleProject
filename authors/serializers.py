"""
Методы сериализации объектов.
Такие сериализаторы взяла для примера.
Можно использовать любые по договоренности.
"""
from django.core import serializers

from core.serializers import AbstractSerializer


class ObjectSerializer(AbstractSerializer):
    def execute(self, obj):
        return serializers.serialize('json', [obj])


class QuerysetSerializer(AbstractSerializer):
    def execute(self, queryset):
        return serializers.serialize('json', queryset)
