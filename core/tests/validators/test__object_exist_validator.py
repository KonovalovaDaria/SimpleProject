from django.core.exceptions import ValidationError
from mock import Mock
import pytest

from core.validators import ObjectExistValidator


def test__exist():
    validator = ObjectExistValidator(check_exist_by_id=Mock(execute=lambda a_id: True), error_message='')
    assert validator('author_id') is None


def test__not_exist():
    error_message = 'error_message'
    validator = ObjectExistValidator(check_exist_by_id=Mock(execute=lambda a_id: False), error_message=error_message)
    with pytest.raises(ValidationError) as ex:
        validator('author_id')
    assert ex.value.message == error_message
