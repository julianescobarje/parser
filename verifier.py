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

    def isADeclaredVar(self, token: Token, procedure_vars: list[Token]) -> bool:
        return any(variable.getType() == token.getType() and variable.getValue() == token.getValue()
                   for variable in self.variables + procedure_vars)

    def verifyControlStructures(self, i: int, tokens: list[Token], additional_vars: list[Token]) -> bool:
        print('verifyControlStructure')
        control_structure_token_type = tokens[i].getType()

        if control_structure_token_type not in control_structures:
            return False

        i += 1

        colon_token_type = tokens[i].getType()

        if colon_token_type != 'COLON':
            return False

        i += 1

        syntax_structure_control = control_structures[control_structure_token_type]

        for elem in syntax_structure_control:
            print(elem, tokens[i-2:i+3])
            if type(elem) == list:
                found = False

                for posible_param in elem:
                    if posible_param == 'VARIABLE' and self.isADeclaredVar(tokens[i], additional_vars):
                        found = True
                        break

                    if posible_param == tokens[i].getType():
                        found = True
                        break

                if not found:
                    return False
            elif elem == 'CONDITION':
                result = self.verifyCommandOrCondition(
                    i, tokens, 'condition', additional_vars)
                if result:
                    i = result - 1
                    print(elem, tokens[i-2:i+3])
                else:
                    return False
            elif elem == 'BLOCK':
                print(elem, tokens[i-2:i+3])
                result = self.verifyBlock(i, tokens, False)
                print('result:', result)
                if result:
                    i = result
                else:
                    return False
            else:
                if elem != tokens[i].getType():
                    return False
                i += 1

    def verifyProcs(self, tokens: list[Token]) -> bool:
        print('verifyProcs')
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

            if tokens[i].getType() != 'PIPE':
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
            else:
                i += 1

            while i < len(tokens) - 1:
                command = tokens[i].getType()

                if command in commands:
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
                        next_token_type = tokens[i+1].getType()
                        if next_token_type not in ['COMMA', 'SEMICOLON', 'RKEY']:
                            return False
                        if next_token_type in ['SEMICOLON', 'RKEY']:
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
                elif command in control_structures:
                    self.verifyControlStructures(i, command)

                else:
                    return False

                if next_token_type not in ['SEMICOLON', 'RKEY']:
                    return False

                i += 1

                if tokens[i].getType() == 'RKEY':
                    break
                elif tokens[i].getType() == 'SEMICOLON':
                    i += 1

            if tokens[i].getType() != 'RKEY':
                return False

            i += 1

        return True

    def verifyBlock(self, i: int, tokens: list[Token], procedure: bool) -> bool:
        print('verifyBlock')
        lkey_token_type = tokens[i].getType()

        if lkey_token_type != 'LKEY':
            return False

        i += 1

        if procedure:
            if tokens[i].getType() != 'PIPE':
                return False

            i += 1

            procedure_params = []

            if tokens[i].getType() != 'PIPE':
                while i < len(tokens) - 1:
                    token = tokens[i]
                    next_token_type = tokens[i+1].getType()
                    if token.getType() != 'STRING' or next_token_type not in ['COMMA', 'PIPE']:
                        return False
                    procedure_params.append(token)
                    if next_token_type == 'PIPE':
                        break
                    i += 2
                i += 2
            else:
                i += 1

        additional_vars = [] if not procedure else procedure_params

        token_type = tokens[i].getType()

        while tokens[i-1].getType() != 'RKEY':
            if token_type in commands:
                result = self.verifyCommandOrCondition(
                    i, tokens, 'command', additional_vars)
                if result:
                    i = result
                else:
                    return False
            elif token_type in control_structures:
                result = self.verifyControlStructures(
                    i, tokens, additional_vars)
                if result:
                    i = result
                else:
                    return False
            else:
                return False

            if tokens[i-1].getType() not in ['SEMICOLON', 'RKEY']:
                return False

            token_type = tokens[i].getType()

        return i

    def verifyCommandOrCondition(self, i: int, tokens: list[Token], type_call: str, additional_vars: list[Token]) -> bool:
        print('verifyCommandOrCondition')

        dictionary = {
            'command': commands,
            'condition': conditions
        }

        condition_token_type = tokens[i].getType()

        if condition_token_type not in dictionary[type_call]:
            return False

        i += 1

        colon_token_type = tokens[i].getType()

        if colon_token_type != 'COLON':
            return False

        i += 1

        params_condition = dictionary[type_call][condition_token_type]
        params_given = []

        while len(params_given) != len(params_condition):
            token = tokens[i]
            next_token_type = tokens[i+1].getType()
            if next_token_type not in ['COMMA', 'SEMICOLON', 'RKEY', 'DO']:
                return False
            params_given.append(token)
            i += 2

        for j in range(len(params_condition)):
            param = params_condition[j]
            param_given = params_given[j]

            if type(param) == list:

                found = False

                for posible_param in param:
                    if posible_param == 'VARIABLE' and self.isADeclaredVar(param_given, additional_vars):
                        found = True
                        break

                    if posible_param == param_given.getType():
                        found = True
                        break

                if not found:
                    return False

            elif param == 'CONDITION':
                if not self.verifyCommandOrCondition(i, tokens, 'condition'):
                    return False

            elif param == 'VARIABLE':
                if not self.isADeclaredVar(param_given, additional_vars):
                    return False

            else:
                if param != param_given.getType():
                    return False

        return i

    def verifyProcs(self, tokens: list[Token]) -> bool:
        if len(tokens) < 5:
            return False

        i = 0
        while i < len(tokens) - 2:
            if tokens[i].getType() != 'STRING':
                return False

            i += 1

            result = self.verifyBlock(i, tokens, True)
            if result:
                i = result
            else:
                return False

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
