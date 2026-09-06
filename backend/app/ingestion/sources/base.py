from abc import ABC, abstractmethod


class JobSource(ABC):
    @abstractmethod
    def fetch_data(self) -> dict:
        pass
