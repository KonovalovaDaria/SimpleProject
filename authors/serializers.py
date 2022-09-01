"""
Методы сериализации объектов.
Такие сериализаторы взяла для примера.
Можно использовать любые по договоренности.
"""

from django.core import serializers


def obj_serializer(obj):
    return serializers.serialize('json', [obj])


def queryset_serializer(queryset):
    return serializers.serialize('json', queryset)
