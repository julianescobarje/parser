from tokenizer import Token

special_reserved_words = [
    'MOVE', 'MOVETOTHE', 'MOVEINDIR', 'CANMOVEINDIR', 'CANMOVETOTHE'
]

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

characters = {
    '|': Token('LINE', ''),
    '[': Token('LKEY', ''),
    ']': Token('RKEY', ''),
    ';': Token('SEMICOLON', ''),
    ':': Token('COLON', ''),
    ',': Token('COMMA', ''),
}
