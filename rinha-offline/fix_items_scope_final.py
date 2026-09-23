import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Remove itemMods from anywhere inside
text = re.sub(r'\s*const itemMods = meuGalo\.item_equipado \? ITENS_DB\[meuGalo\.item_equipado\]\?\.modificadores \|\| \{\} : \{\};', '', text)

# Add it exactly at the start of iniciarLoop
text = text.replace(
    'const iniciarLoop = async () => {\n        // Inicializar hp atual igual ao max\n',
    'const iniciarLoop = async () => {\n        // Inicializar hp atual igual ao max\n        const itemMods = meuGalo.item_equipado ? ITENS_DB[meuGalo.item_equipado]?.modificadores || {} : {};\n'
)

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done item integration fix final")

