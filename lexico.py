class Lexico:
  palavras_reservadas = ['program', 'if', 'then', 'else', 'while', 'do', 'until', 'repeat', 'int', 'double', 'char', 'case', 'switch', 'end', 'procedure', 'function','for', 'begin']
  simbolos_especiais = [',', ';', '.', '=', '(', ')', '{', '}']
  
  def __init__(self, nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
      self.arquivo = arquivo.read()
    self.linha_atual = 1
    self.posicao_atual = 0
    self.caractere_atual = self.arquivo[self.posicao_atual]
    self.tamanho_arquivo = len(self.arquivo)
    self.lexema = ''
    self.fim_arquivo = False
  
  def ignorar_em_branco(self):
    while self.posicao_atual < self.tamanho_arquivo and l.em_branco(self.caractere_atual):
      self.posicao_atual += 1
      self.caractere_atual = self.arquivo[self.posicao_atual]
      
  def verifica_nova_linha(self):
    while self.nova_linha(self.caractere_atual):
        self.linha_atual += 1
        if self.posicao_atual+1 < len(self.arquivo):
            self.posicao_atual += 1
            self.caractere_atual = self.arquivo[self.posicao_atual]
        else:
            self.fim_arquivo = True
            break
  
  def proximo_caractere(self):
    if self.posicao_atual+1 < self.tamanho_arquivo:
      self.posicao_atual += 1
      self.caractere_atual = self.arquivo[self.posicao_atual]
      return True
    else:
      self.fim_arquivo = True
      return False
  
  def erro_identificador_invalido(self):
    print(f'Erro: identificador inválido [ {self.lexema} ] na linha {self.linha_atual}.')
    exit()
  
  def erro_caractere_invalido(self):
    print(f'Erro: caractere inválido [ {self.lexema} ] na linha {self.linha_atual}.')
    exit()
    
  def erro_comentario_invalido(self):
    print(f'Erro: comentário inválido  [ {self.lexema} ] na linha {self.linha_atual}.')
    exit()
    
  def erro_digito_invalido(self):
    print(f'Erro: dígito inválido [ {self.lexema} ] na linha {self.linha_atual}.')
    exit()
    
  def gerar_token(self):
    self.ignorar_em_branco() # ignora os espaços em branco até achar um caracter
    self.verifica_nova_linha() # verifica se é nova linha e passa para o próximo atualizando a contagem de linhas
    
    # identificador
    if self.letra(self.caractere_atual): # 0 >> 1
      self.lexema += self.caractere_atual
      if self.proximo_caractere():
        if self.caractere_atual in ('!', '_'):  # 1 >> 2
          self.lexema += self.caractere_atual
          if self.proximo_caractere():
            self.lexema += self.caractere_atual
            if self.let_dig(self.caractere_atual): # 2 >> 3
              while self.proximo_caractere() and self.let_dig(self.caractere_atual): # 3 >> 3
                self.lexema += self.caractere_atual
              token = {'tipo': 'identificador', 'valor': self.lexema}
              self.lexema = ''
              return token
            else: # finalização do token inválido
              self.erro_identificador_invalido()
          else: # finalização do token inválido
            self.erro_identificador_invalido()       
        elif self.let_dig(self.caractere_atual): # 1 >> 3
          self.lexema += self.caractere_atual
          while self.proximo_caractere() and self.let_dig(self.caractere_atual): # 3 >> 3
            self.lexema += self.caractere_atual
            
          if self.lexema in self.palavras_reservadas:
            token = {'tipo': 'palavra_reservada', 'valor': self.lexema}
          else:
            token = {'tipo': 'identificador', 'valor': self.lexema}
          
          self.lexema = ''
          return token
        
        else: # finalização do token válido
          token = {'tipo': 'identificador', 'valor': self.lexema}
          self.lexema = ''
          return token
      else: # finalização do token válido
        token = {'tipo': 'identificador', 'valor': self.lexema}
        self.lexema = ''
        return token
    # comentário
    elif self.caractere_atual == '/': # 0 >> 6
      self.lexema += self.caractere_atual
      if self.proximo_caractere():
        if self.caractere_atual == '/': # 6|13 >> 14
          self.lexema += self.caractere_atual
          while self.proximo_caractere() and self.caractere_atual != '/': # 14 >> 14
            if self.nova_linha(self.caractere_atual):
              self.linha_atual += 1
            else:
              self.lexema += self.caractere_atual
          self.lexema += self.caractere_atual # / | 14 >> 15
          if self.proximo_caractere() and self.caractere_atual == '/': # 15 >> 12
            self.lexema += self.caractere_atual
            token = {'tipo': 'comentario', 'valor': self.lexema}
            self.lexema = ''
            return token  
          else:
            self.erro_comentario_invalido()
        elif self.caractere_atual == ':': # 6|13 >> 16
          self.lexema += self.caractere_atual
          while self.proximo_caractere() and self.caractere_atual != ':': # 16 >> 16
            if self.nova_linha(self.caractere_atual):
              self.linha_atual += 1
            else:
              self.lexema += self.caractere_atual
          self.lexema += self.caractere_atual # : | 16 >> 17
          if self.proximo_caractere() and self.caractere_atual == '/': # 17 >> 12
            self.lexema += self.caractere_atual
            token = {'tipo': 'comentario', 'valor': self.lexema}
            self.lexema = ''
            return token
          else:
            self.erro_comentario_invalido()
        else:
          token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
          self.lexema = ''
          return token
      else:
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token
    elif self.caractere_atual == '@': # 0 >> 6
      self.lexema += self.caractere_atual
      if self.proximo_caractere():
        if self.caractere_atual == '@': # 6|10 >> 11
          self.lexema += self.caractere_atual
          while self.proximo_caractere() and not self.nova_linha(self.caractere_atual): # 11 >> 11
            self.lexema += self.caractere_atual
          self.linha_atual += 1
          # 11 >> 12
          token = {'tipo': 'comentario', 'valor': self.lexema}
          self.lexema = ''
          return token
        else:
          token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
          self.lexema = ''
          return token
      else:
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token
    # dígito
    elif self.digito(self.caractere_atual): # 0 >> 18
      self.lexema += self.caractere_atual
      while self.proximo_caractere() and self.digito(self.caractere_atual): # 18 >> 18
        self.lexema += self.caractere_atual
      if self.caractere_atual == ',': # 18 >> 19
        self.lexema += self.caractere_atual
        if self.proximo_caractere():
          if self.digito(self.caractere_atual): # 19 >> 20
            self.lexema += self.caractere_atual
            while self.proximo_caractere() and self.digito(self.caractere_atual): # 20 >> 20
              self.lexema += self.caractere_atual
            token = {'tipo': 'digito', 'valor': self.lexema}
            self.lexema = ''
            return token
          else:
            self.erro_digito_invalido()
        else:
          self.erro_digito_invalido()
      else:
        token = {'tipo': 'digito', 'valor': self.lexema}
        self.lexema = ''
        return token
    elif self.caractere_atual == '-': # 0 >> 6
      self.lexema += self.caractere_atual
      if self.proximo_caractere():
        if self.digito(self.caractere_atual): # 6|21 >> 18
          self.lexema += self.caractere_atual
          while self.proximo_caractere() and self.digito(self.caractere_atual): # 18 >> 18
            self.lexema += self.caractere_atual
          if self.caractere_atual == ',': # 18 >> 19
            self.lexema += self.caractere_atual
            if self.proximo_caractere():
              if self.digito(self.caractere_atual): # 19 >> 20
                self.lexema += self.caractere_atual
                while self.proximo_caractere() and self.digito(self.caractere_atual): # 20 >> 20
                  self.lexema += self.caractere_atual
                token = {'tipo': 'digito', 'valor': self.lexema}
                self.lexema = ''
                return token
              else:
                self.erro_digito_invalido()
            else:
              self.erro_digito_invalido()
          else:
            token = {'tipo': 'digito', 'valor': self.lexema}
            self.lexema = ''
            return token
        else:
          token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
          self.lexema = ''
          return token
      else:
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token
    # símbolo especial
    elif self.caractere_atual == '<': # 0 >> 4
      self.lexema += self.caractere_atual
      if self.proximo_caractere():
        if self.caractere_atual in ('=', '>'): # 4 >> 6
          self.lexema += self.caractere_atual
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token
      else:
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token  
    elif self.caractere_atual == '>': # 0 >> 5
      self.lexema += self.caractere_atual
      if self.proximo_caractere():
        if self.caractere_atual == '=': # 5 >> 6
          self.lexema += self.caractere_atual
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token
      else:
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token   
    elif self.caractere_atual == '*': # 0 >> 7
      self.lexema += self.caractere_atual
      if self.proximo_caractere():
        if self.caractere_atual == '*': # 7 >> 6
          self.lexema += self.caractere_atual
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token
      else:
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token  
    elif self.caractere_atual == '+': # 0 >> 8
      self.lexema += self.caractere_atual
      if self.proximo_caractere():
        if self.caractere_atual == '+': # 8 >> 6
          self.lexema += self.caractere_atual
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token
      else:
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token  
    elif self.caractere_atual == ':': # 0 >> 9
      self.lexema += self.caractere_atual
      if self.proximo_caractere():
        if self.caractere_atual == '=': # 9 >> 6
          self.lexema += self.caractere_atual
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token
      else:
        token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
        self.lexema = ''
        return token  
    elif self.caractere_atual in self.simbolos_especiais: # 0 >> 6
      self.lexema += self.caractere_atual
      token = {'tipo': 'simbolo_especial', 'valor': self.lexema}
      self.lexema = ''
      self.proximo_caractere()
      return token
    else:
      if not self.fim_arquivo:
        self.erro_caractere_invalido()
      
  @classmethod
  def em_branco(cls, caractere):
    return caractere == ' '
    
  def nova_linha(cls, caractere):
    return caractere == '\n'
    
  def letra(cls, caractere):
    return caractere.isalpha()
    
  def let_dig(cls, caractere):
    return caractere.isalnum()
    
  def digito(cls, caractere):
    return caractere.isdigit()
  
  
  
l = Lexico('fonte.txt')

while not l.fim_arquivo:
  print(l.gerar_token())