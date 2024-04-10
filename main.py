# Importação da classe Lex do módulo lex
from lex import Lex
# Importação do módulo rules (que contém as regras de análise léxica)
import rules

# Abertura do arquivo 'teste-erro.c' em modo de leitura
f = open(r'teste-erro.c')
# Leitura do conteúdo do arquivo e atribuição à variável content
content = f.read()

# Impressão de mensagem indicando o início do parsing do conteúdo
print('parsing content')
# Impressão do conteúdo lido do arquivo
print(content)
# Impressão de novas linhas para separar visualmente o conteúdo
print('\n\n')

# Criação de uma instância da classe Lex para análise léxica, passando o conteúdo e uma lista de regras de análise léxica
# As regras incluem NumberConstantRule, SymbolRule, ReservedRule e IdRule
# As regras são passadas como uma lista, onde cada regra é inicializada e adicionada à lista dentro de colchetes
# As barras invertidas (\) são usadas para indicar a continuação da linha
lex = Lex(content, [
    rules.NumberConstantRule(),  # Regra para constantes numéricas
    rules.SymbolRule(),          # Regra para símbolos
    rules.ReservedRule(),        # Regra para palavras reservadas
    rules.IdRule() ])               # Regra para identificadores

# Loop infinito para extrair tokens até que não haja mais tokens a serem extraídos
while True:
    # Obtém o próximo token da análise léxica
    token_atual = lex.next()
    # Verifica se o token atual é None, indicando o fim da análise léxica
    if token_atual is None:
        # Se for None, sai do loop
        break
    # Impressão do token extraído
    print(f'\nToken extraido: {token_atual}\n')
