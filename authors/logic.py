import csv
from typing import Any

from core.logic import AbstractLogic


def example_func(author_id):
    return f'my id: {author_id}'


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
