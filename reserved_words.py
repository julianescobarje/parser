from tokenizer import Token

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
                  'LEFT',
                  'AROUND']

characters = {
    '|': Token('PIPE', ''),
    '[': Token('LKEY', ''),
    ']': Token('RKEY', ''),
    ';': Token('SEMICOLON', ''),
    ':': Token('COLON', ''),
    ',': Token('COMMA', ''),
}

commands = {
    'ASSIGNTO': [['INT', 'FLOAT'], 'VARIABLE'],
    'GOTO': [['VARIABLE', 'INT', 'FLOAT'], ['VARIABLE', 'INT', 'FLOAT']],
    'MOVE': [['VARIABLE', 'INT', 'FLOAT']],
    'TURN': [['LEFT', 'RIGHT', 'AROUND']],
    'FACE': [['NORTH', 'SOUTH', 'EAST', 'WEST']],
    'PUT': [['VARIABLE', 'INT', 'FLOAT'], ['BALLOONS', 'CHIPS']],
    'PICK': [['VARIABLE', 'INT', 'FLOAT'], ['BALLOONS', 'CHIPS']],
    'MOVETOTHE': [['VARIABLE', 'INT', 'FLOAT'], ['FRONT', 'RIGHT', 'LEFT', 'BACK']],
    'MOVEINDIR': [['VARIABLE', 'INT', 'FLOAT'], ['NORTH', 'SOUTH', 'EAST', 'WEST']],
    'JUMPTOTHE': [['VARIABLE', 'INT', 'FLOAT'], ['FRONT', 'RIGHT', 'LEFT', 'BACK']],
    'JUMPINDIR': [['VARIABLE', 'INT', 'FLOAT'], ['NORTH', 'SOUTH', 'EAST', 'WEST']],
    'NOP': None
}

control_structures = {
    'IF': ['CONDITION', 'THEN', 'COLON', 'BLOCK', 'ELSE', 'COLON', 'BLOCK'],
    'WHILE': ['CONDITION', 'DO', 'COLON', 'BLOCK'],
    'REPEAT': [['VARIABLE', 'INT', 'FLOAT'], 'BLOCK']
}

conditions = {
    'FACING': [['NORTH', 'SOUTH', 'EAST', 'WEST']],
    'CANPUT': [['VARIABLE', 'INT', 'FLOAT'], ['CHIPS', 'BALLOONS']],
    'CANPICK': [['VARIABLE', 'INT', 'FLOAT'], ['CHIPS', 'BALLOONS']],
    'CANMOVEINDIR': [['VARIABLE', 'INT', 'FLOAT'], ['NORTH', 'SOUTH', 'EAST', 'WEST']],
    'CANJUMPINDIR': [['VARIABLE', 'INT', 'FLOAT'], ['NORTH', 'SOUTH', 'EAST', 'WEST']],
    'CANJUMPINDIR': [['VARIABLE', 'INT', 'FLOAT'], ['NORTH', 'SOUTH', 'EAST', 'WEST']],
    'CANMOVETOTHE': [['VARIABLE', 'INT', 'FLOAT'], ['FRONT', 'RIGHT', 'LEFT', 'BACK']],
    'CANJUMPTOTHE': [['VARIABLE', 'INT', 'FLOAT'], ['FRONT', 'RIGHT', 'LEFT', 'BACK']],
    'NOT': ['CONDITION']
}
