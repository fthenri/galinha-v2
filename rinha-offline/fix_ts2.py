import codecs
import re

with codecs.open('src/components/ModoTrial.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Remove PESOS_RARIDADE
text = re.sub(r'const PESOS_RARIDADE: Record<string, number> = \{\s*Common: 1, Rare: 2, Epic: 3, Legendary: 4, Mythic: 5, Divine: 6\s*\};\n', '', text)

# Remove ConfigDificuldade and CONFIG_DIFICULDADE
# Wait, are they used? I removed the random generation, so they shouldn't be!
# Actually, the compiler didn't complain about CONFIG_DIFICULDADE! So maybe it's used?
# Let's check the error: only PESOS_RARIDADE and isTrial are reported!

text = text.replace("            const isTrial = true;\n", "")
text = text.replace("            const isTrial = true;", "")

with codecs.open('src/components/ModoTrial.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done ts fixes 2")

