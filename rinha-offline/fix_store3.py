import codecs
import re

with codecs.open('src/store/jogadorStore.ts', 'r', 'utf-8') as f:
    text = f.read()

# Interface
if 'desbloquearEvolucao: (galoIndex: number)' not in text:
    text = text.replace('darRebirth: (galoIndex: number) => void;', 'darRebirth: (galoIndex: number) => void;\n    desbloquearEvolucao: (galoIndex: number) => void;')

impl = '''            darRebirth: (galoIndex) => set((state) => {
                const galos = [...state.galos];
                const galo = galos[galoIndex];
                const nivelNec = calcularNivelRebirth(galo.rebirths || 0);
                if (galo.nivel >= nivelNec) {
                    galo.rebirths = (galo.rebirths || 0) + 1;
                    galo.nivel = 1;
                    galo.xp = 0;
                    galo.skills_equipadas = [];
                }
                return { galos };
            }),
            desbloquearEvolucao: (galoIndex) => set((state) => {
                const galos = [...state.galos];
                const galo = galos[galoIndex];
                
                if ((galo.rebirths || 0) >= 10 && state.galoCoins >= 10 && !galo.evolucao_desbloqueada) {
                    galo.evolucao_desbloqueada = true;
                    const novoGaloCoins = state.galoCoins - 10;
                    
                    if (galo.nivel >= 30) {
                        const dbSkills = GALOS_DB[galo.nome]?.skills;
                        if (dbSkills) {
                            for (const [lvlStr, skill] of Object.entries(dbSkills)) {
                                if (parseInt(lvlStr, 10) <= galo.nivel && skill.isEvoluida) {
                                    galo.skills_equipadas = [skill, ...galo.skills_equipadas.filter(s => s !== null)].slice(0, 5);
                                    while (galo.skills_equipadas.length < 5) galo.skills_equipadas.push(null);
                                }
                            }
                        }
                    }
                    return { galos, galoCoins: novoGaloCoins };
                }
                return { galos };
            })'''

if 'desbloquearEvolucao: (galoIndex) =>' not in text:
    text = re.sub(r'darRebirth:\s*\(galoIndex\)\s*=>\s*set\(\(state\)\s*=>\s*\{.*?return\s*\{\s*galos\s*\};\s*\}\)', impl, text, flags=re.DOTALL)
    
with codecs.open('src/store/jogadorStore.ts', 'w', 'utf-8') as f:
    f.write(text)
print("Done Store")

