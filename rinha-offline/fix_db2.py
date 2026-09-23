import codecs
import re

with codecs.open('src/data/galosDb.ts', 'r', 'utf-8') as f:
    text = f.read()

text = text.replace('turnos?: number;\n};', 'turnos?: number;\n  isEvoluida?: boolean;\n};')

# Restore the duplicate 30 back to `"30_evo"`
# Before we replaced `31:\s*\{` with `30: {"isEvoluida": true, `
# So now we have `30: {"isEvoluida": true, `
text = text.replace('30: {"isEvoluida": true, ', '"30_evo": {"isEvoluida": true, ')

with codecs.open('src/data/galosDb.ts', 'w', 'utf-8') as f:
    f.write(text)
print("Done DB")

