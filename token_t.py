# Importação do módulo Enum do pacote enum
from enum import Enum

# Definição de uma classe Enum chamada TokenClass
class TokenClass(Enum):
    # Definição dos membros da enumeração TokenClass
    NUMERICAL_CONSTANT = 1,
    ID = 2,
    SYMBOL = 3,
    PALAVRA_RESERVADA = 4,
    COMENT = 5

# Definição de uma classe Token
class Token:
    # Método de inicialização da classe Token
    def __init__(self, token_class: TokenClass, token_value):
        # Atribuição do valor do parâmetro token_class ao atributo token_class da instância
        self.token_class = token_class
        # Atribuição do valor do parâmetro token_value ao atributo token_value da instância
        self.token_value = token_value
    # Método para representação da instância como string
    def __str__(self) -> str:
        # Retorna uma string representando a instância
        return f'<Token class: {self.token_class}, Value: {self.token_value}>'
