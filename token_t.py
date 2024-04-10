# Importação da classe Enum do módulo enum
from enum import Enum

# Definição da classe TokenClass que herda de Enum
class TokenClass(Enum):
    # Definição dos membros da enumeração TokenClass com seus valores
    NUMERICAL_CONSTANT = 1,  # Constante numérica
    ID = 2,                   # Identificador
    SYMBOL = 3,               # Símbolo
    RESERVED = 4              # Palavra reservada

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