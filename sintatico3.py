from lexico import main as lexicoMain
import numpy as np
from token_t import TokenClass
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.value[0]) + ": " + repr(self.value[1]) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens.size > 0 else None
        self.syntax_tree = None

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
        self.syntax_tree = TreeNode(("PROGRAM", None))
        self.program(self.syntax_tree)

    def program(self, parent_node):
        """ Regra: Program -> StatementList """
        print("Iniciando análise: Program")
        statement_list_node = TreeNode(("STATEMENT_LIST", None))
        parent_node.add_child(statement_list_node)
        print("Chamando statement_list na função program")
        self.statement_list(statement_list_node)  # Adicionando esta linha para chamar statement_list
        print("Análise de statement_list concluída na função program")

    def statement_list(self, parent_node):
        """ Regra: StatementList -> Statement StatementList | ε """
        print("Iniciando análise: StatementList")
        while self.current_token is not None:
            print("Token atual antes de chamar statement:", self.current_token)
            statement_node = TreeNode(("STATEMENT", None))
            parent_node.add_child(statement_node)
            self.statement(statement_node)
            print("Token atual após chamar statement:", self.current_token)
            # Movendo a chamada para advance para dentro do loop, após adicionar um nó de declaração
            self.advance()
        print("Análise de statement_list concluída")








    def statement(self, parent_node):
        """ Regra: Statement -> Imports | Assignment | Declaration | ForLoop | OtherStatements """
        print("Analisando: Statement")
        print("Token atual:", self.current_token)
        if self.current_token[0] == 'IMPORTS':
            print("Chamando imports")
            self.imports(parent_node)
        elif self.current_token[0] == 'ID':
            print("Chamando assignment")
            self.assignment(parent_node)
        elif self.current_token[0] == 'RESERVED' and self.current_token[1] == 'int':
            print("Chamando declaration")
            self.declaration(parent_node)
        elif self.current_token[0] == 'RESERVED' and self.current_token[1] == 'for':
            print("Chamando for_loop")
            self.for_loop(parent_node)
        else:
            print("Chamando other_statements")
            self.other_statements(parent_node)
        print("Token atual após statement:", self.current_token)




    def imports(self, parent_node):
        """ Regra: Imports -> #include <filename> """
        print("Analisando: Imports")
        imports_node = TreeNode(("IMPORTS", self.current_token[1]))
        parent_node.add_child(imports_node)
        self.consume('IMPORTS')

    def assignment(self, parent_node):
        """ Regra: Assignment -> id = Expression ; """
        print("Analisando: Assignment")
        assignment_node = TreeNode(("ASSIGNMENT", None))
        parent_node.add_child(assignment_node)
        id_node = TreeNode(("ID", self.current_token[1]))
        assignment_node.add_child(id_node)
        self.consume('ID')
        self.consume('SYMBOL')  # Consuming '='
        self.expression(assignment_node)
        self.consume('SYMBOL')  # Consuming ';'

    def declaration(self, parent_node):
        """ Regra: Declaration -> type id ; """
        print("Analisando: Declaration")
        declaration_node = TreeNode(("DECLARATION", None))
        parent_node.add_child(declaration_node)
        self.consume('RESERVED')
        id_node = TreeNode(("ID", self.current_token[1]))
        declaration_node.add_child(id_node)
        self.consume('ID')
        self.consume('SYMBOL')  # Consuming ';'

    def for_loop(self, parent_node):
        """ Regra: ForLoop -> for (Assignment; Condition; Assignment) { StatementList } """
        print("Analisando: ForLoop")
        for_loop_node = TreeNode(("FOR_LOOP", None))
        parent_node.add_child(for_loop_node)
        self.consume('RESERVED')
        self.consume('SYMBOL')
        self.assignment(for_loop_node)
        self.condition(for_loop_node)
        self.consume('SYMBOL')
        self.assignment(for_loop_node)
        self.consume('SYMBOL')
        self.consume('SYMBOL')
        statement_list_node = TreeNode(("STATEMENT_LIST", None))
        for_loop_node.add_child(statement_list_node)
        self.statement_list(statement_list_node)
        self.consume('SYMBOL')

    def condition(self, parent_node):
        """ Regra: Condition -> Expression ComparisonOperator Expression """
        print("Analisando: Condition")
        condition_node = TreeNode(("CONDITION", None))
        parent_node.add_child(condition_node)
        self.expression(condition_node)
        self.consume('SYMBOL')  # Simplificação para exemplo
        self.expression(condition_node)

    def other_statements(self, parent_node):
        """ Placeholder para outras declarações que não estão cobertas pelas regras básicas """
        print(f"Analisando: OtherStatements - {self.current_token}")
        other_statements_node = TreeNode(("OTHER_STATEMENTS", self.current_token[1]))
        parent_node.add_child(other_statements_node)
        self.advance()

    def expression(self, parent_node):
        """ Regra: Expression -> id | number """
        print("Analisando: Expression")
        expression_node = TreeNode(("EXPRESSION", None))
        parent_node.add_child(expression_node)
        if self.current_token[0] == 'ID':
            id_node = TreeNode(("ID", self.current_token[1]))
            expression_node.add_child(id_node)
            self.consume('ID')
        elif self.current_token[0] == 'NUMBER':
            number_node = TreeNode(("NUMBER", self.current_token[1]))
            expression_node.add_child(number_node)
            self.consume('NUMBER')
        else:
            raise SyntaxError(f"Esperado 'ID' ou 'NUMBER', mas encontrou {self.current_token}")

    def print_syntax_tree(self, node=None, indent=0):
        """Imprime a árvore sintática final."""
        if node is None:
            node  = self.syntax_tree
        print("Árvore Sintática:")
        self._print_syntax_tree_recursive(node, indent)

    def _print_syntax_tree_recursive(self, node, indent):
        """Método auxiliar para imprimir a árvore sintática final de forma recursiva."""
        if node:
            print("  " * indent + str(node.value[0]) + ": " + str(node.value[1]))
            for child in node.children:
                self._print_syntax_tree_recursive(child, indent + 1)

def main():
    tokens = lexicoMain()
    parser = Parser(tokens)
    try:
        parser.parse()
        print("Análise sintática concluída com sucesso!")
        print("Árvore sintática:")
        parser.print_syntax_tree()
    except SyntaxError as e:
        print(f"Erro de sintaxe: {e}")

if __name__ == "__main__":
    main()

