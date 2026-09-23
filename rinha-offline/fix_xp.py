import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

text = re.sub(
    r'const xpGanho = Math\.floor\(configDif\.calcXp\(xpBase\)\);\s*const moedasGanhas = 6;',
    r'const xpGanho = Math.floor(configDif.calcXp(xpBase) * (1 + (itemMods.xpBonus || 0)));\n                    const moedasGanhas = 6 + (itemMods.dinheiroBonus || 0);',
    text
)

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done xp fix")

