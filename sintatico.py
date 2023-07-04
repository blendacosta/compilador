class Sintatico:
  def __init__(self, lexico):
    self.l = lexico
    self.token = None
    self.valido = True
    
  def erro(self, esperado):
    if self.token is None:
      print(f'Erro: esperado [ {esperado} ], encontrado [ fim do arquivo ] na linha {self.l.linha_atual}.')
    else:
      print(f'Erro: esperado [ {esperado} ], encontrado [ {self.token["valor"]} ] na linha {self.l.linha_atual}.')
    exit()
  
  def obter_token(self):
    self.token = None
    self.token = self.l.gerar_token()
    if self.token and self.token['tipo'] == 'comentario':
      self.obter_token()
      
  # 01 <programa>: program <identificador> ; <bloco>
  def programa(self):
    self.obter_token()
    if self.token is None or self.token['valor'] != 'program':
      self.erro('program')
    self.obter_token()
    if self.token is None or self.token['tipo'] != 'identificador':
      self.erro('identificador')
    self.obter_token()
    if self.token is None or self.token['valor'] != ';':
      self.erro(';')
    self.bloco()
  
  # 02 <bloco>: [<definicao de tipos>] [<definicao de variaveis>] [<definicao de sub-rotinas>] <comando composto>
  def bloco(self):
    self.obter_token()
    if self.token is not None:
      if self.token['valor'] == 'type': # definicao de tipos
        self.d_tipos()
      if self.token['valor'] == 'var':  # definicao de variaveis
        self.d_variaveis()
      # 07 <definição de sub-rotinas>: {<definição de procedimento>; | <definição de função>;}
      while self.token is not None and self.token['valor'] in ('procedure', 'function'): # definicao de sub-rotinas
        if self.token['valor'] == 'procedure':
          self.d_procedimento()
        else:
          self.d_funcao()
        self.obter_token() 
        if self.token is None or self.token['valor'] != ';':
          self.erro(';')
        self.obter_token()
    self.comando_composto() # comando composto

  # 03 <definição de tipos>: type <identificador> = <tipo> ; {<identificador> = <tipo> ;}
  def d_tipos(self):
    self.obter_token()
    if self.token is None or self.token['tipo'] != 'identificador':
      self.erro('identificador')
    while True:
      self.obter_token()
      if self.token is None or self.token['valor'] != '=':
        self.erro('=')
      self.obter_token()
      if self.token is None or not self.tipo():
        self.erro('tipo')
      self.obter_token()
      if self.token is None or self.token['valor'] != ';':
        self.erro(';')
      self.obter_token()
      if self.token is None or self.token['tipo'] != 'identificador':
        break
  
  # 04 <tipo>: integer | double | boolean | char | <identificador>
  def tipo(self):
    return self.token['valor'] in ('integer', 'double', 'boolean', 'char') or self.token['tipo'] == 'identificador'
  
  # 05 <definição de variáveis>: var <lista de identificadores> : <tipo> {; <lista de identificadores> : <tipo>};
  def d_variaveis(self):
    self.obter_token()
    if self.token is None or self.token['tipo'] != 'identificador':
      self.erro('identificador')
    while True:
      self.lista_identificadores()
      if self.token is None or self.token['valor'] != ':':
        self.erro(':')
      self.obter_token()
      if not self.tipo():
        self.erro('tipo')
      self.obter_token()
      if self.token is None or self.token['valor'] != ';':
        self.erro(';')
      self.obter_token()
      if self.token is None or self.token['tipo'] != 'identificador':
        break
  
  # 06 <lista de identificadores>: <identificador> {, <identificador>}
  def lista_identificadores(self):
    self.obter_token()
    while self.token is not None and self.token['valor'] == ',':
      self.obter_token()
      if self.token is None or self.token['tipo'] != 'identificador':
        self.erro('identificador')
      self.obter_token()
  
  # 08 <definição de procedimento>: procedure <identificador> [<parâmetros formais>] ; <bloco>
  def d_procedimento(self):
    self.obter_token()
    if self.token is None or self.token['tipo'] != 'identificador':
      self.erro('identificador')
    self.obter_token()
    if self.token is not None and self.token['valor'] == '(':
      self.parametros_formais()
    if self.token is None or self.token['valor'] != ';':
      self.erro(';')
    self.bloco()
  
  # 09 <definição de função>: function <identificador> [<parâmetros formais>] : <tipo> ; <bloco>
  def d_funcao(self):
    self.obter_token()
    if self.token is None or self.token['tipo'] != 'identificador':
      self.erro('identificador')
    self.obter_token()
    if self.token is not None and self.token['valor'] == '(':
      self.parametros_formais()
    if self.token is None or self.token['valor'] != ':':
      self.erro(':')
    self.obter_token()
    if self.token is None or self.token['tipo'] != 'identificador':
      self.erro('identificador')
    self.obter_token()
    if self.token is None or self.token['valor'] != ';':
      self.erro(';')
    self.bloco()  
  
  # 10 <parâmetros formais>: (<lista de identificadores> : <identificador> {; <lista de identificadores> : <identificador>})
  def parametros_formais(self):
    self.obter_token()
    if self.token is None or self.token['tipo'] != 'identificador':
      self.erro('identificador')
    self.lista_identificadores()
    if self.token is None or self.token['valor'] != ':':
      self.erro(':')
    self.obter_token()
    if self.token is None or self.token['tipo'] != 'identificador':
      self.erro('identificador')
    
    self.obter_token()
    while self.token is not None and self.token['valor'] == ';':
      self.obter_token()
      if self.token is None or self.token['tipo'] != 'identificador':
        self.erro('identificador')
      self.lista_identificadores()
      if self.token is None or self.token['valor'] != ':':
        self.erro(':')
      self.obter_token()
      if self.token is None or self.token['tipo'] != 'identificador':
        self.erro('identificador')
      self.obter_token()
    
    if self.token is None or self.token['valor'] != ')':
      self.erro(')')
    self.obter_token()
  
  # 11 <comando composto>: begin <comando sem rotulo>; {<comando sem rotulo>;} end
  def comando_composto(self):
    if self.token is None or self.token['valor'] != 'begin':
      self.erro('begin')
    self.obter_token()
    while True:
      self.comando_sem_rotulo()
      if self.token is None or self.token['valor'] != ';':
        self.erro(';')
      self.obter_token()
      if self.token is None or self.token['valor'] == 'end':
        break
  
  # 12 <comando sem rotulo>: <atribuicao> | <chamada de procedimento> | <comando condicional> | <comando repetitivo>
  def comando_sem_rotulo(self):
    if self.token is None:
      self.erro('comando sem rotulo')
    if self.token['valor'] in ('write', 'read'):
      self.obter_token()
      if self.token is None or self.token['valor'] != '(':
        self.erro('(')
      self.chamada_procedimento()
    elif self.variavel(): # identificador
      self.obter_token()
      if self.token is not None and self.token['valor'] == ':=':
        self.atribuicao()
      elif self.token is not None and self.token['valor'] == '(':
        self.chamada_procedimento()
      else:
        self.erro('atribuicao ou chamada de procedimento')
    elif self.token['valor'] == 'if':
      self.comando_condicional()
    elif self.token['valor'] == 'while':
      self.comando_repetitivo()
    else:
      self.erro('comando sem rotulo')
  
  # 13 <atribuição>: <variável> := <expressão>
  def atribuicao(self):
    self.expressao()
  
  # 14 <chamada de procedimento>: <identificador> [(<lista de expressões>)]
  def chamada_procedimento(self):
    self.lista_expressoes()
    if self.token is None or self.token['valor'] != ')':
      self.erro(')')
    self.obter_token()
  
  # 15 <comando condicional>: if <expressão> then <comando sem rotulo> [else <comando sem rotulo>]
  def comando_condicional(self):
    self.expressao()
    if self.token is None or self.token['valor'] != 'then':
      self.erro('then')
    self.obter_token()
    self.comando_sem_rotulo()
    if self.token is not None and self.token['valor'] == 'else':
      self.obter_token()
      self.comando_sem_rotulo()
  
  # 16 <comando repetitivo>: while <expressão> do <comando sem rotulo>
  def comando_repetitivo(self):
    self.expressao()
    if self.token is None or self.token['valor'] != 'do':
      self.erro('do')
    self.obter_token()
    self.comando_sem_rotulo()
  
  # 17 <lista de expressões>: <expressão> {, <expressão>}
  def lista_expressoes(self):
    self.expressao()
    while self.token is not None and self.token['valor'] == ',':
      self.expressao()
  
  # 18 <expressão>: <expressão simples> [ <relação> <expressão simples> ]
  def expressao(self):
    self.expressao_simples()
    if self.token is not None and self.relacao():
      self.expressao_simples()
  
  # 19 <relação>: = | < | > | <= | >= | <>
  def relacao(self):
    return self.token['valor'] in ('=', '<', '>', '<=', '>=', '<>')

  # 20 <expressão simples>: [+|-] <termo> {<operador1> <termo>}
  def expressao_simples(self):
    self.obter_token()
    if self.token is not None and self.token['valor'] in ('+', '-'):
      self.obter_token()
    self.termo()
    while self.token is not None and self.operador1():
      self.obter_token()
      self.termo()
  
  # 21 <termo>: <fator> {<operador2> <fator>}
  def termo(self):
    self.fator()
    while self.token is not None and self.operador2():
      self.obter_token()
      self.fator()
  
  # 22 <operador1>: + | - | or
  def operador1(self):
    return self.token['valor'] in ('+', '-', 'or')
  
  # 23 <operador2>: * | div | and
  def operador2(self):
    return self.token['valor'] in ('*', 'div', 'and')
  
  # 24 <fator>: <variável> | <digito> | <chamada de função> | (<expressão>)
  def fator(self):
    if self.token is None:
      self.erro('fator')
    
    if self.token['tipo'] == 'identificador':
      self.chamada_funcao()
    elif self.token['tipo'] == 'digito':
      self.obter_token()
    elif self.token['valor'] == '(':
      self.expressao()
      self.obter_token()
      if self.token is None or self.token['valor'] != ')':
        self.erro(')')
    else:
      self.erro('fator')
      
  # 25 <variável>: <identificador>
  def variavel(self): # 25
    return self.token['tipo'] == 'identificador'
  
  # 26 <chamada de função>: <identificador> [(<lista de expressões>)]
  def chamada_funcao(self):
    self.obter_token()
    if self.token is not None and self.token['valor'] == '(':
      self.lista_expressoes()
      if self.token is None or self.token['valor'] != ')':
        self.erro(')')
      self.obter_token()
        