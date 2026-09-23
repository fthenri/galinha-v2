import codecs

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

text = text.replace(
    'export default function Perfil() {\n  const { nome, moedas, galoCoins, galos, galoAtivoIndex, setGaloAtivo } = useJogadorStore();',
    'import { useState } from "react";\n\nexport default function Perfil() {\n  const { nome, moedas, galoCoins, galos, galoAtivoIndex, setGaloAtivo } = useJogadorStore();\n  const [modalEvolucao, setModalEvolucao] = useState<number | null>(null);\n  const [modalRebirth, setModalRebirth] = useState<number | null>(null);'
)

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done state fix")

