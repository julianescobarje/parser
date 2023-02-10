from tokenizer import Token
from helper import Helper
from reserved_words import *


class Verifier:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.helper = Helper()
        self.variables = None

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

    def verifyIncrease(self, actualIndex: int, tokens_length: int, increase: int) -> bool:
        return actualIndex + increase < tokens_length

    def verifyProcs(self, tokens: list[Token]) -> bool:
        if len(tokens) < 5:
            return False

        i = 0
        while i < len(tokens) - 2:
            if tokens[i].getType() != 'STRING':
                return False

            if not self.verifyIncrease(i, len(tokens), 1):
                return False
            i += 1

            if tokens[i].getType() != 'LKEY':
                return False

            if not self.verifyIncrease(i, len(tokens), 1):
                return False
            i += 1

            if tokens[i].getType() != 'PIPE':
                return False

            if not self.verifyIncrease(i, len(tokens), 1):
                return False
            i += 1

            while i < len(tokens) - 1:
                token = tokens[i]
                next_token_type = tokens[i+1].getType()
                if token.getType() != 'STRING' or next_token_type not in ['COMMA', 'PIPE']:
                    return False
                if next_token_type == 'PIPE':
                    break
                i += 2

            if not self.verifyIncrease(i, len(tokens), 2):
                return False
            i += 2

            while i < len(tokens) - 1:
                command = tokens[i].getType()
                print('command:', command)

                if command not in reserved_words:
                    return False

                if not self.verifyIncrease(i, len(tokens), 1):
                    return False
                i += 1

                if tokens[i].getType() != 'COLON':
                    return False

                if not self.verifyIncrease(i, len(tokens), 1):
                    return False
                i += 1

                if command in commands:
                    params = commands[command]
                    params_command = []

                    while i < len(tokens) - 1:
                        token = tokens[i]
                        token_type = token.getType()
                        token_value = token.getValue()
                        next_token_type = tokens[i+1].getType()
                        if next_token_type not in ['COMMA', 'SEMICOLON']:
                            return False
                        if next_token_type == 'SEMICOLON':
                            params_command.append(token)
                            break
                        params_command.append(token)
                        i += 2

                    if len(params_command) != len(params):
                        return False

                    for j in range(len(params)):
                        types_param = params[j]
                        token = params_command[j]

                        found = False

                        if type(types_param) == list:
                            for type_param in types_param:
                                if type_param == 'VARIABLE':
                                    for variable in self.variables:
                                        if variable.getType() == token.getType() and variable.getValue() == token.getValue():
                                            found = True

                                    for variable in params_command:
                                        if variable.getType() == token.getType() and variable.getValue() == token.getValue():
                                            found = True
                                else:
                                    if type_param == token.getType():
                                        found = True
                        else:
                            if types_param == 'VARIABLE':
                                for variable in self.variables:
                                    if variable.getType() == token.getType() and variable.getValue() == token.getValue():
                                        found = True

                                for variable in params_command:
                                    if variable.getType() == token.getType() and variable.getValue() == token.getValue():
                                        found = True
                            else:
                                if types_param == token.getType():
                                    found = True

                        if not found:
                            return False

                if next_token_type != 'SEMICOLON':
                    return False

                i += 2

                if tokens[i].getType() == 'RKEY':
                    break

            if tokens[i].getType() != 'RKEY':
                return False

            i += 1
            print('i3', i)

        return True

    def verifySyntax(self) -> bool:

        if not self.verifyUnique():
            return False

        if self.tokens[0].getType() != 'ROBOT_R':
            return False

        if len(self.tokens) > 1:

            second_token_type = self.tokens[1].getType()

            if second_token_type not in ['VARS', 'PROCS', 'LKEY']:
                return False

            if second_token_type == 'VARS':
                i = 2
                variables = []
                next_token_type = None
                while i < len(self.tokens) - 1:
                    token = self.tokens[i]
                    token_type = token.getType()
                    token_value = token.getValue()
                    next_token_type = self.tokens[i+1].getType()
                    if token_type != 'STRING' or self.helper.isInteger(token_value[:1]) or next_token_type not in ['COMMA', 'SEMICOLON']:
                        return False
                    if next_token_type == 'SEMICOLON':
                        variables.append(token)
                        break
                    variables.append(token)
                    i += 2
                if next_token_type != 'SEMICOLON':
                    return False

                self.variables = variables

                if i + 2 < len(self.tokens):
                    i += 2
                    token_type = self.tokens[i].getType()
                    if token_type not in ['PROCS', 'LKEY']:
                        return False

                    if token_type == 'PROCS':
                        i += 1
                        if not self.verifyProcs(self.tokens[i:]):
                            return False

            elif second_token_type == 'PROCS':
                if not self.verifyProcs(self.tokens[2:]):
                    return False

        return True
