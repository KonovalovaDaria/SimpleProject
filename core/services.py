"""
Для примера представлено 2 сервиса.
Один работает напрямую с валидатором, данными и репо.
Второй работает через форму.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional, TypeVar, Generic

from django.core.exceptions import ValidationError

from core.logic import AbstractLogic
from core.repository import AbstractRepository
from core.serializers import AbstractSerializer
from core.validators import AbstractValidator


CONTEXT = TypeVar('CONTEXT')
DATASTRUCTURE = TypeVar('DATASTRUCTURE')


class IServiceExecutable(ABC):
    _success = None
    _errors = None
    _result = None

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


class RepoService(Generic[CONTEXT, DATASTRUCTURE], AbstractService, ABC):

    __slots__ = (
        '_success',
        '_errors',
        '_result',
        '_validator',
        '_repo',
        '_serializer',
        '_call_back',
        '_on_error',
        '_parent',
    )

    def __init__(self, *args, **kwargs):
        super(RepoService, self).__init__(*args, **kwargs)

        if not self._repo:
            raise TypeError('repo is required')

    def execute(self, context: CONTEXT, **kwargs) -> DATASTRUCTURE:
        try:
            if self._validator:
                self._validator.execute(**context)
        except ValidationError as ex:
            self._success = False
            self._errors = ex.messages
            if self._on_error:
                self._on_error.execute(context=context, **kwargs)
        else:
            self._success = True
            self._errors = None
            self._result = self._repo.execute(**context)
            if self._serializer:
                self._result = self._serializer.execute(self._result)
            if self._call_back:
                self._call_back.execute(context=self._result, **kwargs)
            return self._result


class LogicService(Generic[CONTEXT, DATASTRUCTURE], AbstractService, ABC):

    __slots__ = (
        '_success',
        '_errors',
        '_result',
        '_validator',
        '_logic',
        '_serializer',
        '_call_back',
        '_on_error',
        '_parent',
    )

    def __init__(self, *args, **kwargs):
        super(LogicService, self).__init__(*args, **kwargs)

        if not self._logic:
            raise TypeError('logic is required')

    def execute(self, context: CONTEXT, **kwargs) -> DATASTRUCTURE:
        try:
            if self._validator:
                self._validator.execute(**context)
        except ValidationError as ex:
            self._success = False
            self._errors = ex.messages
            if self._on_error:
                self._on_error.execute(context=context, **kwargs)
        else:
            self._success = True
            self._errors = None
            self._result = self._logic.execute(context=context)
            if self._serializer:
                self._result = self._serializer.execute(self._result)
            if self._call_back:
                self._call_back.execute(context=self._result, **kwargs)
            return self._result


class FormService(Generic[CONTEXT, DATASTRUCTURE], AbstractService, ABC):

    __slots__ = (
        '_success',
        '_errors',
        '_result',
        '_validator',
        '_form',
        '_serializer',
        '_call_back',
        '_on_error',
        '_parent',
    )

    def __init__(self, *args, **kwargs):
        super(FormService, self).__init__(*args, **kwargs)

        if not self._form:
            raise TypeError('form required')

    def execute(self, **kwargs) -> DATASTRUCTURE:
        if self._form.is_valid():
            self._success = True
            self._errors = None
            self._result = self._form.save()
            if self._serializer:
                self._result = self._serializer.execute(self._result)
            if self._call_back:
                self._call_back.execute(context=self._result, **kwargs)
            return self._result
        else:
            self._success = False
            self._errors = self._form.errors
            if self._on_error:
                self._on_error.execute(context=self._form.data, **kwargs)
