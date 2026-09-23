import codecs
import re

with codecs.open('src/components/ModoTreino.tsx', 'r', 'utf-8') as f:
    text_treino = f.read()

text_treino = text_treino.replace('export default function Rinha() {', 'export default function ModoTreino() {')
# Remove all isTrial checks and hardcode isTrial to false
text_treino = text_treino.replace('const isTrial = useJogadorStore.getState().isTrialMode;', 'const isTrial = false;')

with codecs.open('src/components/ModoTreino.tsx', 'w', 'utf-8') as f:
    f.write(text_treino)


with codecs.open('src/components/ModoTrial.tsx', 'r', 'utf-8') as f:
    text_trial = f.read()

text_trial = text_trial.replace('export default function Rinha() {', 'export default function ModoTrial() {')
text_trial = text_trial.replace('const isTrial = useJogadorStore.getState().isTrialMode;', 'const isTrial = true;')

# Remove difficulty and auto revive selects from ModoTrial
ui_controls_regex = r'<div className="flex flex-col w-40">\s*<label className="text-sm text-zinc-400 mb-1 font-semibold">Dificuldade</label>[\s\S]*?<div className="flex items-center gap-2 mt-4">'
# I need to be careful with regex here. I will just replace the specific blocks.
with codecs.open('src/components/ModoTrial.tsx', 'w', 'utf-8') as f:
    f.write(text_trial)

print("Done prep")

