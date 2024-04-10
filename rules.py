# Importação do módulo re (expressões regulares)
import re
# Importação das classes Token e TokenClass do módulo token_t
from token_t import Token, TokenClass

# Definição da classe abstrata RuleInterface
class RuleInterface:
    # Método abstrato para retornar regras de expressões regulares
    def regex_rules(self) -> list[str]:
        pass
    # Método abstrato para extrair token de um padrão correspondente
    def extract_token(self, match: str) -> Token:
        pass
    # Método para verificar correspondência de padrão em um conteúdo
    def check_match(self, content: str) -> re.Match:
        # Itera sobre as regras de expressões regulares
        for rule in self.regex_rules():
            # Tenta encontrar uma correspondência no início do conteúdo
            match = re.match('^' + rule, content)
            # Se encontrar uma correspondência, retorna o objeto de correspondência
            if match:
                return match
        # Se nenhuma correspondência for encontrada, retorna None
        return None

# Definição da classe NumberConstantRule que herda de RuleInterface
class NumberConstantRule(RuleInterface):
    # Método para retornar regras de expressões regulares para constantes numéricas
    def regex_rules(self) -> list[str]:
        return ['[0-9]+', '[0-9]+.[0-9+]']
    # Método para extrair token de uma correspondência de regra de constante numérica
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.NUMERICAL_CONSTANT, int(match))

# Definição da classe IdRule que herda de RuleInterface
class IdRule(RuleInterface):
    # Método para retornar regras de expressões regulares para identificadores
    def regex_rules(self) -> list[str]:
        return ['[a-zA-Z_][a-zA-Z0-9_]*']
    # Método para extrair token de uma correspondência de regra de identificador
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.ID, match)

# Definição da classe SymbolRule que herda de RuleInterface
class SymbolRule(RuleInterface):
    # Método para retornar regras de expressões regulares para símbolos
    def regex_rules(self) -> list[str]:
        return ['\\{', '\\}', '\\(', '\\)', '\\+', '-', '\\*', '/','\\#','\\<','\\>','\\.','\\"','\\!','\\;', '\\=']
    # Método para extrair token de uma correspondência de regra de símbolo
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.SYMBOL, match)

# Definição da classe PRRule que herda de RuleInterface
class PRRule(RuleInterface):
    # Método para retornar regras de expressões regulares para palavras reservadas
    def regex_rules(self) -> list[str]:
        return ['\\struct', '\\if', '\\int', '\\lse', '\\while', '\\do', '\\for', '\\float', '\\double', '\\char', '\\long', '\\short', '\\break', '\\continue', '\\case', '\\switch', '\\deafult', '\\void', '\\return']
    # Método para extrair token de uma correspondência de regra de palavra reservada
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.PALAVRA_RESERVADA, match)

# Definição da classe ComentRule que herda de RuleInterface
class ComentRule(RuleInterface):
    # Método para retornar regras de expressões regulares para comentários
    def regex_rules(self) -> list[str]:
        return ['\\*/', '\\/*', '\\//']
    # Método para extrair token de uma correspondência de regra de comentário
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.COMENT, match)
