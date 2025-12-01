"""Абстрактные классы"""

from abc import ABC, abstractmethod
from typing import Any

class Parser[TInput, TOutput](ABC):
    """Абстрактный парсер"""

    @abstractmethod
    def parse(
        self,
        obj: TInput,
        **kwargs: Any
    ) -> TOutput:
        """Парсит объект

        :param obj: объект, который нужно распарсить.
        :param kwargs: дополнительные параметры.

        :return: распаршенный объект.
        """
