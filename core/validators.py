"""
Универсальных валидаторы, принемают репо с помощью которой производится проверка.
"""
from abc import ABC, abstractmethod
from typing import Any

from django.core.exceptions import ValidationError


class AbstractValidator(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass


class ObjectExistValidator(AbstractValidator):

    __slots__ = ('_check_exist_by_id', '_error_message')

    def __init__(self, check_exist_by_id, error_message):
        self._check_exist_by_id = check_exist_by_id
        self._error_message = error_message

    def execute(self, author_id):
        if not self._check_exist_by_id(author_id):
            raise ValidationError(self._error_message)


class ObjectNotExistValidator(AbstractValidator):

    __slots__ = ('_check_exist', '_error_message', '_obj_id')

    def __init__(self, check_exist, error_message, obj_id=None):
        self._check_exist = check_exist
        self._error_message = error_message
        self._obj_id = obj_id

    def execute(self, **context):
        if self._check_exist(**context, obj_id=self._obj_id):
            raise ValidationError(self._error_message)
