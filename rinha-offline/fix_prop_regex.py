import codecs
import re

for fname in ['src/components/ModoTreino.tsx', 'src/components/ModoTrial.tsx']:
    with codecs.open(fname, 'r', 'utf-8') as f:
        text = f.read()
    
    # Remove the galos and galoAtivoIndex
    text = re.sub(r'const galos = useJogadorStore\(s => s\.galos\);\n\s*const galoAtivoIndex = useJogadorStore\(s => s\.galoAtivoIndex\);\n\s*const meuGalo = galoAtivoIndex >= 0 && galoAtivoIndex < galos\.length \? galos\[galoAtivoIndex\] : null;', 'const meuGalo = jogador;', text)
    
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(text)

print("Done prop regex")

