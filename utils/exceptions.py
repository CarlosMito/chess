class NonSquareMatrix(Exception):
    pass


class InvalidMatrix(Exception):
    def __init__(self, message='Given argument is not a matrix'):
        super().__init__(message)


class InvalidSize(Exception):
    def __init__(self, size, message='Both dimensions must be greater than 0'):
        super().__init__(message)
        self.message = message
        self.size = size

    def __str__(self):
        return f'{self.size}: {self.message}'
