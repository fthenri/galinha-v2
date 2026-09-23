import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Fix `onOpenEvolucao` etc never read because `GaloCard` didn't have its body updated!
body_regex = r'(<button\s*onClick=\{[^}]+\}\s*disabled=\{galo\.nivel < calcularNivelRebirth\(galo\.rebirths \|\| 0\)\}[^>]+>\s*Rebirth[^<]+</button>)'
new_btns = '''      <button
        onClick={() => onOpenRebirth(galoIndex)}
        className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold py-2 rounded-lg mt-4 w-full hover:from-purple-500 hover:to-indigo-500 shadow-lg transition-all"
      >
        Rebirth
      </button>
      <button
        onClick={() => onOpenEvolucao(galoIndex)}
        className="bg-gradient-to-r from-amber-500 to-yellow-600 text-black font-bold py-2 rounded-lg mt-2 w-full hover:from-amber-400 hover:to-yellow-500 shadow-lg transition-all"
      >
        Evolução
      </button>'''

text = re.sub(body_regex, new_btns, text)

# Fix `<GaloCard` usage in `Perfil`
text = re.sub(
    r'(onEquipar=\{\(\) => setGaloAtivo\(idx\)\})([^\w]*)/>',
    r'\1\n            onOpenEvolucao={setModalEvolucao}\n            onOpenRebirth={setModalRebirth}\n          />',
    text
)

# Fix states in `Perfil`
if 'const [modalEvolucao, setModalEvolucao] = useState<number | null>(null);' not in text:
    text = re.sub(
        r'export default function Perfil\(\) \{\n\s*const \{ nome, moedas, galoCoins, galos, galoAtivoIndex, setGaloAtivo \} = useJogadorStore\(\);',
        r'import { useState } from "react";\n\nexport default function Perfil() {\n  const { nome, moedas, galoCoins, galos, galoAtivoIndex, setGaloAtivo } = useJogadorStore();\n  const [modalEvolucao, setModalEvolucao] = useState<number | null>(null);\n  const [modalRebirth, setModalRebirth] = useState<number | null>(null);',
        text
    )

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done fix galocard body and usage")

