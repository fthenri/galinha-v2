import codecs
import re

with codecs.open('src/logic/Galo.ts', 'r', 'utf-8') as f:
    text = f.read()

# Import
if 'calcularMultiplicadorRebirth' not in text:
    text = "import { calcularMultiplicadorRebirth } from '../store/jogadorStore';\n" + text

# Add rebirths property
text = text.replace('skills_equipadas: (Skill | null)[];', 'skills_equipadas: (Skill | null)[];\n    rebirths: number;')

# Constructor
text = text.replace('efeitos: Record<string, number> | null = null\n    ) {', 'efeitos: Record<string, number> | null = null,\n        rebirths: number = 0\n    ) {')
text = text.replace('this.efeitos = efeitos ?? {};', 'this.efeitos = efeitos ?? {};\n        this.rebirths = rebirths;')

# Hp Max and Curas logic:
# Wait, HP max should be multiplied at battle start?
# "Multiplique o HP Máximo, o dano causado e a cura recebida por esse fator."
# Wait, if we multiply hp_max by rebirth multiplier, we can just do it in a getter, or when calculating damage.
# If I change hp_max, I should just change the constructor maybe? No, `this.hp_max` is base HP.
# Wait, let's see how hp_max is read in battle. Let's just create a getter `getHpMax()` or multiply it directly where it is returned? In JS, it's just a property.
# I will make `getHpMax()` method, or replace `this.hp_max` usage.
# Better to do it in the methods `atacar` and `sofrerDano`, and for `hp_max`, maybe we just multiply it when the Galo is created? But `fromDict` uses it.

# Let's check `sofrerDano` and `atacar` first.
text = text.replace('let danoReal = Math.floor(skill.dano);', 'let danoReal = Math.floor(skill.dano * calcularMultiplicadorRebirth(this.rebirths));')

# What about sofrerDano?
# Wait! "a cura recebida por esse fator."
# In `aplicarVariacaoHp`, we have `let valorBase = ...` and then `this.hp_atual += valorBase`. If valorBase > 0, we can multiply.
text = text.replace('let valorBase = Math.floor(Math.random() * (max - min + 1)) + min;', 'let valorBase = Math.floor(Math.random() * (max - min + 1)) + min;\n        if (valorBase > 0) valorBase = Math.floor(valorBase * calcularMultiplicadorRebirth(this.rebirths));')

# toDict and fromDict
text = text.replace('efeitos: this.efeitos\n        };', 'efeitos: this.efeitos,\n            rebirths: this.rebirths\n        };')
text = text.replace('data.efeitos ? { ...data.efeitos } : {}\n        );', 'data.efeitos ? { ...data.efeitos } : {},\n            data.rebirths ?? 0\n        );')

with codecs.open('src/logic/Galo.ts', 'w', 'utf-8') as f:
    f.write(text)
print("Done logic")

