import codecs
import re

with codecs.open('src/logic/Galo.ts', 'r', 'utf-8') as f:
    text = f.read()

# Import
if 'calcularMultiplicadorRebirth' not in text:
    text = "import { calcularMultiplicadorRebirth } from '../store/jogadorStore';\n" + text

# rebirths
if 'rebirths: number;' not in text:
    text = text.replace('skills_equipadas: (Skill | null)[];', 'skills_equipadas: (Skill | null)[];\n    rebirths: number;')
    text = text.replace('efeitos: Record<string, number> | null = null\n    ) {', 'efeitos: Record<string, number> | null = null,\n        rebirths: number = 0\n    ) {')
    text = text.replace('this.efeitos = efeitos ?? {};', 'this.efeitos = efeitos ?? {};\n        this.rebirths = rebirths;')

# hp_max level up
text = text.replace('this.hp_max += 12;', 'this.hp_max += Math.floor(12 * calcularMultiplicadorRebirth(this.rebirths));')

# damage
text = text.replace('let danoReal = Math.floor(skill.dano);', 'let danoReal = Math.floor(skill.dano * calcularMultiplicadorRebirth(this.rebirths));')

# heal received
heal_block = '''let valorBase = Math.floor(Math.random() * (max - min + 1)) + min;
        if (valorBase > 0) {
            valorBase = Math.floor(valorBase * calcularMultiplicadorRebirth(this.rebirths));
        }'''
text = re.sub(r'let valorBase = Math.floor\(Math\.random\(\) \* \(max - min \+ 1\)\) \+ min;', heal_block, text)

# toDict and fromDict
if 'rebirths: this.rebirths' not in text:
    text = text.replace('efeitos: this.efeitos\n        };', 'efeitos: this.efeitos,\n            rebirths: this.rebirths\n        };')
if 'data.rebirths ?? 0' not in text:
    text = text.replace('data.efeitos ? { ...data.efeitos } : {}\n        );', 'data.efeitos ? { ...data.efeitos } : {},\n            data.rebirths ?? 0\n        );')

with codecs.open('src/logic/Galo.ts', 'w', 'utf-8') as f:
    f.write(text)
print("Done logic")
