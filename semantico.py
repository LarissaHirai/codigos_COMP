from lexico import main as lexicoMain
import numpy as np
from token_t import TokenClass


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
    
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def declare_variable(self, name, var_type):
        if name in self.symbol_table:
            raise SemanticError(f"Variável '{name}' já declarada.")
        self.symbol_table[name] = var_type
        print(f"Declarada variável: {name} do tipo {var_type}")

    def use_variable(self, name):
        if name not in self.symbol_table:
            raise SemanticError(f"Variável '{name}' não declarada.")
        print(f"Variável usada: {name} do tipo {self.symbol_table[name]}")

    def check_assignment(self, name, expression_type):
        if name not in self.symbol_table:
            raise SemanticError(f"Variável '{name}' não declarada.")
        if self.symbol_table[name] != expression_type:
            raise SemanticError(f"Tipo de dados incompatível em atribuição para variável '{self.symbol_table[name]}'.")
        
    def check_variable_type(self, name):
        print(f'Tipo: {self.symbol_table[name]}')
        return self.symbol_table[name]
        
class SemanticError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens.size > 0 else None
        self.syntax_tree = None
        self.semantic_analyzer = SemanticAnalyzer()
        self.declared_variables = set()

    def is_variable_declared(self, var_name):
        """ Verifica se a variável foi declarada anteriormente """
        return var_name in self.declared_variables

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
            if self.current_token is not None:
                raise SyntaxError(f"Esperado token {expected_class}, mas encontrou {self.current_token}")
            else:
                print("Fim dos tokens")


    def parse(self):
        """ Inicia a análise sintática """
        self.syntax_tree = TreeNode(("PROGRAM", None))
        self.program(self.syntax_tree)

    def program(self, parent_node):
        """ Regra: Program -> StatementList """
        print("Iniciando análise: Program")
        print("Chamando statement_list na função program")
        statement_list_node = TreeNode(("STATEMENT_LIST", None))
        parent_node.add_child(statement_list_node)
        self.statement_list(statement_list_node)
        print("Análise de statement_list concluída na função program")

    def statement_list(self, parent_node):
        """ Regra: StatementList -> Statement StatementList | ε """
        print("Iniciando análise: StatementList")
        while self.current_token is not None:
            statement_node = TreeNode(("STATEMENT", None))
            parent_node.add_child(statement_node)
            self.statement(statement_node)
        print("Análise de statement_list concluída")


    def statement(self, parent_node):
        """ Regra: Statement -> Imports | FunctionDeclaration | Assignment | Declaration | ForLoop | OtherStatements """
        print("Analisando: Statement")
        print("Token atual:", self.current_token)
        if self.current_token[0] == 'IMPORTS':
            print("Chamando imports")
            self.imports(parent_node)
        elif self.current_token[0] == 'RESERVED' and self.current_token[1] == 'void':
            print("Chamando function_declaration")
            self.function_declaration(parent_node)
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
        print("Token atual após imports:", self.current_token)

    def function_declaration(self, parent_node):
        """ Regra: FunctionDeclaration -> void id ( ) { StatementList } """
        print("Analisando: FunctionDeclaration")
        func_decl_node = TreeNode(("FUNCTION_DECLARATION", None))
        parent_node.add_child(func_decl_node)
        self.consume('RESERVED')  # Consome 'void'
        func_name = self.current_token[1]
        func_name_node = TreeNode(("ID", func_name))
        func_decl_node.add_child(func_name_node)
        self.consume('ID')
        self.consume('SYMBOL')  # Consome '('
        self.consume('SYMBOL')  # Consome ')'
        self.consume('SYMBOL')  # Consome '{'
        statement_list_node = TreeNode(("STATEMENT_LIST", None))
        func_decl_node.add_child(statement_list_node)
        self.statement_list(statement_list_node)
        self.consume('SYMBOL')  # Consome '}'
        print("Token atual após function_declaration:", self.current_token)

    def assignment(self, parent_node):
        """ Regra: Assignment -> id = Expression ; """
        print("Analisando: Assignment")
        assignment_node = TreeNode(("ASSIGNMENT", None))
        parent_node.add_child(assignment_node)
        var_name = self.current_token[1]
        print(f'varname: {var_name}')
        id_node = TreeNode(("ID", var_name))
        assignment_node.add_child(id_node)
        self.semantic_analyzer.use_variable(var_name)
        self.consume('ID')
        print(f'current {self.current_token[0]}')
        self.consume('SYMBOL')  # Consuming '=' or '+-'
        if self.current_token[0]=='SYMBOL':
            print("Aqui")
            self.consume('SYMBOL') # Consuming '+-'
        else: 
            print("Aqui2")
            expr_type = self.expression(assignment_node)
            print(f'exprtype: {expr_type}')
            self.consume('SYMBOL')  # Consuming ';'
            self.semantic_analyzer.check_assignment(var_name, expr_type)
        print("Token atual após assignment:", self.current_token)

    
    

    def declaration(self, parent_node):
        """ Regra: Declaration -> type id [= Expression] ; """
        print("Analisando: Declaration")
        declaration_node = TreeNode(("DECLARATION", None))
        parent_node.add_child(declaration_node)
        var_type = self.current_token[1]
        self.consume('RESERVED')  # Consome 'int'
        var_name = self.current_token[1]
        id_node = TreeNode(("ID", var_name))
        declaration_node.add_child(id_node)
        self.consume('ID')

        # Verifica se há uma atribuição opcional
        if self.current_token is not None and self.current_token[0] == 'SYMBOL' and self.current_token[1] == '=':
            self.consume('SYMBOL')  # Consome '='
            self.expression(declaration_node)

        self.consume('SYMBOL')  # Consome ';'
        self.semantic_analyzer.declare_variable(var_name, var_type)

    def for_loop(self, parent_node):
        """ Regra: ForLoop -> for (Declaration; Condition; Assignment) { StatementList } """
        print("Analisando: ForLoop")
        for_loop_node = TreeNode(("FOR_LOOP", None))
        parent_node.add_child(for_loop_node)
        self.consume('RESERVED')  # Consome 'for'
        self.consume('SYMBOL')  # Consome '('

        # Verifica se é uma declaração de variável dentro do for
        if self.current_token[0] == 'RESERVED' and self.current_token[1] == 'int':
            self.declaration(for_loop_node)
        else:
            self.assignment(for_loop_node)

        # Aqui não consome ';' porque já é consumido na declaração ou atribuição

        self.condition(for_loop_node)
        self.consume('SYMBOL')  # Consome ';'
        self.assignment(for_loop_node)
        self.consume('SYMBOL')  # Consome ')'
        self.consume('SYMBOL')  # Consome '{'
        statement_list_node = TreeNode(("STATEMENT_LIST", None))
        for_loop_node.add_child(statement_list_node)
        self.statement_list(statement_list_node)
        self.consume('SYMBOL')  # Consome '}'



    def condition(self, parent_node):
        """ Regra: Condition -> Expression ComparisonOperator Expression """
        print("Analisando: Condition")
        condition_node = TreeNode(("CONDITION", None))
        parent_node.add_child(condition_node)
        expr_type_left = self.expression(condition_node)
        
        if self.current_token is not None and self.current_token[0] in ['SYMBOL', 'RESERVED']:
            comparison_op_node = TreeNode(("COMPARISON_OPERATOR", self.current_token[1]))
            condition_node.add_child(comparison_op_node)
            self.consume(self.current_token[0])
        else:
            raise SyntaxError(f"Operador de comparação esperado, encontrado: {self.current_token}")
        
        expr_type_right = self.expression(condition_node)
        
        # Aqui você pode realizar a verificação semântica se necessário
        
        print("Token atual após condition:", self.current_token)

    def other_statements(self, parent_node):
        """ Placeholder para outras declarações que não estão cobertas pelas regras básicas """
        print(f"Analisando: OtherStatements - {self.current_token}")
        other_statements_node = TreeNode(("OTHER_STATEMENTS", self.current_token[1]))
        parent_node.add_child(other_statements_node)
        self.advance()
        print("Token atual após other_statements:", self.current_token)

    def expression(self, parent_node):
        """ Regra: Expression -> id | number | ε """
        print("Analisando: Expression")
        expression_node = TreeNode(("EXPRESSION", None))
        parent_node.add_child(expression_node)
        
        if self.current_token is None:
            print("Expressão vazia")
            return None
        
        if self.current_token[0] == 'ID':
            var_name = self.current_token[1]
            id_node = TreeNode(("ID", var_name))
            expression_node.add_child(id_node)          
                   
            tipo = self.semantic_analyzer.check_variable_type(self.current_token[1])
            print(f'tipo {tipo}')
            self.consume('ID')

            return tipo  # Expressão com ID retorna None        
        elif self.current_token[0] == 'NUMERICAL_CONSTANT':
            number_node = TreeNode(("NUMBER", self.current_token[1]))
            expression_node.add_child(number_node)
            self.consume('NUMERICAL_CONSTANT')
            return 'int'  # Assumindo que todos os números são inteiros            
        else:
            print(f'token: {self.current_token[0]}')
            print("Token atual após expression:", self.current_token)
            #print("Token inesperado encontrado:", self.current_token)
            return

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

    def generate_machine_code(self):
        machine_code = []
        self.traverse_and_generate(self.syntax_tree, machine_code)
        return machine_code

    def traverse_and_generate(self, node, machine_code):
        if node.value[0] == "PROGRAM":
            for child in node.children:
                self.traverse_and_generate(child, machine_code)
        elif node.value[0] == "IMPORTS":
            import_statement = f"IMPORT {node.value[1]}"
            machine_code.append(import_statement)
        elif node.value[0] == "FUNCTION_DECLARATION":
            func_name = node.children[0].value[1]
            machine_code.append(f"DECLARE FUNCTION {func_name}")
            if len(node.children) > 1:
                self.traverse_and_generate(node.children[1], machine_code)
        elif node.value[0] == "ASSIGNMENT":
            var_name = node.children[0].value[1]
            if len(node.children) > 1:
                self.traverse_expression(node.children[1], machine_code)
                machine_code.append(f"STORE {var_name}")
        elif node.value[0] == "DECLARATION":
            var_name = node.children[0].value[1]
            var_type = node.value[1]
            if len(node.children) > 1:
                self.traverse_expression(node.children[1], machine_code)
                machine_code.append(f"STORE {var_name}")
        elif node.value[0] == "FOR_LOOP":
            if len(node.children) > 0:
                self.traverse_and_generate(node.children[0], machine_code)  # Declaração ou Atribuição inicial
            if len(node.children) > 1:
                self.traverse_and_generate(node.children[1], machine_code)  # Condição
            if len(node.children) > 2:
                self.traverse_and_generate(node.children[2], machine_code)  # Atribuição
            if len(node.children) > 3:
                self.traverse_and_generate(node.children[3], machine_code)  # Lista de instruções dentro do for
        elif node.value[0] == "STATEMENT":
            for child in node.children:
                self.traverse_and_generate(child, machine_code)
        elif node.value[0] == "STATEMENT_LIST":
            for child in node.children:
                self.traverse_and_generate(child, machine_code)
        elif node.value[0] == "OTHER_STATEMENTS":
            statement_type = node.value[1]
            if statement_type == ';':
                machine_code.append("NOP")  # Comando vazio
            elif statement_type == '{':
                machine_code.append("BEGIN_BLOCK")  # Início de bloco
            elif statement_type == '}':
                machine_code.append("END_BLOCK")  # Fim de bloco
        elif node.value[0] == "CONDITION":
            self.traverse_and_generate(node.children[0], machine_code)  # Primeira expressão
            machine_code.append(node.children[1].value[0])  # Operador de comparação
            self.traverse_and_generate(node.children[2], machine_code)  # Segunda expressão
        elif node.value[0] == "EXPRESSION":
            for child in node.children:
                self.traverse_expression(child, machine_code)  # Lidar com cada child da expressão
            
        else:
            print(f"Tipo de nó não reconhecido: {node.value}")

    def traverse_expression(self, node, machine_code):
        if node.value[0] == "EXPRESSION":
            for child in node.children:
                self.traverse_expression(child, machine_code)  # Lidar com cada child da expressão
            if node.value[1] is not None:
                machine_code.append(node.value[1])  # Adicionar operador ou tipo de expressão
        elif node.value[0] == "ID":
            machine_code.append(f"LOAD {node.value[1]}")  # Carregar variável
        elif node.value[0] == "NUMBER":
            machine_code.append(node.value[1])  # Adicionar o número ao código de máquina
        else:
            print("AQUIASDASJ")
            if node.value[1] is not None:
                if node.value[1] == "=":
                    machine_code.append("STORE")  # Atribuição
                elif node.value[1] == "+":
                    machine_code.append("ADD")  # Adição
                elif node.value[1] == "-":
                    machine_code.append("SUB")  # Subtração
                elif node.value[1] == "*":
                    machine_code.append("MUL")  # Multiplicação
                elif node.value[1] == "/":
                    machine_code.append("DIV")  # Divisão
                else:
                    machine_code.append(node.value[1])
            machine_code.append(node.value[0])  # Adicionar operador ao código de máquina
        


def main():
    tokens = lexicoMain()
    parser = Parser(tokens)
    try:
        parser.parse()
        print("Análise sintática e semântica concluída com sucesso!")
        parser.print_syntax_tree()
        codigo=parser.generate_machine_code()
        print("codigo", codigo)

    except (SyntaxError, SemanticError) as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()

