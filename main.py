from lexico import Lexico

if __name__ == '__main__':
    l = Lexico('fonte.txt')

    while not l.fim_arquivo:
        token = l.gerar_token()
        if not token['tipo'] == 'comentario':
            print(token)
