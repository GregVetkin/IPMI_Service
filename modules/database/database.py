from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def _close(self):
        pass

    @abstractmethod
    def _execute_query(self, query, params=None):
        pass

    @abstractmethod
    def _fetch_results(self, query, params=None):
        pass

