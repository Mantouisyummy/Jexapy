class NoDataException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class AuthFailed(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)