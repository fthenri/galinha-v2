import codecs
import re

with codecs.open('src/store/jogadorStore.ts', 'r', 'utf-8') as f:
    text = f.read()

text = text.replace('setAutoRevive: (valor: boolean) => void;', 'setAutoRevive: (valor: boolean) => void;\n    darRebirth: (galoIndex: number) => void;')

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
            }),'''

text = text.replace('setAutoRevive: (valor) => set({ autoRevive: valor }),', implementation)

with codecs.open('src/store/jogadorStore.ts', 'w', 'utf-8') as f:
    f.write(text)
print("Done adding darRebirth")
