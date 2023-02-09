from tokenizer import Token

digitos = [str(x) for x in range(10)]
letras = [chr(x) for x in range(65, 91)]

"""
Definición de tokens
"""

reserved_words = ['ROBOT_R',
                  'VARS',
                  'PROCS',
                  'WHILE',
                  'DO',
                  'IF',
                  'THEN',
                  'ELSE',
                  'ASSIGNTO',
                  'GOTO',
                  'MOVE',
                  'TURN',
                  'FACE',
                  'PUT',
                  'PICK',
                  'MOVETOTHE',
                  'MOVEINDIR',
                  'JUMPTOTHE',
                  'JUMPINDIR',
                  'NOP',
                  'REPEAT',
                  'FACING',
                  'CANPUT',
                  'CANPICK',
                  'CANMOVEINDIR',
                  'CANJUMPINDIR',
                  'CANMOVETOTHE',
                  'CANJUMPTOTHE',
                  'NOT',
                  'M',
                  'R',
                  'C',
                  'B',
                  'P',
                  'J',
                  'G',
                  'CHIPS',
                  'BALLOONS',
                  'EAST',
                  'NORTH',
                  'SOUTH',
                  'WEST',
                  'FRONT',
                  'BACK',
                  'RIGHT',
                  'LEFT']


class Lexer:
    def __init__(self, program):
        self.program = program
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.program[self.pos] if self.pos < len(
            self.program) else None

    def make_number(self):
        num_str = ''
        exist_point = False

        while self.current_char and self.current_char != ' ' and (self.current_char in digitos or self.current_char == '.'):
            if self.current_char == '.':
                if exist_point:
                    break
                exist_point = True
                num_str += '.'
            else:
                num_str += self.current_char
                self.advance()

        if exist_point:
            return Token('FLOAT', float(num_str))
        else:
            return Token('INT', int(num_str))

    def generateToken(self, word):
        return Token(word, '')

    def make_word(self):
        word = ''

        while self.current_char and self.current_char != ' ' and (self.current_char in letras or self.current_char in digitos or self.current_char == '_'):
            word += self.current_char
            self.advance()

        if word in reserved_words:
            return self.generateToken(word)
        else:
            return Token('STRING', word)

    def make_tokens(self):
        tokens = []
        token_types = {
            ' ': lambda: None,
            '\t': lambda: None,
            '|': lambda: tokens.append(Token('LINE', '')),
            '[': lambda: tokens.append(Token('LKEY', '')),
            ']': lambda: tokens.append(Token('RKEY', '')),
            ';': lambda: tokens.append(Token('SEMICOLON', '')),
            ':': lambda: tokens.append(Token('COLON', '')),
            ',': lambda: tokens.append(Token('COMMA', '')),
        }

        while self.current_char is not None:
            if self.current_char in digitos:
                tokens.append(self.make_number())
            elif self.current_char in letras:
                tokens.append(self.make_word())
            elif self.current_char in token_types:
                token_types[self.current_char]()
                self.advance()
            else:
                self.advance()
                return

        return tokens
