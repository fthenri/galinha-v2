import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Fix handleModoClick for Raid
text = text.replace(
    "if (modo === 'Dungeon' || modo === 'Arena' || modo === 'Survival') {",
    "if (modo === 'Raid' || modo === 'Dungeon' || modo === 'Arena' || modo === 'Survival') {"
)

text = re.sub(r"\} else if \(modo === 'Raid'\) \{\s*setModoAtivo\('raid'\);\s*\}", "", text)

# Remove the unused if (modoAtivo === 'raid') block
text = re.sub(r"if \(modoAtivo === 'raid'\) \{\s*return \([\s\S]*?\);\s*\}", "", text)

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done Rinha Raid fix")

