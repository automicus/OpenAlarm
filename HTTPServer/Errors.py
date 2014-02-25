class HTTP404(Exception):
    def __init__(self):
        super(HTTP404, self).__init__()
        self.code = 404

    def __str__(self):
        return "404: Page Not Found"

    def __repr__(self):
        return self.__str__()
