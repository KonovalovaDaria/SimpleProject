from django.core.exceptions import ValidationError
from mock import Mock
import pytest

from authors.forms import AuthorForm


def test__clean__has_not_errors__valid():
    data = {'first_name': 'first_name_test', 'last_name': 'last_name_test', 'birthday': '2020-02-02'}
    form = AuthorForm(data, validate_unique_author=Mock())
    form._errors = {}
    form.cleaned_data = data

    assert form.clean() == data


def test__clean__has_not_errors__not_valid():
    data = {'first_name': 'first_name_test', 'last_name': 'last_name_test', 'birthday': '2020-02-02'}
    form = AuthorForm(data, validate_unique_author=Mock(side_effect=ValidationError('error')))
    form._errors = {}
    form.cleaned_data = data

    with pytest.raises(ValidationError):
        form.clean()


def test__clean__has_not_validator():
    data = {'first_name': 'first_name_test', 'last_name': 'last_name_test', 'birthday': '2020-02-02'}
    form = AuthorForm(data)
    form._errors = {}
    form.cleaned_data = data

    assert form.clean() == data


def test__clean__has_errors():
    data = {'first_name': 'first_name_test', 'last_name': 'last_name_test', 'birthday': '2020-02-02'}
    form = AuthorForm(data, validate_unique_author=Mock(side_effect=ValidationError('error')))
    form._errors = {'first_name': 'error'}
    form.cleaned_data = data

    assert form.clean() == data
