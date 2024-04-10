# Importação do módulo rules (contendo as regras de análise léxica)
import rules
# Importação da classe Token do módulo token_t
from token_t import Token

# Definição da classe Lex para análise léxica
class Lex:
    # Método de inicialização da classe Lex
    def __init__(self, content: str, rules: list[rules.RuleInterface]):
        # Atribuição da lista de regras de análise léxica ao atributo rules
        self.rules = rules
        # Atribuição do conteúdo a ser analisado ao atributo content
        self.content = content
    
    # Método para obter o próximo token da análise léxica
    def next(self) -> Token:
        # Verifica se o conteúdo a ser analisado está vazio
        if not self.content:
            # Se estiver vazio, retorna None, indicando o fim da análise léxica
            return None

        # Itera sobre as regras de análise léxica
        for rule in self.rules:
            # Verifica se há correspondência com a regra atual
            match = rule.check_match(self.content)
            # Imprime a regra que está sendo testada e o resultado da correspondência
            print(f'matching rule {rule.__class__.__name__}: {match}')

            # Se não houver correspondência, passa para a próxima regra
            if not match:
                continue

            # Obtém a posição final da correspondência
            endpos = match.span()[1]
            # Atualiza o conteúdo para o próximo token, removendo o token atual e espaços em branco à esquerda
            self.content = self.content[endpos:].lstrip()
            # Retorna o token extraído da correspondência
            return rule.extract_token(match.group(0))
        
        # Se nenhuma regra corresponder, lança uma exceção indicando erro léxico
        raise Exception(f'Lexical Error: symbol {self.content[0]} not recognized')
