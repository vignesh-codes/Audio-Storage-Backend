class api_dto:

    def __init__(self, output):
        self.output = output

    def success(self):
        return {"code": 200,
                "status": "success",
                "output": self.output}

    def clientError(self):
        return {"code": 400,
                "status": "error",
                "message": "Bad Request",
                "output": self.output}

    def serverError(self):
        return {"code": 500,
                "status": "error",
                "message": "Server Error",
                "output": self.output}

    