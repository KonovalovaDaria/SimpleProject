import csv
from typing import Any

from core.logic import AbstractLogic


class GenerateReportLogic(AbstractLogic):

    def __init__(self, repo):
        self._repo = repo

    def execute(self, *args, **kwargs) -> Any:
        result = self._repo.execute()
        file_path = 'authors_report.csv'
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'first_name'])

            for author in result:
                writer.writerow([author.id, author.first_name])

        return file_path


class CallBackOnCreateLogic(AbstractLogic):
    def execute(self, context, **kwargs) -> Any:
        obj_id = context['id']
        first_name = context['first_name']
        last_name = context['last_name']
        birthday = context['birthday']
        print(f'Created author {obj_id} first_name: {first_name}, last_name: {last_name}, birthday: {birthday}')
        return context


class OnErrorCreateLogic(AbstractLogic):
    def execute(self, context, **kwargs) -> Any:
        first_name = context.get('first_name')
        last_name = context.get('last_name')
        birthday = context.get('birthday')
        print(f'Error create author first_name: {first_name}, last_name: {last_name}, birthday: {birthday}')
        return context
