class Result:
    def __init__(self, data=None, error=None):
        self.data = data
        self.error = error

    @classmethod
    def failure(cls, error):
        return cls(error=error)

    @classmethod
    def success(cls, data=None):
        return cls(data=data)

    def is_failure(self):
        return self.error is not None

    def is_success(self):
        return self.error is None
