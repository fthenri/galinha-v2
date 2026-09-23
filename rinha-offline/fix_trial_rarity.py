import codecs
import re

with codecs.open('src/components/ModoTrial.tsx', 'r', 'utf-8') as f:
    text = f.read()

old_gen = '''            const nomeSorteado = meuGalo.nome;
            const dadosInimigo = GALOS_DB[meuGalo.nome];'''

new_gen = '''            const raridadeJogador = GALOS_DB[meuGalo.nome]?.raridade || "Common";
            const galosPermitidos = Object.keys(GALOS_DB).filter(nome => (GALOS_DB[nome]?.raridade || "Common") === raridadeJogador);
            
            const nomeSorteado = galosPermitidos.length > 0 
                ? galosPermitidos[Math.floor(Math.random() * galosPermitidos.length)] 
                : meuGalo.nome;
                
            const dadosInimigo = GALOS_DB[nomeSorteado];'''

text = text.replace(old_gen, new_gen)

with codecs.open('src/components/ModoTrial.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done trial generation update")

