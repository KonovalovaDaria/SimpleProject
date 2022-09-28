"""
Обработка запростов.
Представления принимают на вход данные. Отдают данные форме или напрямую сервису.
В результате вьюхи отдаем результат работы сервиса.
"""
import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse

from authors.dto import AuthorDto, AuthorObjDto
from authors.forms import AuthorForm
from authors.logic import GenerateReportLogic, CallBackOnCreateLogic, OnErrorCreateLogic
from authors.serializers import ObjectSerializer, QuerysetSerializer
from authors.repositories import (
    GetAuthorRepo,
    GetAllAuthorsRepo,
    CheckExistAuthorRepo,
    CheckExistAuthorByIdRepo,
    DeleteAuthorRepo,
)
from core.services import FormService, LogicService, RepoService
from core.validators import ObjectExistValidator, ObjectNotExistValidator


@method_decorator(csrf_exempt, name='dispatch')
class Author(View):
    def get(self, request, author_id, *args, **kwargs):
        """Получение."""
        validator = ObjectExistValidator(check_exist_by_id=CheckExistAuthorByIdRepo(), error_message='Author not exist')
        service = RepoService(repo=GetAuthorRepo(), serializer=ObjectSerializer(), validator=validator)
        result = service.execute({'author_id': author_id})

        if service.success:
            return JsonResponse({'success': True, 'result': result}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': service.errors}, status=400)

    def put(self, request, *args, **kwargs):
        """Создание."""
        # тут пока не поняла в каком виде обрабатывать входные данные
        context = json.loads(request.body.decode('utf-8'))

        # валидатору говорим с помощью какого репо проверять
        validate_unique_author = ObjectNotExistValidator(
            check_exist=CheckExistAuthorRepo(), error_message='Author already exist'
        )

        # форме говорим с помощью какого валидатора валидировать
        form = AuthorForm(context, validate_unique_author=validate_unique_author)

        callback = LogicService[AuthorObjDto, AuthorObjDto](logic=CallBackOnCreateLogic())
        on_error = LogicService[AuthorDto, AuthorDto](logic=OnErrorCreateLogic())

        # сервису говорим с помощью какой формы производить обработку и как сериализовать выходные данные
        service = FormService[AuthorDto, AuthorObjDto](
            form=form, serializer=ObjectSerializer(), call_back=callback, on_error=on_error
        )
        result = service.execute()

        if service.success:
            response = JsonResponse({'success': True, 'result': result}, status=201)
            response['Location'] = reverse('authors:author', kwargs={'author_id': result['id']})
            return response
        else:
            return JsonResponse({'success': False, 'errors': service.errors}, status=400)

    def post(self, request, author_id, *args, **kwargs):
        """Обновление."""
        validator = ObjectExistValidator(check_exist_by_id=CheckExistAuthorByIdRepo(), error_message='Author not exist')

        get_author_service = RepoService(validator=validator, repo=GetAuthorRepo())
        author = get_author_service.execute({'author_id': author_id})

        if get_author_service.errors:
            return JsonResponse({'success': False, 'errors': get_author_service.errors}, status=400)

        context = json.loads(request.body.decode('utf-8'))
        validate_unique_author = ObjectNotExistValidator(
            check_exist=CheckExistAuthorRepo(), error_message='Author already exist', obj_id=author_id
        )
        form = AuthorForm(context, instance=author, validate_unique_author=validate_unique_author)
        service = FormService(form=form, serializer=ObjectSerializer())
        result = service.execute()

        if service.success:
            return JsonResponse({'success': True, 'result': result}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': service.errors}, status=400)

    def delete(self, request, author_id, *args, **kwargs):
        """Удаление."""
        validator = ObjectExistValidator(check_exist_by_id=CheckExistAuthorByIdRepo(), error_message='Author not exist')

        delete_author_service = RepoService(validator=validator, repo=DeleteAuthorRepo())
        delete_author_service.execute({'author_id': author_id})

        if delete_author_service.success:
            return JsonResponse({'success': True, 'result': None}, status=204)
        else:
            return JsonResponse({'success': False, 'errors': delete_author_service.errors}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class GetAllAuthors(View):
    def get(self, request, *args, **kwargs):
        service = RepoService(repo=GetAllAuthorsRepo(), serializer=QuerysetSerializer())
        result = service.execute({})

        if service.success:
            return JsonResponse({'success': True, 'result': result}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': service.errors}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class GetAuthorsReport(View):
    def get(self, request, *args, **kwargs):
        service = LogicService(logic=GenerateReportLogic(repo=GetAllAuthorsRepo()))
        result = service.execute({})

        if service.success:
            return JsonResponse({'success': True, 'result': result}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': service.errors}, status=400)
