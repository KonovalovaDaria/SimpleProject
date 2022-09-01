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

from authors.forms import AuthorForm
from authors.serializers import obj_serializer, queryset_serializer
from authors.repositories import get_author, get_all_authors, check_exist_author_by_id, check_exist_author
from core.services import FormService, Service
from core.validators import ObjectExistValidator, ObjectNotExistValidator


@method_decorator(csrf_exempt, name='dispatch')
class CreateAuthor(View):
    def post(self, request, *args, **kwargs):
        # тут пока не поняла в каком виде обрабатывать входные данные
        context = json.loads(request.body.decode('utf-8'))

        # валидатору говорим с помощью какого репо проверять
        validate_unique_author = ObjectNotExistValidator(
            check_exist=check_exist_author, error_message='Author already exist'
        )

        # форме говорим с помощью какого валидатора валидировать
        form = AuthorForm(context, validate_unique_author=validate_unique_author)

        # сервису говорим с помощью какой формы производить обработку и как сериализовать выходные данные
        service = FormService(form=form, serializer=obj_serializer)
        result = service.execute()

        if service.success:
            return JsonResponse({'success': True, 'result': result}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': service.errors}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateAuthor(View):
    def post(self, request, author_id, *args, **kwargs):
        validator = ObjectExistValidator(check_exist_by_id=check_exist_author_by_id, error_message='Author not exist')

        get_author_service = Service(validator=validator, repo=get_author)
        author = get_author_service.execute({'author_id': author_id})

        if get_author_service.errors:
            return JsonResponse({'success': False, 'errors': get_author_service.errors}, status=200)

        context = json.loads(request.body.decode('utf-8'))
        validate_unique_author = ObjectNotExistValidator(
            check_exist=check_exist_author, error_message='Author already exist', obj_id=author_id
        )
        form = AuthorForm(context, instance=author, validate_unique_author=validate_unique_author)
        service = FormService(form=form, serializer=obj_serializer)
        result = service.execute()

        if service.success:
            return JsonResponse({'success': True, 'result': result}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': service.errors}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class GetAllAuthors(View):
    def get(self, request, *args, **kwargs):
        service = Service(repo=get_all_authors, serializer=queryset_serializer)
        result = service.execute({})

        if service.success:
            return JsonResponse({'success': True, 'result': result}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': service.errors}, status=200)
