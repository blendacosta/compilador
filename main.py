from lexico import Lexico
from sintatico import Sintatico

if __name__ == '__main__':
    l = Lexico('teste.txt')
    s = Sintatico(l)
    s.programa()
    print('mo! compilado com sucesso! (๑•̀ㅂ•́)و✧')
 