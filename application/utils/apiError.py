class ApiError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.is_success = False
        self.status_code = status_code
        self.message = message
