from mock import Mock

from authors.repositories import CheckExistAuthorRepo


def test__exist__without_author_id(mocker):
    data = {'first_name': 'first_name', 'last_name': 'last_name', 'birthday': 'birthday'}

    queryset = Mock()
    queryset.exists = lambda: True
    mocked = mocker.patch('authors.models.Author.objects.filter', return_value=queryset)
    check_exist_author = CheckExistAuthorRepo()

    assert check_exist_author.execute(**data) is True
    assert mocked.called
    assert mocked.call_args[1] == data


def test__not_exist__without_author_id(mocker):
    data = {'first_name': 'first_name', 'last_name': 'last_name', 'birthday': 'birthday'}

    queryset = Mock()
    queryset.exists = lambda: False
    mocked = mocker.patch('authors.models.Author.objects.filter', return_value=queryset)
    check_exist_author = CheckExistAuthorRepo()

    assert check_exist_author.execute(**data) is False

    assert mocked.called
    assert mocked.call_args[1] == data


def test__exist__with_author_id(mocker):
    data = {'first_name': 'first_name', 'last_name': 'last_name', 'birthday': 'birthday'}

    queryset = Mock()
    queryset.exclude = lambda id: queryset
    queryset.exists = lambda: True

    mocked = mocker.patch('authors.models.Author.objects.filter', return_value=queryset)
    check_exist_author = CheckExistAuthorRepo()

    assert check_exist_author.execute(**data, obj_id='author_id') is True
    assert mocked.called
    assert mocked.call_args[1] == data


def test__not_exist__with_author_id(mocker):
    data = {'first_name': 'first_name', 'last_name': 'last_name', 'birthday': 'birthday'}

    queryset = Mock()
    queryset.exclude = lambda id: queryset
    queryset.exists = lambda: False
    mocked = mocker.patch('authors.models.Author.objects.filter', return_value=queryset)
    check_exist_author = CheckExistAuthorRepo()

    assert check_exist_author.execute(**data, obj_id='author_id') is False

    assert mocked.called
    assert mocked.call_args[1] == data
