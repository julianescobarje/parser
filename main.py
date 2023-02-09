from lexer import Lexer


def tokenize(program):
    lexer = Lexer(program)
    tokens = lexer.make_tokens()
    return tokens


def verifySyntax(tokens):
    if str(tokens[0]) != 'ROBOT_R':
        return False


def main():
    try:
        # file_url = input('Ingrese el archivo: ')
        file_url = './program.txt'

        with open(file_url) as file:
            program = ' '.join(line.strip().upper() for line in file)

        tokens = tokenize(program)

        print(tokens)

        # result = verifySyntax(tokens) if tokens else False

        # print('yes') if result else print('no')

        file.close()

    except FileNotFoundError:
        print('No se encontro el archivo')


if __name__ == '__main__':
    main()
