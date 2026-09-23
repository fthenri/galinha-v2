import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

# 1. Imports and Reference
if 'ITENS_DB' not in text:
    text = text.replace("import { GALOS_DB } from '../data/galosDb';", "import { GALOS_DB } from '../data/galosDb';\nimport { ITENS_DB } from '../data/itensDb';")

# 2. Add itemMods reference inside the loop
if 'const itemMods =' not in text:
    text = text.replace(
        "const isTrial = useJogadorStore.getState().isTrialMode;",
        "const isTrial = useJogadorStore.getState().isTrialMode;\n            const itemMods = meuGalo.item_equipado ? ITENS_DB[meuGalo.item_equipado]?.modificadores || {} : {};"
    )

# 3. Pre-battle Modifiers
# Player HP
hp_jogador_regex = r'meuGalo\.hp_max = Math\.floor\(hpBaseOriginal \* \(1 \+ bonusTrial\.vida\)\);'
new_hp_jogador = 'meuGalo.hp_max = Math.floor(hpBaseOriginal * (1 + bonusTrial.vida) * (1 + (itemMods.vidaBonus || 0)));'
text = re.sub(hp_jogador_regex, new_hp_jogador, text)

# Enemy HP (Voodoo)
voodoo_regex = r'novoInimigo\.hp_atual = hpInimigoComRebirth;'
new_voodoo = 'novoInimigo.hp_atual = Math.floor(hpInimigoComRebirth * (1 - (itemMods.voodoo || 0)));'
text = re.sub(voodoo_regex, new_voodoo, text)

# 4. Effect Damage Bonus
efeito_bonus_code = '''                const resEfeitos = atacante.processarEfeitosInicioTurno();
                const mensagensEfeito = resEfeitos[0];
                const podeAtacar = resEfeitos[1];

                if (!turnoJogador && itemMods.danoEfeitoBonus) {
                    for (let i = 0; i < mensagensEfeito.length; i++) {
                        const match = mensagensEfeito[i].match(/perdeu (\\d+) HP por/);
                        if (match) {
                            const dmg = parseInt(match[1]);
                            const extra = Math.floor(dmg * itemMods.danoEfeitoBonus);
                            if (extra > 0) {
                                atacante.hp_atual -= extra;
                                mensagensEfeito[i] = mensagensEfeito[i].replace(`perdeu ${dmg} HP`, `perdeu ${dmg + extra} HP`);
                            }
                        }
                    }
                }'''
text = re.sub(
    r'const resEfeitos = atacante\.processarEfeitosInicioTurno\(\);\s*const mensagensEfeito = resEfeitos\[0\];\s*const podeAtacar = resEfeitos\[1\];',
    efeito_bonus_code,
    text
)

# 5. Attack Damage Bonus
ataque_bonus_regex = r'danoAtaque = Math\.floor\(danoAtaque \* \(1 \+ bonusTrial\.dano\)\);'
new_ataque_bonus = 'danoAtaque = Math.floor(danoAtaque * (1 + bonusTrial.dano) * (1 + (itemMods.ataqueBonus || 0)));'
text = re.sub(ataque_bonus_regex, new_ataque_bonus, text)

# 6. Damage Block (Bloqueio)
bloqueio_regex_1 = r'danoReal = alvoDano\.sofrerDano\(danoAtaque, defensor\.tipo\);'
new_bloqueio_1 = 'danoReal = alvoDano.sofrerDano(alvoDano === meuGalo ? Math.floor(danoAtaque * (1 - (itemMods.bloqueioDano || 0))) : danoAtaque, defensor.tipo);'
text = re.sub(bloqueio_regex_1, new_bloqueio_1, text)

bloqueio_regex_2 = r'danoReal = alvoDano\.sofrerDano\(danoAtaque, atacante\.tipo\);'
new_bloqueio_2 = 'danoReal = alvoDano.sofrerDano(alvoDano === meuGalo ? Math.floor(danoAtaque * (1 - (itemMods.bloqueioDano || 0))) : danoAtaque, atacante.tipo);'
text = re.sub(bloqueio_regex_2, new_bloqueio_2, text)

# 7. Regen and Item Effect
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

# 8. Post-battle XP and Coins
post_battle_code = '''                    const configDif = CONFIG_DIFICULDADE[difRinhaRef.current] || CONFIG_DIFICULDADE.Facil;
                    const xpGanho = Math.floor(configDif.calcXp(xpBase) * (1 + (itemMods.xpBonus || 0)));
                    const moedasGanhas = 6 + (itemMods.dinheiroBonus || 0);'''
text = re.sub(
    r'const configDif = CONFIG_DIFICULDADE\[difRinhaRef\.current\] \|\| CONFIG_DIFICULDADE\.Facil;\s*const xpGanho = Math\.floor\(configDif\.calcXp\(xpBase\)\);\s*const moedasGanhas = 6;',
    post_battle_code,
    text
)

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done item integration")

