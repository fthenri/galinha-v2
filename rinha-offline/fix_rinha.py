import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

# 1. Update HP calculation for Trial
hp_calc_regex = r'const hpInimigoSemRebirth = dadosInimigo\.hp_base \+ \(\(nivelInimigo - 1\) \* 12\);'
new_hp_calc = '''            let hpInimigoSemRebirth = dadosInimigo.hp_base + ((nivelInimigo - 1) * 12);
            if (isTrial) {
                hpInimigoSemRebirth = 100 + (nivelInimigo * 12);
            }'''
if 'hpInimigoSemRebirth = 100 + (nivelInimigo * 12);' not in text:
    text = re.sub(hp_calc_regex, new_hp_calc, text)

# 2. Update post-combat log message
log_trial_regex = r'adicionarLog\(`Trial de \$\{meuGalo\.nome\} Conclu.da!\\nVoltando ao treino normal\.\.\.`\);'
new_log_trial = 'adicionarLog(`Trial Concluída! Bônus da classe ${meuGalo.nome} aumentado.`);'
if 'Bônus da classe' not in text:
    text = re.sub(log_trial_regex, new_log_trial, text)

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done fix rinha logic")

