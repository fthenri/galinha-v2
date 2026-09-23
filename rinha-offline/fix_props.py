import codecs

with codecs.open('src/components/ModoTreino.tsx', 'r', 'utf-8') as f:
    text = f.read()
text = text.replace('export default function ModoTreino() {', 'export default function ModoTreino({ jogador }: { jogador: any }) {')
with codecs.open('src/components/ModoTreino.tsx', 'w', 'utf-8') as f:
    f.write(text)

with codecs.open('src/components/ModoTrial.tsx', 'r', 'utf-8') as f:
    text2 = f.read()
text2 = text2.replace('export default function ModoTrial() {', 'export default function ModoTrial({ jogador }: { jogador: any }) {')
with codecs.open('src/components/ModoTrial.tsx', 'w', 'utf-8') as f:
    f.write(text2)

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text3 = f.read()
text3 = text3.replace('<ModoTreino />', '<ModoTreino jogador={meuGalo} />')
text3 = text3.replace('<ModoTrial />', '<ModoTrial jogador={meuGalo} />')
with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text3)

print("Done props")

