import codecs
import re

with codecs.open('src/components/ModoTrial.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Replace the generation block completely
old_block = r'''            const configDif = CONFIG_DIFICULDADE\[dificuldade\] \|\| CONFIG_DIFICULDADE\.Facil;
            
            let nivelInimigo = 0;
            let rebirthsInimigo = 0;
            let inimigoEvoluido = false;

            if \(isTrial\) \{
                const trialsAtualLoop = useJogadorStore\.getState\(\)\.trialsPorClasse\[meuGalo\.nome\] \|\| 0;
                nivelInimigo = calcularNivelInimigoTrial\(trialsAtualLoop\);
                rebirthsInimigo = meuGalo\.rebirths \|\| 0;
                inimigoEvoluido = false;
            \} else \{
                nivelInimigo = configDif\.calcNivel\(nivelBase\);
                if \(dificuldade === "Facil" && pesoInimigo > pesoJogador\) \{
                    nivelInimigo = Math\.max\(1, nivelInimigo - \(pesoInimigo - pesoJogador\)\);
                \}
                rebirthsInimigo = configDif\.calcRebirths\(meuGalo\.rebirths \|\| 0\);
                inimigoEvoluido = configDif\.inimigoEvoluido \|\| false;
            \}

                        let hpInimigoSemRebirth = dadosInimigo\.hp_base \+ \(\(nivelInimigo - 1\) \* 12\);
            if \(isTrial\) \{
                hpInimigoSemRebirth = 100 \+ \(nivelInimigo \* 12\);
            \}
            const hpInimigoComRebirth = Math\.floor\(hpInimigoSemRebirth \* calcularMultiplicadorRebirth\(rebirthsInimigo\)\);'''

new_block = '''            const trialsAtualLoop = useJogadorStore.getState().trialsPorClasse[meuGalo.nome] || 0;
            const nivelInimigo = calcularNivelInimigoTrial(trialsAtualLoop);
            const rebirthsInimigo = meuGalo.rebirths || 0;
            const inimigoEvoluido = false;

            const hpInimigoSemRebirth = 100 + (nivelInimigo * 12);
            const hpInimigoComRebirth = Math.floor(hpInimigoSemRebirth * calcularMultiplicadorRebirth(rebirthsInimigo));'''

text = re.sub(old_block, new_block, text)

# There is a check for isTrial further down for victory logic
# Let's clean it up too for ModoTrial
text = text.replace('if (isTrial) {', 'if (true) {')

with codecs.open('src/components/ModoTrial.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done clean trial")

