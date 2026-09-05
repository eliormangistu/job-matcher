from abc import ABC, abstractmethod


class JobSource(ABC):

    @abstractmethod
    def fetch_jobs(self) -> list[dict]:
        pass