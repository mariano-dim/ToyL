class SymbolsWrapper:

    def __init__(self, name, type=None, value=None, location=None):
        self.name = name
        self.type = type
        self.value = value
        self.location = location

    def set_name(self, name):
        self.name = name

    def set_value(self, value):
        self.value = value

    def set_type(self, type):
        self.type = type

    def set_location(self, location):
        self.location = location

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_location(self):
        return self.location
