import codecs
import re

with codecs.open('src/data/galosDb.ts', 'r', 'utf-8') as f:
    text = f.read()

# Add isEvoluida
if 'isEvoluida?: boolean' not in text:
    text = re.sub(r'turnos\?:\s*number;[\r\n]*\}', 'turnos?: number;\n  isEvoluida?: boolean;\n}', text)

# The keys are already "30_evo", BUT we need to make sure Record<number, Skill> accepts it.
# Actually, Record<number, Skill> might complain about `"30_evo"` if it only accepts numbers!
# Let's change `Record<number, Skill>` to `Record<number | string, Skill>`.
text = text.replace('skills: Record<number, Skill>;', 'skills: Record<number | string, Skill>;')

with codecs.open('src/data/galosDb.ts', 'w', 'utf-8') as f:
    f.write(text)
print("Done DB 3")

