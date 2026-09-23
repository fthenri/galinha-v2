import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

if "import { calcularMultiplicadorRebirth" not in text:
    text = text.replace("import { useJogadorStore } from '../store/jogadorStore';", "import { useJogadorStore, calcularMultiplicadorRebirth } from '../store/jogadorStore';")

bad_line = 'meuGalo.hp_max = (GALOS_DB[meuGalo.nome]?.hp_base || 100) + ((meuGalo.nivel - 1) * 12);'
good_line = 'meuGalo.hp_max = Math.floor(((GALOS_DB[meuGalo.nome]?.hp_base || 100) + ((meuGalo.nivel - 1) * 12)) * calcularMultiplicadorRebirth(meuGalo.rebirths || 0));'

if bad_line in text:
    text = text.replace(bad_line, good_line)
    
with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done Rinha")

