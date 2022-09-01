"""
Методы для совершения запросов к базе данных.
Сейчас тут один файл, тк в модуле одна модель.
Но если моделий будет больше, можно для каждой модели создавать отдельный файл.
"""
from authors.models import Author


def check_exist_author(first_name, last_name, birthday, obj_id=None):
    qs = Author.objects.filter(first_name=first_name, last_name=last_name, birthday=birthday)
    if obj_id is not None:
        qs = qs.exclude(id=obj_id)
    return qs.exists()


def check_exist_author_by_id(obj_id):
    return Author.objects.filter(id=obj_id).exists()


def get_author(author_id):
    return Author.objects.get(id=author_id)


def get_all_authors():
    return Author.objects.all()
