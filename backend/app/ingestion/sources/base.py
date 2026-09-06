from abc import ABC, abstractmethod
from typing import Any


class JobSource(ABC):
    @abstractmethod
    def fetch_data(self) -> Any:
        pass
