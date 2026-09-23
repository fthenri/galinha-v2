import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

regen_and_effect_code = '''                    adicionarLog(msgAtaque);

                    if (atacante === meuGalo) {
                        if (itemMods.regeneracao) {
                            const cura = Math.floor(meuGalo.hp_max * itemMods.regeneracao);
                            meuGalo.hp_atual = Math.min(meuGalo.hp_max, meuGalo.hp_atual + cura);
                            adicionarLog(`Seu item curou ${cura} HP!`);
                        }
                        if (itemMods.efeitoAoAtacar && Math.random() <= itemMods.efeitoAoAtacar.chance) {
                            const ef = itemMods.efeitoAoAtacar.nome;
                            const alvo = BUFFS.includes(ef) ? meuGalo : novoInimigo;
                            alvo.aplicarEfeito({ nome: ef, chance: 100, turnos: 2 });
                            adicionarLog(`Seu item ativou ${ef}!`);
                        }
                    }
                }'''

text = re.sub(r'adicionarLog\(msgAtaque\);\s*\}', regen_and_effect_code, text)

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done regen fix")

