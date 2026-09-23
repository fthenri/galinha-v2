import codecs
import re

with codecs.open('src/components/Loja.tsx', 'r', 'utf-8') as f:
    text = f.read()

if "import { META_TIPOS" not in text:
    text = text.replace("import { GALOS_DB } from '../data/galosDb';", "import { GALOS_DB } from '../data/galosDb';\nimport { META_TIPOS } from '../data/tiposDb';")

regex = r'<span className="text-xl text-amber-500 font-bold mb-6">\{galoSorteado\.tipo\}</span>'
good = '''<span className={`px-4 py-2 rounded-md text-xl font-bold mb-6 ${META_TIPOS[galoSorteado.tipo]?.corFundo || 'bg-zinc-800'} ${META_TIPOS[galoSorteado.tipo]?.corTexto || 'text-amber-500'}`}>
              {META_TIPOS[galoSorteado.tipo]?.icone || ''} {galoSorteado.tipo}
            </span>'''

text = re.sub(regex, good, text)

with codecs.open('src/components/Loja.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done with Loja")

