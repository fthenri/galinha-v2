import codecs

with codecs.open('src/components/ModoTrial.tsx', 'r', 'utf-8') as f:
    text = f.read()

text = text.replace('const PESOS_RARIDADE: Record<string, number> = {\n    Common: 1, Rare: 2, Epic: 3, Legendary: 4, Mythic: 5, Divine: 6\n};', '')
text = text.replace('const PESOS_RARIDADE: Record<string, number> = {\r\n    Common: 1, Rare: 2, Epic: 3, Legendary: 4, Mythic: 5, Divine: 6\r\n};', '')

with codecs.open('src/components/ModoTrial.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done PESOS")

