class Lexico:
  """
    Classe responsável por realizar a análise léxica de um arquivo de código fonte.
  """
   # Lista de palavras reservadas
  palavras_reservadas = ['program', 'if', 'then', 'else', 'while', 'do', 'until', 'repeat', 'int', 'double', 'char', 'case', 'switch', 'end', 'procedure', 'function','for', 'begin']
  # Lista de símbolos especiais
  simbolos_especiais = [',', ';', '.', '=', '(', ')', '{', '}']
  
  def __init__(self, nome_arquivo):
    """
    Inicializa o objeto com o conteúdo do arquivo de código fonte.
    
    :param nome_arquivo: Nome do arquivo de código fonte a ser analisado.
    """
    with open(nome_arquivo, 'r') as arquivo:
      self.arquivo = arquivo.read()
    self.linha_atual = 1
    self.posicao_atual = 0
    self.caractere_atual = self.arquivo[self.posicao_atual]
    self.tamanho_arquivo = len(self.arquivo)
    self.lexema = ''
    self.fim_arquivo = False
  
  def ignorar_em_branco(self):
    """
    Ignora caracteres em branco e novas linha no arquivo de código fonte. Adicionalmente verifica se o fim do arquivo foi atingido.
    
    Esta função avança a posição atual no arquivo até encontrar um caractere que não seja considerado em branco pela função `em_branco`. Ou nova linha.
    """
    while self.posicao_atual < self.tamanho_arquivo:
      if self.em_branco(self.caractere_atual):
        if self.posicao_atual+1 < len(self.arquivo):
          self.posicao_atual += 1
          self.caractere_atual = self.arquivo[self.posicao_atual]
        else:
          self.fim_arquivo = True
          break
      elif self.nova_linha(self.caractere_atual):
        self.verifica_nova_linha()
      else:
        break
      
  def verifica_nova_linha(self):
    """
    Verifica se o caractere atual é uma nova linha e atualiza a linha atual.
    
    Esta função avança a posição atual no arquivo até encontrar um caractere que não seja uma nova linha. A cada nova linha encontrada, a linha atual é incrementada. Se o fim do arquivo for atingido, o atributo `fim_arquivo` é definido como `True`.
    """
    while self.nova_linha(self.caractere_atual):
      self.linha_atual += 1
      if self.posicao_atual+1 < len(self.arquivo):
          self.posicao_atual += 1
          self.caractere_atual = self.arquivo[self.posicao_atual]
      else:
          self.fim_arquivo = True
          break
  
  def proximo_caractere(self):
    """
    Avança para o próximo caractere no arquivo de código fonte.
    
    :return: `True` se o próximo caractere foi encontrado, `False` se o fim do arquivo foi atingido.
    """
    if self.posicao_atual+1 < self.tamanho_arquivo:
      self.posicao_atual += 1
      self.caractere_atual = self.arquivo[self.posicao_atual]
      return True
    else:
      self.fim_arquivo = True
      return False
  
  def erro_identificador_invalido(self):
    """
    Exibe uma mensagem de erro para um identificador inválido e encerra o programa.
    """
    print(f'Erro: identificador inválido [ {self.lexema} ] na linha {self.linha_atual}.')
    exit()
  
  def erro_caractere_invalido(self):
    """
    Exibe uma mensagem de erro para um caractere inválido e encerra o programa.
    """
    print(f'Erro: caractere inválido [ {self.caractere_atual} ] na linha {self.linha_atual}.')
    exit()
    
  def erro_comentario_invalido(self):
    """
    Exibe uma mensagem de erro para um comentário inválido e encerra o programa.
    """
    print(f'Erro: comentário inválido  [ {self.lexema} ] na linha {self.linha_atual}.')
    exit()
    
  def erro_digito_invalido(self):
    """
    Exibe uma mensagem de erro para um dígito inválido e encerra o programa.
    """
    print(f'Erro: dígito inválido [ {self.lexema} ] na linha {self.linha_atual}.')
    exit()
    
  def a_identificador(self):
    """
    Reconhece um identificador ou palavra reservada no arquivo de código fonte.
    
    :return: Um dicionário contendo o tipo e o valor do token gerado.
    """
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

  def a_comentario_vl(self):
    """
    Reconhece um comentário de várias linhas no arquivo de código fonte.
    
    :return: Um dicionário contendo o tipo e o valor do token gerado.
    """
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
          self.proximo_caractere()
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
  
  def a_comentario_ul(self):
    """
    Reconhece um comentário de única linha no arquivo de código fonte.
    
    :return: Um dicionário contendo o tipo e o valor do token gerado.
    """
    self.lexema += self.caractere_atual
    if self.proximo_caractere():
      if self.caractere_atual == '@': # 6|10 >> 11
        self.lexema += self.caractere_atual
        while self.proximo_caractere() and not self.nova_linha(self.caractere_atual): # 11 >> 11
          self.lexema += self.caractere_atual
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

  def a_digito(self):
    """
    Reconhece um dígito no arquivo de código fonte.
    
    :return: Um dicionário contendo o tipo e o valor do token gerado.
    """
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
  
  def a_digito_negativo(self):
    """
    Reconhece um dígito negativo no arquivo de código fonte.
    
    :return: Um dicionário contendo o tipo e o valor do token gerado.
    """
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

  def gerar_token(self):
    """
    Gera o próximo token a partir do arquivo de código fonte.
    
    Esta função ignora espaços em branco e verifica se o caractere atual é uma nova linha. Em seguida, ela verifica se o caractere atual é uma letra, um dígito ou um símbolo especial e chama a função apropriada para reconhecer o token.
    
    :return: Um dicionário contendo o tipo e o valor do token gerado.
    """
    self.ignorar_em_branco() # ignora os espaços em branco até achar um caracter
    
    if self.fim_arquivo:
      exit()
    
    # identificador
    if self.letra(self.caractere_atual): # 0 >> 1
      return self.a_identificador()
    
    # comentário
    elif self.caractere_atual == '/': # 0 >> 6
      return self.a_comentario_vl()
    
    elif self.caractere_atual == '@': # 0 >> 6
      return self.a_comentario_ul()
    
    # dígito
    elif self.digito(self.caractere_atual): # 0 >> 18
      return self.a_digito()
    
    elif self.caractere_atual == '-': # 0 >> 6
      return self.a_digito_negativo()
    
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
    """
    Verifica se um caractere é considerado em branco.
    
    :param caractere: Caractere a ser verificado.
    :return: `True` se o caractere for considerado em branco, `False` caso contrário.
    """
    return caractere == ' '
    
  def nova_linha(cls, caractere):
    """
    Verifica se um caractere é uma nova linha.
    
    :param caractere: Caractere a ser verificado.
    :return: `True` se o caractere for uma nova linha, `False` caso contrário.
    """
    return caractere == '\n'
    
  def letra(cls, caractere):
    """
    Verifica se um caractere é uma letra.
    
    :param caractere: Caractere a ser verificado.
    :return: `True` se o caractere for uma letra, `False` caso contrário.
    """
    return caractere.isalpha()
    
  def let_dig(cls, caractere):
    """
    Verifica se um caractere é uma letra ou um dígito.
    
    :param caractere: Caractere a ser verificado.
    :return: `True` se o caractere for uma letra ou um dígito, `False` caso contrário.
    """
    return caractere.isalnum()
    
  def digito(cls, caractere):
    """
    Verifica se um caractere é um dígito.
    
    :param caractere: Caractere a ser verificado.
    :return: `True` se o caractere for um dígito, `False` caso contrário.
    """
    return caractere.isdigit()
  