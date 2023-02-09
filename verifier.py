from tokenizer import Token


class Verifier:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

    def verifyUnique(self) -> bool:
        unique_token_types = {'ROBOT_R', 'VARS', 'PROCS'}
        seen_token_types = set()

        for token in self.tokens:
            token_type = token.getType()
            if token_type in seen_token_types:
                return False
            if token_type not in unique_token_types:
                continue
            seen_token_types.add(token_type)

        return True

    def verifySyntax(self) -> bool:

        if not self.verifyUnique():
            return False

        if self.tokens[0].getType() != 'ROBOT_R':
            return False

        if len(self.tokens) > 1:
            pass

        return True
