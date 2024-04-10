# Importação da classe Lex do módulo lex
from lex import Lex
# Importação do módulo rules (que contém as regras de análise léxica)
import rules

# Abertura do arquivo 'teste-erro.c' em modo de leitura
f = open(r'teste-erro.c')
# Leitura do conteúdo do arquivo
content = f.read()

# Impressão de mensagem indicando o início do parsing do conteúdo
print('parsing content')
# Impressão do conteúdo lido do arquivo
print(content)
# Impressão de novas linhas para separar visualmente o conteúdo
print('\n\n')

# Criação de uma instância da classe Lex para análise léxica, passando o conteúdo e a lista de regras de análise léxica
lex = Lex(content, [ 
    rules.NumberConstantRule(),
    rules.SymbolRule(),
    rules.IdRule(),
    rules.PRRule(),
    rules.ComentRule()])

# Loop infinito para extrair tokens até que não haja mais tokens a serem extraídos
while True:
    # Obtém o próximo token da análise léxica
    token_atual = lex.next()
    # Se não houver mais tokens, interrompe o loop
    if token_atual is None:
        break
    # Impressão do token extraído
    print(f'\nToken extraído: {token_atual}\n\n\n')
