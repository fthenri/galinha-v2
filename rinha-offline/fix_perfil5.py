import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

text = text.replace('import { useState } from "react";\n\nexport default function Perfil() {', 'export default function Perfil() {')
if 'import { useState }' not in text:
    text = 'import { useState } from "react";\n' + text

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done import")

