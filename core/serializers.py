from abc import ABC, abstractmethod
from typing import Any


class AbstractSerializer(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass
