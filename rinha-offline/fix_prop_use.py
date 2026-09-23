import codecs

for fname in ['src/components/ModoTreino.tsx', 'src/components/ModoTrial.tsx']:
    with codecs.open(fname, 'r', 'utf-8') as f:
        text = f.read()
    
    # Replace useJogadorStore call with the prop
    text = text.replace('const meuGalo = useJogadorStore(s => s.galos[s.galoAtivoIndex]);', 'const meuGalo = jogador;')
    
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(text)

print("Done using prop")

