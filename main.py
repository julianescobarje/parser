from lexer import Lexer
from verifier import Verifier
from reserved_words import *


def main():
    # file_url = input('Ingrese el archivo: ')
    file_url = './program.txt'

    try:
        lexer = Lexer(file_url)
    except FileNotFoundError:
        print('No se encontro el archivo')
        return

    tokens = lexer.tokenize()
    print(tokens)

    verifier = Verifier(tokens)
    result = verifier.verifySyntax() if tokens else False

    print('yes') if result else print('no')


if __name__ == '__main__':
    main()
