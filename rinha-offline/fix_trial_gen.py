import codecs
import re

with codecs.open('src/components/ModoTrial.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Replace the generation logic
regex = r'const dificuldade = difRinhaRef\.current;[\s\S]*?const pesoInimigo = PESOS_RARIDADE\[dadosInimigo\.raridade \|\| "Common"\] \|\| 1;'
replacement = '''const nomeSorteado = meuGalo.nome;
            const dadosInimigo = GALOS_DB[meuGalo.nome];'''

text = re.sub(regex, replacement, text)

# Remove `isTrial = true` and `if (isTrial)` branches, just use the true branch logic directly to make it clean
# Actually the true branch sets `nivelInimigo = calcularNivelInimigoTrial(trialsAtualLoop);`
# But let's check what's there
with codecs.open('src/components/ModoTrial.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done enemy generation fix")

