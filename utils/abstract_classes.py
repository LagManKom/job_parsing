from abc import ABC, abstractmethod


class WorkingAPI(ABC):
    @abstractmethod
    def get_vacancies(self, profession):
        pass

    @abstractmethod
    def get_request(self):
        pass


class FormattedVacancies(WorkingAPI):

    @abstractmethod
    def get_formatted_vacancies(self):
        pass
