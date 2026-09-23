import codecs
import re

with codecs.open('src/logic/Galo.ts', 'r', 'utf-8') as f:
    text = f.read()

# Add to properties
if 'evolucao_desbloqueada?: boolean;' not in text:
    text = text.replace('rebirths: number;', 'rebirths: number;\n    evolucao_desbloqueada?: boolean;')

# Add to constructor
if 'evolucao_desbloqueada: boolean = false' not in text:
    text = text.replace('rebirths: number = 0\n    ) {', 'rebirths: number = 0,\n        evolucao_desbloqueada: boolean = false\n    ) {')
    text = text.replace('this.rebirths = rebirths;', 'this.rebirths = rebirths;\n        this.evolucao_desbloqueada = evolucao_desbloqueada;')

# Update `obterSkillsDesbloqueadas`
if 'if (!skill.isEvoluida || this.evolucao_desbloqueada)' not in text:
    bad_push = 'if (lvl <= this.nivel) {\n                desbloqueadas.push({ level: lvl, skill });\n            }'
    good_push = 'if (lvl <= this.nivel) {\n                if (!skill.isEvoluida || this.evolucao_desbloqueada) {\n                    desbloqueadas.push({ level: lvl, skill });\n                }\n            }'
    text = text.replace(bad_push, good_push)

# Update `ganharXp` level up skill insertion
if 'if (!skill.isEvoluida || this.evolucao_desbloqueada)' not in text:
    bad_push2 = 'if (parseInt(lvlStr, 10) === this.nivel) {\n                        skillsNoNovoNivel.push(skill);\n                    }'
    good_push2 = 'if (parseInt(lvlStr, 10) === this.nivel) {\n                        if (!skill.isEvoluida || this.evolucao_desbloqueada) {\n                            skillsNoNovoNivel.push(skill);\n                        }\n                    }'
    text = text.replace(bad_push2, good_push2)

# Update toDict and fromDict
if 'evolucao_desbloqueada: this.evolucao_desbloqueada' not in text:
    text = text.replace('rebirths: this.rebirths\n        };', 'rebirths: this.rebirths,\n            evolucao_desbloqueada: this.evolucao_desbloqueada\n        };')

if 'data.evolucao_desbloqueada ?? false' not in text:
    text = text.replace('data.rebirths ?? 0\n        );', 'data.rebirths ?? 0,\n            data.evolucao_desbloqueada ?? false\n        );')

with codecs.open('src/logic/Galo.ts', 'w', 'utf-8') as f:
    f.write(text)
print("Done Galo")

