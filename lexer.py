from tokenizer import Token

digitos = [str(x) for x in range(10)]
letras = [chr(x) for x in range(65, 91)]

'''
Definición de tokens
'''
TSTRING = 'STRING'
TINT = 'INT'
TFLOAT = 'FLOAT'
TROBOT_R = 'ROBOT_R'
TVARS = 'VARS'
TPROCS = 'PROCS'
TLINE = 'LINE'
TLKEY = 'LKEY'
TRKEY = 'RKEY'
TSEMICOLON = 'SEMICOLON'
TTWOPOINTS = 'TWOPOINTS'
TWHILE = 'WHILE'
TDO = 'DO'
TIF = 'IF'
TTHEN = 'THEN'
TELSE = 'ELSE'
TCOMA = 'COMA'
TM = 'M'
TR = 'R'
TC = 'C'
TB = 'B'
TP = 'P'
TJ = 'J'
TG = 'G'
TASSIGNTO = 'ASSIGNTO'
TGOTO = 'GOTO'
TMOVE = 'MOVE'
TTURN = 'TURN'
TFACE = 'FACE'
TPUT = 'PUT'
TPICK = 'PICK'
TMOVETOTHE = 'MOVETOTHE'
TMOVEINDIR = 'MOVEINDIR'
TJUMPTOTHE = 'JUMPTOTHE'
TJUMPINDIR = 'JUMPINDIR'
TNOP = 'NOP'
TREPEAT = 'REPEAT'
TFACING = 'FACING'
TCANPUT = 'CANPUT'
TCANPICK = 'CANPICK'
TCANMOVEINDIR = 'CANMOVEONDIR'
TCANJUMPINDIR = 'CANJUMPINDIR'
TCANMOVETOTHE = 'CANMOVETOTHE'
TCANJUMPTOTHE = 'CANJUMPTOTHE'
TNOT = 'NOT'
TCHIPS = 'CHIPS'
TBALLOONS = 'BALLOONS'
TEAST = 'EAST'
TSOUTH = 'SOUTH'
TNORTH = 'NORTH'
TWEST = 'WEST'
TFRONT = 'FRONT'
TBACK = 'BACK'
TLEFT = 'LEFT'
TRIGHT = 'RIGHT'


class Lexer:
    def __init__(self, program):
        self.program = program
        self.pos = -1
        self.current_char = None
        self.advance()

    # Avanza el contador de posicion y actualiza el caracter actual siendo leido en el programa
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
            return Token(TFLOAT, float(num_str))
        else:
            return Token(TINT, int(num_str))

    def get_token(self, word):
        switch = {
            'ROBOT_R': Token(TROBOT_R, ''),
            'VARS': Token(TVARS, ''),
            'PROCS': Token(TPROCS, ''),
            'WHILE': Token(TWHILE, ''),
            'DO': Token(TDO, ''),
            'IF': Token(TIF, ''),
            'THEN': Token(TTHEN, ''),
            'ELSE': Token(TELSE, ''),
            'ASSIGNTO': Token(TASSIGNTO, ''),
            'GOTO': Token(TGOTO, ''),
            'MOVE': Token(TMOVE, ''),
            'TURN': Token(TTURN, ''),
            'FACE': Token(TFACE, ''),
            'PUT': Token(TPUT, ''),
            'PICK': Token(TPICK, ''),
            'MOVETOTHE': Token(TMOVETOTHE, ''),
            'MOVEINDIR': Token(TMOVEINDIR, ''),
            'JUMPTOTHE': Token(TJUMPTOTHE, ''),
            'JUMPINDIR': Token(TJUMPINDIR, ''),
            'NOP': Token(TNOP, ''),
            'REPEAT': Token(TREPEAT, ''),
            'FACING': Token(TFACING, ''),
            'CANPUT': Token(TCANPUT, ''),
            'CANPICK': Token(TCANPICK, ''),
            'CANMOVEINDIR': Token(TCANMOVEINDIR, ''),
            'CANJUMPINDIR': Token(TCANJUMPINDIR, ''),
            'CANMOVETOTHE': Token(TCANMOVETOTHE, ''),
            'CANJUMPTOTHE': Token(TCANJUMPTOTHE, ''),
            'NOT': Token(TNOT, ''),
            'M': Token(TM, ''),
            'R': Token(TR, ''),
            'C': Token(TC, ''),
            'B': Token(TB, ''),
            'P': Token(TP, ''),
            'J': Token(TJ, ''),
            'G': Token(TG, ''),
            'CHIPS': Token(TCHIPS, ''),
            'BALLOONS': Token(TBALLOONS, ''),
            'EAST': Token(TEAST, ''),
            'NORTH': Token(TNORTH, ''),
            'SOUTH': Token(TSOUTH, ''),
            'WEST': Token(TWEST, ''),
            'FRONT': Token(TFRONT, ''),
            'BACK': Token(TBACK, ''),
            'RIGHT': Token(TRIGHT, ''),
            'LEFT': Token(TLEFT, '')
        }

        return switch.get(word, Token(TSTRING, word))

    def make_word(self):
        word = ''

        while self.current_char and self.current_char != ' ' and (self.current_char in letras or self.current_char in digitos or self.current_char == '_'):
            word += self.current_char
            self.advance()

        return self.get_token(word)

    def make_tokens(self):
        tokens = []
        token_types = {
            ' ': lambda: None,
            '\t': lambda: None,
            '|': lambda: tokens.append(Token(TLINE, '')),
            '[': lambda: tokens.append(Token(TLKEY, '')),
            ']': lambda: tokens.append(Token(TRKEY, '')),
            ';': lambda: tokens.append(Token(TSEMICOLON, '')),
            ':': lambda: tokens.append(Token(TTWOPOINTS, '')),
            ',': lambda: tokens.append(Token(TCOMA, '')),
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
