from reserved_words import *
from tokenizer import Token
from helper import Helper


class Lexer:
    def __init__(self, file_URL):
        self.file_URL = file_URL
        self.helper = Helper()
        self.program = None
        self.readProgram()

    def specialReplace(self, string: str) -> str:
        start = 0
        while start < len(string):
            pos = string.find('MOVE', start)
            if pos == -1:
                break
            word_end = pos + 4
            if string[pos+4:pos+9] == 'INDIR' or string[pos+4:pos+9] == 'TOTHE':
                word_end += 5
            if string[pos-3:pos] == 'CAN':
                pos -= 3
            string = string[:pos] + ' ' + \
                string[pos:word_end] + ' ' + string[word_end:]
            start = word_end + 2
        return string

    def cleanProgram(self, program: str) -> list:
        program = program.upper()
        program = self.specialReplace(program)
        for word in reserved_words:
            if word not in special_reserved_words:
                program = program.replace(word, f' {word} ')
        for character in characters:
            program = program.replace(character, f' {character} ')
        program = program.replace('\t', ' ').replace('\n', ' ').strip()
        return program.split()

    def readProgram(self):
        with open(self.file_URL) as file:
            program = file.read()
            self.program = self.cleanProgram(program)

    def generateToken(self, word):
        return Token(word, '')

    def getToken(self, word):
        if word in reserved_words:
            return self.generateToken(word)
        elif word in characters:
            return characters[word]
        elif self.helper.isInteger(word):
            return Token('INT', int(word))
        elif self.helper.isFloat(word):
            return Token('FLOAT', float(word))
        else:
            return Token('STRING', word)

    def tokenize(self):
        tokens = []

        for word in self.program:
            tokens.append(self.getToken(word))

        return tokens
