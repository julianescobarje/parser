class Token:
    def __init__(self, type_: str, value):
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

    def getType(self) -> str:
        return self.type

    def getValue(self) -> str:
        return self.value
