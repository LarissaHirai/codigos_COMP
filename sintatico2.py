from lexico import main as lexicoMain
import numpy as np
from token_t import TokenClass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens.size > 0 else None

    def advance(self):
        """ Avança para o próximo token """
        self.current_token_index += 1
        if self.current_token_index < self.tokens.shape[0]:
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None
        print(f"Avançando para o próximo token: {self.current_token}")

    def consume(self, expected_class):
        """ Consome o token atual se ele for do tipo esperado """
        expected_class = str(expected_class)  # Assegura que expected_class é uma string
        actual_class = str(self.current_token[0]) if self.current_token is not None else None
        print(f"Esperado: {expected_class}, Encontrado: {actual_class}")
        if self.current_token is not None and self.current_token[0] == expected_class:
            self.advance()
        else:
            raise SyntaxError(f"Esperado token {expected_class}, mas encontrou {self.current_token}")

    def parse(self):
        """ Inicia a análise sintática """
        self.program()

    def program(self):
        """ Regra: Program -> StatementList """
        print("Iniciando análise: Program")
        self.statement_list()

    def statement_list(self):
        """ Regra: StatementList -> Statement StatementList | ε """
        print("Iniciando análise: StatementList")
        while self.current_token is not None:
            self.statement()

    def statement(self):
        """ Regra: Statement -> Imports | Assignment | Declaration | ForLoop | OtherStatements """
        print("Analisando: Statement")
        if self.current_token[0] == 'IMPORTS':
            self.imports()
        elif self.current_token[0] == 'ID':
            self.assignment()
        elif self.current_token[0] == 'RESERVED' and self.current_token[1] == 'int':
            self.declaration()
        elif self.current_token[0] == 'RESERVED' and self.current_token[1] == 'for':
            self.for_loop()
        else:
            self.other_statements()

    def imports(self):
        """ Regra: Imports -> #include <filename> """
        print("Analisando: Imports")
        self.consume('IMPORTS')

    def assignment(self):
        """ Regra: Assignment -> id = Expression ; """
        print("Analisando: Assignment")
        self.consume('ID')
        self.consume('SYMBOL')  # Consuming '='
        self.expression()
        self.consume('SYMBOL')  # Consuming ';'

    def declaration(self):
        """ Regra: Declaration -> type id ; """
        print("Analisando: Declaration")
        self.consume('RESERVED')
        self.consume('ID')
        self.consume('SYMBOL')  # Consuming ';'

    def for_loop(self):
        """ Regra: ForLoop -> for (Assignment; Condition; Assignment) { StatementList } """
        print("Analisando: ForLoop")
        self.consume('RESERVED')
        self.consume('SYMBOL')
        self.assignment()
        self.condition()
        self.consume('SYMBOL')
        self.assignment()
        self.consume('SYMBOL')
        self.consume('SYMBOL')
        self.statement_list()
        self.consume('SYMBOL')

    def condition(self):
        """ Regra: Condition -> Expression ComparisonOperator Expression """
        print("Analisando: Condition")
        self.expression()
        self.consume('SYMBOL')  # Simplificação para exemplo
        self.expression()

    def other_statements(self):
        """ Placeholder para outras declarações que não estão cobertas pelas regras básicas """
        print(f"Analisando: OtherStatements - {self.current_token}")
        self.advance()

    def expression(self):
        """ Regra: Expression -> id | number """
        print("Analisando: Expression")
        if self.current_token[0] == 'ID':
            self.consume('ID')
        elif self.current_token[0] == 'NUMBER':
            self.consume('NUMBER')
        else:
            raise SyntaxError(f"Esperado 'ID' ou 'NUMBER', mas encontrou {self.current_token}")

# Função principal para executar o analisador sintático
def main():
    tokens = lexicoMain()
    parser = Parser(tokens)
    try:
        parser.parse()
        print("Análise sintática concluída com sucesso!")
    except SyntaxError as e:
        print(f"Erro de sintaxe: {e}")

if __name__ == "__main__":
    main()
