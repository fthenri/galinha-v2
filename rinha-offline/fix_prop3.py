import codecs
import re

for fname in ['src/components/ModoTreino.tsx', 'src/components/ModoTrial.tsx']:
    with codecs.open(fname, 'r', 'utf-8') as f:
        text = f.read()
    
    text = text.replace('const meuGalo = galoAtivoIndex >= 0 && galoAtivoIndex < galos.length ? galos[galoAtivoIndex] : null;', 'const meuGalo = jogador || (galoAtivoIndex >= 0 && galoAtivoIndex < galos.length ? galos[galoAtivoIndex] : null);')
    
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(text)

print("Done using prop fix 3")

