import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Insert the states after useJogadorStore();
state_vars = '''
  const [modalEvolucao, setModalEvolucao] = useState<number | null>(null);
  const [modalRebirth, setModalRebirth] = useState<number | null>(null);'''
  
if 'const [modalEvolucao, setModalEvolucao] = useState' not in text:
    text = re.sub(
        r'(const \{[^}]+\} = useJogadorStore\(\);)',
        r'\1' + state_vars,
        text
    )

# Make sure useState is imported
if 'import { useState } from "react";' not in text:
    text = 'import { useState } from "react";\n' + text

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done state fix final")

