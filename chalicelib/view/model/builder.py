from chalicelib.view.model.api import Api


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
