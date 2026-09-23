import codecs
import re

# 1. CODEX
with codecs.open('src/components/Codex.tsx', 'r', 'utf-8') as f:
    text_codex = f.read()

if "import { META_TIPOS" not in text_codex:
    text_codex = text_codex.replace("import { SISTEMA_TIPOS } from '../data/tiposDb';", "import { SISTEMA_TIPOS, META_TIPOS } from '../data/tiposDb';")

# Replace <span className="px-3 py-1 rounded-md text-sm font-bold bg-zinc-800 text-zinc-300">{galo.tipo}</span>
regex_codex_tipo = r'<span className="px-3 py-1 rounded-md text-sm font-bold bg-zinc-800 text-zinc-300">\s*\{galo\.tipo\}\s*</span>'
good_codex_tipo = '''<span className={`px-3 py-1 rounded-md text-sm font-bold ${META_TIPOS[galo.tipo]?.corFundo || 'bg-zinc-800'} ${META_TIPOS[galo.tipo]?.corTexto || 'text-zinc-300'}`}>
                {META_TIPOS[galo.tipo]?.icone || ''} {galo.tipo}
              </span>'''
text_codex = re.sub(regex_codex_tipo, good_codex_tipo, text_codex)

with codecs.open('src/components/Codex.tsx', 'w', 'utf-8') as f:
    f.write(text_codex)


# 2. RINHA
with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text_rinha = f.read()

if "import { META_TIPOS" not in text_rinha:
    text_rinha = text_rinha.replace("import { SISTEMA_TIPOS } from '../data/tiposDb';", "import { SISTEMA_TIPOS, META_TIPOS } from '../data/tiposDb';")

regex_rinha_badge1 = r'<span className="bg-zinc-800 px-3 py-1 rounded-md text-xs font-bold text-zinc-300">\s*\{meuGalo\.tipo\}\s*</span>'
good_rinha_badge1 = '''<span className={`px-3 py-1 rounded-md text-xs font-bold ${META_TIPOS[meuGalo.tipo]?.corFundo || 'bg-zinc-800'} ${META_TIPOS[meuGalo.tipo]?.corTexto || 'text-zinc-300'}`}>
                                    {META_TIPOS[meuGalo.tipo]?.icone || ''} {meuGalo.tipo}
                                </span>'''
text_rinha = re.sub(regex_rinha_badge1, good_rinha_badge1, text_rinha)

regex_rinha_badge2 = r'<span className="bg-zinc-800 px-3 py-1 rounded-md text-xs font-bold text-zinc-300">\s*\{inimigo\.tipo\}\s*</span>'
good_rinha_badge2 = '''<span className={`px-3 py-1 rounded-md text-xs font-bold ${META_TIPOS[inimigo.tipo]?.corFundo || 'bg-zinc-800'} ${META_TIPOS[inimigo.tipo]?.corTexto || 'text-zinc-300'}`}>
                                        {META_TIPOS[inimigo.tipo]?.icone || ''} {inimigo.tipo}
                                    </span>'''
text_rinha = re.sub(regex_rinha_badge2, good_rinha_badge2, text_rinha)

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text_rinha)

print("Done with Codex and Rinha")

