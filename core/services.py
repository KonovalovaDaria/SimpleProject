"""
Для примера представлено 2 сервиса.
Один работает напрямую с валидатором, данными и репо.
Второй работает через форму.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional

from django.core.exceptions import ValidationError

from core.logic import AbstractLogic
from core.repository import AbstractRepository
from core.serializers import AbstractSerializer
from core.validators import AbstractValidator


class IServiceExecutable(ABC):
    _success = None
    _errors = None

    @abstractmethod
    def execute(self, context: Any, **kwargs) -> Any:
        pass

    @property
    def success(self) -> Optional[bool]:
        return self._success

    @property
    def errors(self) -> Any:
        return self._errors


class AbstractService(IServiceExecutable, ABC):
    """Абстрактный сервис."""

    def __init__(
        self,
        validator: Optional[AbstractValidator] = None,
        repo: Optional[AbstractRepository] = None,
        form: Optional[ABC] = None,
        logic: Optional[AbstractLogic] = None,
        serializer: Optional[AbstractSerializer] = None,
        call_back: Optional[IServiceExecutable] = None,
        on_error: Optional[IServiceExecutable] = None,
    ):
        self._validator = validator
        self._repo = repo
        self._form = form
        self._logic = logic
        self._serializer = serializer
        self._call_back = call_back
        self._on_error = on_error


class RepoService(AbstractService, ABC):

    __slots__ = ('_validator', '_repo', '_serializer', '_call_back', '_on_error')

    def __init__(self, *args, **kwargs):
        super(RepoService, self).__init__(*args, **kwargs)

        if not self._repo:
            raise TypeError('repo is required')

    def execute(self, context, **kwargs):
        try:
            if self._validator:
                self._validator.execute(**context)
        except ValidationError as ex:
            self._success = False
            self._errors = ex.messages
        else:
            self._success = True
            result = self._repo.execute(**context)
            if self._serializer:
                return self._serializer.execute(result)
            return result


class LogicService(AbstractService, ABC):

    __slots__ = ('_validator', '_logic', '_serializer', '_call_back', '_on_error')

    def __init__(self, *args, **kwargs):
        super(LogicService, self).__init__(*args, **kwargs)

        if not self._logic:
            raise TypeError('logic is required')

    def execute(self, context, **kwargs):
        try:
            if self._validator:
                self._validator.execute(**context)
        except ValidationError as ex:
            self._success = False
            self._errors = ex.messages
        else:
            self._success = True
            result = self._logic.execute(**context)
            if self._serializer:
                return self._serializer.execute(result)
            return result


class FormService(AbstractService, ABC):

    __slots__ = ('_validator', '_form', '_serializer', '_call_back', '_on_error')

    def __init__(self, *args, **kwargs):
        super(FormService, self).__init__(*args, **kwargs)

        if not self._form:
            raise TypeError('form required')

    def execute(self, **kwargs):
        if self._form.is_valid():
            self._success = True
            result = self._form.save()
            if self._serializer:
                return self._serializer.execute(result)
            return result
        else:
            self._success = False
            self._errors = self._form.errors
