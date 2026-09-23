import codecs
import re

with codecs.open('src/data/galosDb.ts', 'r', 'utf-8') as f:
    text = f.read()

text = text.replace('turnos?: number;\n};', 'turnos?: number;\n  isEvoluida?: boolean;\n};')

# Replace `31: {"nome": "..."}` with `30: {"isEvoluida": true, "nome": "..."}`
# Some might be 31: { "nome": ... }
text = re.sub(r'31:\s*\{', '30: {"isEvoluida": true, ', text)

with codecs.open('src/data/galosDb.ts', 'w', 'utf-8') as f:
    f.write(text)
print("Done DB")

