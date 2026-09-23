import codecs
import re

with codecs.open('src/store/jogadorStore.ts', 'r', 'utf-8') as f:
    text = f.read()

implementation = '''            setAutoRevive: (valor) => set({ autoRevive: valor }),
            darRebirth: (galoIndex) => set((state) => {
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
            })'''

if 'darRebirth: (galoIndex) =>' not in text:
    text = text.replace('setAutoRevive: (valor) => set({ autoRevive: valor })', implementation)
    with codecs.open('src/store/jogadorStore.ts', 'w', 'utf-8') as f:
        f.write(text)


with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text2 = f.read()

text2 = text2.replace('useJogadorStore.getState().darRebirth(index)', 'useJogadorStore.getState().darRebirth(galoIndex)')

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text2)

print("Done fixing store and perfil")

