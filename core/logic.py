from abc import ABC, abstractmethod
from typing import Any


class AbstractLogic(ABC):
    _repo = None

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass
