import codecs
import re

with codecs.open('src/components/Codex.tsx', 'r', 'utf-8') as f:
    text = f.read()

if "import { formatarEfeitoString" not in text:
    text = text.replace("import { EFEITOS_DADOS } from '../data/efeitosDb';", "import { EFEITOS_DADOS } from '../data/efeitosDb';\nimport { formatarEfeitoString } from '../utils/formatters';")

bad_regex = r'\{skill\.efeito && \(\s*<div className="mt-4 pt-4 border-t border-zinc-800/50">\s*<span className="text-indigo-400 text-\[10px\] font-bold uppercase tracking-widest mb-1 block">Effect</span>\s*<span className="text-indigo-300 text-xs flex gap-1 items-center">\s*<span className="font-bold text-indigo-400">\{skill\.efeito\}</span>\s*<span>·</span>\s*<span>\{skill\.chance \?\? 100\}%</span>\s*<span>·</span>\s*<span>\{skill\.turnos \?\? 1\}t</span>\s*\{EFEITOS_DADOS\[skill\.efeito\] && \(\s*<>\s*<span>·</span>\s*<span>\{EFEITOS_DADOS\[skill\.efeito\]\} Min damage</span>\s*</>\s*\)\}\s*</span>\s*</div>\s*\)\}'

good_block = '''{skill.efeito && (
                  <div className="mt-4 pt-4 border-t border-zinc-800/50">
                    <span className="text-indigo-400 text-[10px] font-bold uppercase tracking-widest mb-1 block">Effect</span>
                    <span className="text-indigo-300 text-xs flex gap-1 items-center">
                      <span className="font-bold text-indigo-400">{skill.efeito}</span>
                      <span>·</span>
                      <span>{formatarEfeitoString(skill.efeito, `${skill.chance ?? 100}% · ${skill.turnos ?? 1}t` + (EFEITOS_DADOS[skill.efeito] !== undefined ? ` · ${EFEITOS_DADOS[skill.efeito]}` : ""))}</span>
                    </span>
                  </div>
                )}'''

if re.search(bad_regex, text):
    text = re.sub(bad_regex, good_block, text)
    with codecs.open('src/components/Codex.tsx', 'w', 'utf-8') as f:
        f.write(text)
    print("Done replace")
else:
    print("Not found")

