import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
with codecs.open('src/components/ModoTrial.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Remove `calcularNivelInimigoTrial` from imports
text = text.replace(', calcularNivelInimigoTrial', '')
# Remove unused imports and vars
text = text.replace("import { PESOS_RARIDADE, CONFIG_DIFICULDADE } from '../data/dificuldadeDb';", "import { CONFIG_DIFICULDADE } from '../data/dificuldadeDb';")
text = text.replace("            const isTrial = true;\n", "")

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
with codecs.open('src/components/ModoTrial.tsx', 'w', 'utf-8') as f:
    f.write(text)

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text_rinha = f.read()

# Add explicit type Galo to atacante and defensor
text_rinha = text_rinha.replace('const atacante = turnoJogador ? meuGalo : novoInimigo;', 'const atacante: Galo = turnoJogador ? meuGalo : novoInimigo;')
text_rinha = text_rinha.replace('const defensor = turnoJogador ? novoInimigo : meuGalo;', 'const defensor: Galo = turnoJogador ? novoInimigo : meuGalo;')

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text_rinha)

print("Done fixing TS errors")

print("Done ts fixes")
