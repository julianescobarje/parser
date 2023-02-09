from tokenizer import Token


class Verifier:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

    def verifySyntax(self):
        if str(self.tokens[0]) != 'ROBOT_R':
            return False
        return True
