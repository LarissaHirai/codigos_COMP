# Importação da classe Enum do módulo enum
from enum import Enum

# Definição da classe TokenClass que herda de Enum
class TokenClass(Enum):
    # Definição dos membros da enumeração TokenClass com seus valores
    COMMENTARY = 1,          # Comentário
    IMPORTS = 2,
    NUMERICAL_CONSTANT = 3,  # Constante numérica
    ID = 4,                   # Identificador
    SYMBOL = 5,               # Símbolo
    RESERVED = 6           # Palavra reservada
       

# Definição da classe Token
class Token:
    # Método de inicialização da classe Token
    def __init__(self, token_class: TokenClass, token_value):
        # Atribuição da classe do token ao atributo token_class
        self.token_class = token_class
        # Atribuição do valor do token ao atributo token_value
        self.token_value = token_value
    # Método para representar a instância como uma string
    def __str__(self) -> str:
        # Retorna uma string representando a instância
        return f'<Token class: {self.token_class}, value: {self.token_value} >'
