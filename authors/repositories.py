"""
Методы для совершения запросов к базе данных.
Сейчас тут один файл, тк в модуле одна модель.
Но если моделий будет больше, можно для каждой модели создавать отдельный файл.
"""
from authors.models import Author
from core.repository import AbstractRepository


class CheckExistAuthorRepo(AbstractRepository):
    def execute(self, first_name, last_name, birthday, obj_id=None):
        qs = Author.objects.filter(first_name=first_name, last_name=last_name, birthday=birthday)
        if obj_id is not None:
            qs = qs.exclude(id=obj_id)
        return qs.exists()


class CheckExistAuthorByIdRepo(AbstractRepository):
    def execute(self, obj_id):
        return Author.objects.filter(id=obj_id).exists()


class GetAuthorRepo(AbstractRepository):
    def execute(self, author_id):
        return Author.objects.get(id=author_id)


class GetAllAuthorsRepo(AbstractRepository):
    def execute(self):
        return Author.objects.all()


class DeleteAuthorRepo(AbstractRepository):
    def execute(self, author_id):
        return Author.objects.filter(id=author_id).delete()
