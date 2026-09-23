import codecs
import re

with codecs.open('src/components/Codex.tsx', 'r', 'utf-8') as f:
    text = f.read()

bad_block_regex = r'\{SISTEMA_TIPOS\[galo\.tipo\] && \(\s*<div className="flex flex-row gap-8">\s*<div className="flex flex-col gap-1">\s*<span className="text-emerald-500 text-xs font-bold tracking-widest">↑ \+15% AGAINST</span>\s*<div className="flex gap-2">\s*\{SISTEMA_TIPOS\[galo\.tipo\]\.vantagem\.map\(t => \(\s*<span key=\{t\} className="text-zinc-300 text-sm">\{t\}</span>\s*\)\)\}\s*</div>\s*</div>\s*<div className="flex flex-col gap-1">\s*<span className="text-red-400 text-xs font-bold tracking-widest">↓ -10% AGAINST</span>\s*<div className="flex gap-2">\s*\{SISTEMA_TIPOS\[galo\.tipo\]\.desvantagem\.map\(t => \(\s*<span key=\{t\} className="text-zinc-300 text-sm">\{t\}</span>\s*\)\)\}\s*</div>\s*</div>\s*</div>\s*\)'

good_block = '''{SISTEMA_TIPOS[galo.tipo] && (
              // Inclusão da estrutura de vantagens e desvantagens
              <div className="flex justify-between w-full mt-6">
                <div className="flex flex-col">
                  <span className="text-emerald-400 text-xs font-bold tracking-widest uppercase mb-2">↑ +15% AGAINST</span>
                  <div className="flex flex-col">
                    {SISTEMA_TIPOS[galo.tipo].vantagem.map(t => (
                      <span key={t} className="text-zinc-300 text-sm font-medium">{t}</span>
                    ))}
                  </div>
                </div>
                <div className="flex flex-col">
                  <span className="text-red-400 text-xs font-bold tracking-widest uppercase mb-2">↓ -10% AGAINST</span>
                  <div className="flex flex-col">
                    {SISTEMA_TIPOS[galo.tipo].desvantagem.map(t => (
                      <span key={t} className="text-zinc-300 text-sm font-medium">{t}</span>
                    ))}
                  </div>
                </div>
              </div>
            )}'''

if re.search(bad_block_regex, text):
    text = re.sub(bad_block_regex, good_block, text)
    with codecs.open('src/components/Codex.tsx', 'w', 'utf-8') as f:
        f.write(text)
    print("Done!")
else:
    print("Not found")

