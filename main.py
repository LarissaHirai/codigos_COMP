from lex import Lex
import rules

f = open(r'teste-erro.c')
content = f.read()

print('parsing content')
print (content)
print ('\n\n')

lex = Lex(content, [ \
    rules.NumberConstantRule(), \
    rules.SymbolRule(), \
    rules.IdRule() ])

while True:
    token_atual = lex.next()
    if token_atual is None:
        break
    print(f'\ntoken extraido: {token_atual}\n\n\n')