import codecs
import re

with codecs.open('src/components/ModoTrial.tsx', 'r', 'utf-8') as f:
    text = f.read()

# I will find the block to replace
start_marker = "const dadosInimigo = GALOS_DB[meuGalo.nome];"
end_marker = "const novoInimigo = new Galo("

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx != -1 and end_idx != -1:
    before = text[:start_idx + len(start_marker)]
    after = text[end_idx:]
    
    new_middle = '''
            const trialsAtualLoop = useJogadorStore.getState().trialsPorClasse[meuGalo.nome] || 0;
            const nivelInimigo = calcularNivelInimigoTrial(trialsAtualLoop);
            const rebirthsInimigo = meuGalo.rebirths || 0;
            const inimigoEvoluido = false;

            const hpInimigoSemRebirth = 100 + (nivelInimigo * 12);
            const hpInimigoComRebirth = Math.floor(hpInimigoSemRebirth * calcularMultiplicadorRebirth(rebirthsInimigo));

            '''
    
    text = before + new_middle + after
else:
    print("Markers not found!")

# Now I'll fix the UI panel logic at the top of the component return
# The prompt says: "No topo do componente <ModoTrial>, logo abaixo do botão de '← Abandonar Batalha', crie um painel informativo"
# But `Rinha.tsx` renders the abandon button! `ModoTrial` just renders the combat UI.
# So I'll put it at the top of ModoTrial return.

ui_start_marker = '<div className="p-6 flex flex-col items-center max-w-4xl mx-auto w-full">'
ui_new = '''<div className="p-6 flex flex-col items-center max-w-4xl mx-auto w-full">
            <div className="bg-zinc-800/50 border border-zinc-700 rounded-lg p-4 mb-4 w-full max-w-2xl text-center">
                <h3 className="text-lg font-bold text-amber-500">Trial de Maestria: {meuGalo.nome}</h3>
                <p className="text-sm text-zinc-300">Progresso da Classe: {useJogadorStore.getState().trialsPorClasse[meuGalo.nome] || 0}/20</p>
                <p className="text-xs text-emerald-400 mt-2">
                    Bônus Global Ativo: +{(calcularBonusTrial(useJogadorStore.getState().trialsPorClasse[meuGalo.nome] || 0).dano * 100).toFixed(0)}% Dano | +{(calcularBonusTrial(useJogadorStore.getState().trialsPorClasse[meuGalo.nome] || 0).vida * 100).toFixed(0)}% Vida
                </p>
            </div>'''

text = text.replace(ui_start_marker, ui_new)

with codecs.open('src/components/ModoTrial.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done exact replace")

