class JobNotFoundException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class GeminiException(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code
