import codecs

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
text = text.replace('meuGalo.hp_max = Math.floor(hpBaseOriginal * (1 + bonusTrial.vida));', 'meuGalo.hp_max = Math.floor(hpBaseOriginal * (1 + bonusTrial.vida) * (1 + (itemMods.vidaBonus || 0)));')

# Enemy HP (Voodoo)
text = text.replace('novoInimigo.hp_atual = hpInimigoComRebirth;', 'novoInimigo.hp_atual = Math.floor(hpInimigoComRebirth * (1 - (itemMods.voodoo || 0)));')

# 4. Effect Damage Bonus
old_efeito = '''                const resEfeitos = atacante.processarEfeitosInicioTurno();
                const mensagensEfeito = resEfeitos[0];
                const podeAtacar = resEfeitos[1];'''
new_efeito = '''                const resEfeitos = atacante.processarEfeitosInicioTurno();
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
text = text.replace(old_efeito, new_efeito)

# 5. Attack Damage Bonus
text = text.replace('danoAtaque = Math.floor(danoAtaque * (1 + bonusTrial.dano));', 'danoAtaque = Math.floor(danoAtaque * (1 + bonusTrial.dano) * (1 + (itemMods.ataqueBonus || 0)));')

# 6. Damage Block (Bloqueio)
text = text.replace('danoReal = alvoDano.sofrerDano(danoAtaque, defensor.tipo);', 'danoReal = alvoDano.sofrerDano(alvoDano === meuGalo ? Math.floor(danoAtaque * (1 - (itemMods.bloqueioDano || 0))) : danoAtaque, defensor.tipo);')
text = text.replace('danoReal = alvoDano.sofrerDano(danoAtaque, atacante.tipo);', 'danoReal = alvoDano.sofrerDano(alvoDano === meuGalo ? Math.floor(danoAtaque * (1 - (itemMods.bloqueioDano || 0))) : danoAtaque, atacante.tipo);')

# 7. Regen and Item Effect
old_regen = '''                    adicionarLog(msgAtaque);
                }'''
new_regen = '''                    adicionarLog(msgAtaque);

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
text = text.replace(old_regen, new_regen)

# 8. Post-battle XP and Coins
old_post = '''                    const configDif = CONFIG_DIFICULDADE[difRinhaRef.current] || CONFIG_DIFICULDADE.Facil;
                    const xpGanho = Math.floor(configDif.calcXp(xpBase));
                    const moedasGanhas = 6;'''
new_post = '''                    const configDif = CONFIG_DIFICULDADE[difRinhaRef.current] || CONFIG_DIFICULDADE.Facil;
                    const xpGanho = Math.floor(configDif.calcXp(xpBase) * (1 + (itemMods.xpBonus || 0)));
                    const moedasGanhas = 6 + (itemMods.dinheiroBonus || 0);'''
text = text.replace(old_post, new_post)

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done item integration replace")

