# type: ignore


class BaseError(Exception):
    def __init__(self, *args, context=None) -> None:
        super().__init__(*args)
        self.context = context


class APIError(Exception):
    def __init__(self, text, response) -> None:
        self.text = text
        self.response = response
