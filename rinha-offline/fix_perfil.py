import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

if "import { META_TIPOS" not in text:
    text = text.replace("import { GALOS_DB } from '../data/galosDb';", "import { GALOS_DB } from '../data/galosDb';\nimport { META_TIPOS } from '../data/tiposDb';")

regex = r'<span className="px-2 py-1 rounded-md text-xs font-bold bg-zinc-900 text-zinc-300">Tipo: \{galo\.tipo\}</span>'
good = '''<span className={`px-2 py-1 rounded-md text-xs font-bold ${META_TIPOS[galo.tipo]?.corFundo || 'bg-zinc-900'} ${META_TIPOS[galo.tipo]?.corTexto || 'text-zinc-300'}`}>
          {META_TIPOS[galo.tipo]?.icone || ''} {galo.tipo}
        </span>'''

text = re.sub(regex, good, text)

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done with Perfil")

