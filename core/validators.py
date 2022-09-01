"""
Универсальных валидаторы, принемают репо с помощью которой производится проверка.
"""
from django.core.exceptions import ValidationError


class ObjectExistValidator:
    def __init__(self, check_exist_by_id, error_message):
        self._check_exist_by_id = check_exist_by_id
        self._error_message = error_message

    def __call__(self, author_id):
        if not self._check_exist_by_id(author_id):
            raise ValidationError(self._error_message)


class ObjectNotExistValidator:
    def __init__(self, check_exist, error_message, obj_id=None):
        self._check_exist = check_exist
        self._error_message = error_message
        self._obj_id = obj_id

    def __call__(self, **context):
        if self._check_exist(**context, obj_id=self._obj_id):
            raise ValidationError(self._error_message)
