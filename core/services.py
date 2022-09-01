"""
Для примера представлено 2 сервиса.
Один работает напрямую с валидатором, данными и репо.
Второй работает через форму.
"""
from django.core.exceptions import ValidationError


class Service:
    _success = None
    _errors = None

    def __init__(self, validator=None, repo=None, serializer=None):
        self._repo = repo
        self._validator = validator
        self._serializer = serializer

    def execute(self, context, **kwargs):
        try:
            if self._validator:
                self._validator(**context)
        except ValidationError as ex:
            self._success = False
            self._errors = ex.messages
        else:
            self._success = True
            if self._repo:
                result = self._repo(**context)
                if self._serializer:
                    return self._serializer(result)
                return result

    @property
    def success(self):
        return self._success

    @property
    def errors(self):
        return self._errors


class FormService:
    _success = None
    _errors = None

    def __init__(self, form, serializer=None):
        self._form = form
        self._serializer = serializer

    def execute(self, **kwargs):
        if self._form.is_valid():
            self._success = True
            result = self._form.save()
            if self._serializer:
                return self._serializer(result)
            return result
        else:
            self._success = False
            self._errors = self._form.errors

    @property
    def success(self):
        return self._success

    @property
    def errors(self):
        return self._errors
