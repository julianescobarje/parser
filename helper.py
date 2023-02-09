class Helper:
    def isInteger(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def isFloat(self, string: str) -> bool:
        try:
            float(string)
            return True
        except ValueError:
            return False
