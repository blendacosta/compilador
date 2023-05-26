palavras_reservadas = ['program', 'if', 'then', 'else', 'while', 'do', 'until', 'repeat', 'int', 'double', 'char', 'case', 'switch', 'end', 'procedure', 'function','for', 'begin']
simbolos_especiais = [',', ';', '.', '=', '(', ')', '{', '}']

# funções auxiliares
def em_branco(c):
  return c == ' '

def nova_linha(c):
  return c == '\n'

def letra(c):
  return c.isalpha()

def let_dig(c):
  return c.isalnum()

def digito(c):
  return c.isdigit()

def ignorar_em_branco(c, arquivo):
  # ignora os espaços em branco até achar um caracter
  while c < len(arquivo) and em_branco(arquivo[c]):
    c += 1
  return c

# implementação do léxico
def lexico(arquivo):
  linha_atual = 1 # contagem de linhas do arquivo
  lexema = '' # unidade que vai formar o token futuramente
  
  c = 0 # arquivo[c] : caracter lido
  while c < len(arquivo):
    c = ignorar_em_branco(c, arquivo)
    
    # verifica se é nova linha e passa para o próximo atualizando a contagem de linhas
    if c < len(arquivo) and nova_linha(arquivo[c]):
      linha_atual += 1
      c += 1
      continue
    
    # identificador
    elif letra(arquivo[c]): # 0 >> 1
      lexema += arquivo[c]
      if c+1 < len(arquivo):
        c += 1
        if arquivo[c] in ('!', '_'):  # 1 >> 2
          lexema += arquivo[c]
          if c+1 < len(arquivo):
            c += 1
            if let_dig(arquivo[c]): # 2 >> 3
              while c < len(arquivo) and let_dig(arquivo[c]): # 3 >> 3
                lexema += arquivo[c]
                c += 1
              print('id:', lexema)
              lexema = ''
            else: # finalização do token inválido
              print(f'Erro: identificador inválido [ {lexema} ] na linha {linha_atual}.')
              exit()
          else: # finalização do token inválido
            print(f'Erro: identificador inválido [ {lexema} ] na linha {linha_atual}.')
            exit()
        elif let_dig(arquivo[c]): # 1 >> 3
          while c < len(arquivo) and let_dig(arquivo[c]): # 3 >> 3
            lexema += arquivo[c]
            c += 1
          if lexema in palavras_reservadas: # verificação se é uma palavra reservada
            print('pr:', lexema)
          else:
            print('id:', lexema)
          lexema = ''
        else: # finalização do token
          print('id:', lexema)
          lexema = ''
      else: # finalização do token
        print('id:', lexema)
        lexema = ''
        c += 1
    
    # comentário
    elif arquivo[c] == '/': # 0 >> 6
      lexema += arquivo[c]  # /
      if c+1 < len(arquivo):
        c += 1
        if arquivo[c] == '/': # 6|13 >> 14
          lexema += arquivo[c]  # //
          if c+1 < len(arquivo):
            c += 1
            while c < len(arquivo) and arquivo[c] != '/': # 14 >> 14
              if nova_linha(arquivo[c]):
                linha_atual += 1
                c += 1
              else:
                lexema += arquivo[c]
                c += 1
            if c >= len(arquivo): # no caso de c ter passado de index válido, ou seja nunca achou o fim de comentário
              print(f'Erro: comentário inválido  [ {lexema} ], não foi finalizado na linha {linha_atual}.')
              exit()
            lexema += arquivo[c]  # / | 14 >> 15
            if c+1 < len(arquivo):
              c += 1
              if arquivo[c] == '/':
                lexema += arquivo[c]  # / | 15 > 12
                print('comentário:', lexema)
                lexema = ''
                c += 1
              else:
                lexema += arquivo[c]
                print(f'Erro: comentário inválido [ {lexema} ] na linha [ {linha_atual} ]')
                exit()
            else:
              print(f'Erro: comentário inválido [ {lexema} ], não foi finalizado na linha {linha_atual}.')
              exit()
        elif arquivo[c] == ':': # 13 >> 16
          lexema += arquivo[c]  # /:
          if c+1 < len(arquivo):
            c += 1
            while c < len(arquivo) and arquivo[c] != ':': # 16 >> 16
              if nova_linha(arquivo[c]):
                linha_atual += 1
                c += 1
              else:
                lexema += arquivo[c]
                c += 1
            if c >= len(arquivo): # no caso de c ter passado de index válido, ou seja nunca achou o fim de comentário
              print(f'Erro: comentário inválido  [ {lexema} ], não foi finalizado na linha {linha_atual}.')
              exit()
            lexema += arquivo[c]  # : | 16 >> 17
            if c+1 < len(arquivo):
              c += 1
              if arquivo[c] == '/':
                lexema += arquivo[c]  # :/ | 17 >> 12
                print('comentário:', lexema)
                lexema = ''
                c += 1
              else:
                lexema += arquivo[c]
                print(f'Erro: comentário inválido [ {lexema} ] na linha [ {linha_atual} ]')
                exit()
            else:
              print(f'Erro: comentário inválido [ {lexema} ], não foi finalizado na linha {linha_atual}.')
              exit()
        else:
          print('se:', lexema)
          lexema = ''
          continue
      else:
        print('se:', lexema)
        lexema = ''
        c += 1 
    elif arquivo[c] == '@': # 0 >> 6
      lexema += arquivo[c]
      if c+1 < len(arquivo):
        c += 1
        if arquivo[c] == '@': # 6|10 >> 11
          while c < len(arquivo) and arquivo[c] != '\n': # 11 >> 11
            lexema += arquivo[c]
            c += 1
          linha_atual += 1
          print('comentário:', lexema)
          lexema = ''
          c += 1
        else:
          print('se:', lexema)
          lexema = ''
          continue
      else:
        print('se:', lexema)
        lexema = ''
    
    # dígito
    elif arquivo[c] == '-': # 0 >> 6
      lexema += arquivo[c]
      if c+1 < len(arquivo):
        c += 1
        if digito(arquivo[c]): # 6|21 >> 18
          while c < len(arquivo) and digito(arquivo[c]): # 18 >> 18
            lexema += arquivo[c]
            c += 1
          if arquivo[c] == ',': # 18 >> 19
            lexema += arquivo[c]
            if c+1 < len(arquivo):
              c += 1
              if digito(arquivo[c]): # 19 >> 20
                while c < len(arquivo) and digito(arquivo[c]): # 20 >> 20
                  lexema += arquivo[c]
                  c += 1
                print('d:', lexema)
                lexema = ''
                continue
            print(f'Erro: número inválido [ {lexema} ] na linha {linha_atual}.')
            exit()          
          else:
            print('d:', lexema)
            lexema = ''
            continue
      print('se:', lexema)
      lexema = '' 
    elif digito(arquivo[c]): # 0 >> 18
      while c < len(arquivo) and digito(arquivo[c]): # 18 >> 18
        lexema += arquivo[c]
        c += 1
      if arquivo[c] == ',': # 18 >> 19
        lexema += arquivo[c]
        if c+1 < len(arquivo):
          c += 1
          if digito(arquivo[c]): # 19 >> 20
            while c < len(arquivo) and digito(arquivo[c]): # 20 >> 20
              lexema += arquivo[c]
              c += 1
            print('d:', lexema)
            lexema = ''
            continue
        print(f'Erro: número inválido [ {lexema} ] na linha {linha_atual}.')
        exit()          
      else:
        print('d:', lexema)
        lexema = ''
        continue
    
    # simbolo especial
    elif arquivo[c] == '<': # 0 >> 4
      lexema += arquivo[c]
      if c+1 < len(arquivo):
        c += 1
        if arquivo[c] in ('>', '='): # 4 >> 6
          lexema += arquivo[c]
        else:
          print('se:', lexema)
          lexema = ''
          continue
      print('se:', lexema)
      lexema = ''
      if c < len(arquivo):
        c += 1
    elif arquivo[c] == '>': # 0 >> 5
      lexema += arquivo[c]
      if c+1 < len(arquivo):
        c += 1
        if arquivo[c] == '=': # 5 >> 6
          lexema += arquivo[c]
        else:
          print('se:', lexema)
          lexema = ''
          continue
      print('se:', lexema)
      lexema = ''
      if c < len(arquivo):
        c += 1
    elif arquivo[c] == '*': # 0 >> 7
      lexema += arquivo[c]
      if c+1 < len(arquivo):
        c += 1
        if arquivo[c] == '*': # 7 >> 6
          lexema += arquivo[c]
        else:
          print('se:', lexema)
          lexema = ''
          continue
      print('se:', lexema)
      lexema = ''
      if c < len(arquivo):
        c += 1
    elif arquivo[c] == '+': # 0 >> 8
      lexema += arquivo[c]
      if c+1 < len(arquivo):
        c += 1
        if arquivo[c] == '+': # 8 >> 6
          lexema += arquivo[c]
        else:
          print('se:', lexema)
          lexema = ''
          continue
      print('se:', lexema)
      lexema = ''
      if c < len(arquivo):
        c += 1
    elif arquivo[c] == ':': # 0 >> 9
      lexema += arquivo[c]
      if c+1 < len(arquivo):
        c += 1
        if arquivo[c] == '=': # 9 >> 6
          lexema += arquivo[c]
        else:
          print('se:', lexema)
          lexema = ''
          continue
      print('se:', lexema)
      lexema = ''
      if c < len(arquivo):
        c += 1
    elif arquivo[c] in simbolos_especiais: # 0 >> 6
      lexema += arquivo[c]
      print('se:', lexema)
      lexema = ''
      if c < len(arquivo):
        c += 1
    
    else:
      print(f'Erro: caracter inválido [ {arquivo[c]} ] na linha [ {linha_atual} ]')
      exit()

# 1. leitura do arquivo fonte
arquivo_fonte = open('fonte.txt', 'tr')
arquivo = arquivo_fonte.read()
arquivo_fonte.close()

# 2. entrada do arquivo no léxico
lexico(arquivo)