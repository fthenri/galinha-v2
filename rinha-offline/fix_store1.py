import codecs
import re

with codecs.open('src/store/jogadorStore.ts', 'r', 'utf-8') as f:
    text = f.read()

funcs = '''export const calcularNivelRebirth = (rebirths: number = 0) => Math.floor(34 + (rebirths * 1.55));
export const calcularMultiplicadorRebirth = (rebirths: number = 0) => 1 + (0.15 * rebirths);

export const calcularValorVenda'''

text = text.replace('export const calcularValorVenda', funcs)

with codecs.open('src/store/jogadorStore.ts', 'w', 'utf-8') as f:
    f.write(text)
print("Done store utilities")

