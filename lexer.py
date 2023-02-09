from reserved_words import *
from tokenizer import Token
from helper import Helper


class Lexer:
    def __init__(self, file_URL):
        self.file_URL = file_URL
        self.helper = Helper()
        self.program = None
        self.readProgram()

    def cleanProgram(self, program: str) -> list:
        program = program.upper()
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
