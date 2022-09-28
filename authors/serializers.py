"""
Методы сериализации объектов.
Такие сериализаторы взяла для примера.
Можно использовать любые по договоренности.
"""
from core.serializers import AbstractSerializer


class ObjectSerializer(AbstractSerializer):
    def execute(self, obj):
        return {
            'id': obj.id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'birthday': obj.birthday,
        }


class QuerysetSerializer(AbstractSerializer):
    def execute(self, queryset):
        return [{
            'id': obj.id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'birthday': obj.birthday,
        } for obj in queryset]
