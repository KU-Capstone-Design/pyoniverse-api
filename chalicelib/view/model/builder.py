from chalicelib.view.model.api import Api
from chalicelib.view.model.pagination import Pagination


class ApiBuilder:
    def __init__(self):
        self._status_code = None
        self._status_message = None
        self._data = None

    def with_status_code(self, status_code: str):
        self._status_code = status_code
        return self

    def with_status_message(self, status_message: str):
        self._status_message = status_message
        return self

    def with_data(self, data: dict):
        self._data = data
        return self

    def build(self):
        return Api(
            status_code=self._status_code,
            status_message=self._status_message,
            data=self._data,
        )


class PaginationBuilder:
    def __init__(self):
        self._page = None
        self._size = None
        self._total_size = None
        self._total_page = None
        self._sort = None
        self._direction = None
        self._filter = None

    def with_page(self, page: int):
        self._page = page
        return self

    def with_size(self, size: int):
        self._size = size
        return self

    def with_total_size(self, total_size: int):
        self._total_size = total_size
        return self

    def with_total_page(self, total_page: int):
        self._total_page = total_page
        return self

    def with_sort(self, sort: str):
        self._sort = sort
        return self

    def with_direction(self, direction: str):
        self._direction = direction
        return self

    def with_filter(self, filter: str):
        self._filter = filter
        return self

    def build(self):
        return Pagination(
            page=self._page,
            size=self._size,
            total_size=self._total_size,
            total_page=self._total_page,
            sort=self._sort,
            direction=self._direction,
            filter=self._filter,
        )
