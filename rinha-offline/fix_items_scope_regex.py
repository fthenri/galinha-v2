import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Add it exactly at the start of iniciarLoop
text = re.sub(
    r'(const iniciarLoop = async \(\) => \{)',
    r'\1\n        const itemMods = meuGalo.item_equipado ? ITENS_DB[meuGalo.item_equipado]?.modificadores || {} : {};',
    text
)

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done item integration fix regex")

