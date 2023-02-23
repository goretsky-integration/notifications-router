class ApplicationError(Exception):
    pass


class TelegramAPIError(Exception):

    def __init__(self, error_description):
        super().__init__(error_description)
        self.error_description = error_description
