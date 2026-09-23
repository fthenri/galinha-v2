import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

# 1. Update GaloCard definition
old_def = 'function GaloCard({ galo, galoIndex, isAtivo, onEquipar }: { galo: Galo, galoIndex: number, isAtivo: boolean, onEquipar: () => void }) {'
new_def = 'function GaloCard({ galo, galoIndex, isAtivo, onEquipar, onOpenEvolucao }: { galo: Galo, galoIndex: number, isAtivo: boolean, onEquipar: () => void, onOpenEvolucao: (idx: number) => void }) {'
text = text.replace(old_def, new_def)

# 2. Add evolution button below rebirth button in GaloCard
rebirth_btn = '''      <button
        onClick={() => useJogadorStore.getState().darRebirth(galoIndex)}
        disabled={galo.nivel < calcularNivelRebirth(galo.rebirths || 0)}
        className={`bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold py-2 rounded-lg mt-4 w-full ${galo.nivel < calcularNivelRebirth(galo.rebirths || 0) ? 'opacity-50 cursor-not-allowed' : 'hover:from-purple-500 hover:to-indigo-500'}`}
      >
        Rebirth (Lvl {calcularNivelRebirth(galo.rebirths || 0)})
      </button>'''

evo_btn = '''
      <button
        onClick={() => onOpenEvolucao(galoIndex)}
        className="bg-gradient-to-r from-amber-500 to-yellow-600 text-black font-bold py-2 rounded-lg mt-2 w-full hover:from-amber-400 hover:to-yellow-500 shadow-lg transition-all"
      >
        Evolução
      </button>'''

text = text.replace(rebirth_btn, rebirth_btn + evo_btn)

# 3. Update GaloCard usage
old_usage = '''          <GaloCard 
            key={idx} 
            galo={galo} 
            galoIndex={idx}
            isAtivo={idx === galoAtivoIndex} 
            onEquipar={() => setGaloAtivo(idx)} 
          />'''
new_usage = '''          <GaloCard 
            key={idx} 
            galo={galo} 
            galoIndex={idx}
            isAtivo={idx === galoAtivoIndex} 
            onEquipar={() => setGaloAtivo(idx)}
            onOpenEvolucao={setModalEvolucao}
          />'''
text = text.replace(old_usage, new_usage)

# 4. Add state to Perfil component
if 'const [modalEvolucao, setModalEvolucao] = useState' not in text:
    text = text.replace('export default function Perfil() {\n  const { nome, moedas, galoCoins, galos, galoAtivoIndex, setGaloAtivo } = useJogadorStore();', 'import { useState } from "react";\n\nexport default function Perfil() {\n  const { nome, moedas, galoCoins, galos, galoAtivoIndex, setGaloAtivo } = useJogadorStore();\n  const [modalEvolucao, setModalEvolucao] = useState<number | null>(null);')

# 5. Add Modal HTML inside Perfil return
modal_html = '''
      {modalEvolucao !== null && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
          <div className="bg-zinc-900 border border-zinc-700 p-8 rounded-2xl w-full max-w-md shadow-2xl relative flex flex-col items-center text-center">
            <h2 className="text-3xl font-black text-amber-500 mb-2">Desbloquear Ataque Evoluído</h2>
            <p className="text-zinc-400 text-sm mb-6">Desperte o poder supremo deste Galo, garantindo que sua habilidade no Nível 30 seja automaticamente evoluída!</p>
            
            <div className="w-full flex flex-col gap-4 mb-8">
              <div className="bg-zinc-800 p-4 rounded-xl flex justify-between items-center border border-zinc-700/50">
                <span className="font-bold text-zinc-300">Rebirths do Galo</span>
                <span className={`font-black text-lg ${((galos[modalEvolucao].rebirths || 0) >= 10) ? 'text-green-500' : 'text-red-500'}`}>
                  {galos[modalEvolucao].rebirths || 0} / 10
                </span>
              </div>
              
              <div className="bg-zinc-800 p-4 rounded-xl flex justify-between items-center border border-zinc-700/50">
                <span className="font-bold text-zinc-300">Galo Coins</span>
                <span className={`font-black text-lg ${galoCoins >= 10 ? 'text-green-500' : 'text-red-500'}`}>
                  {galoCoins} / 10
                </span>
              </div>
            </div>
            
            <div className="w-full flex gap-4">
              <button 
                onClick={() => setModalEvolucao(null)}
                className="flex-1 bg-zinc-800 hover:bg-zinc-700 text-white font-bold py-3 px-4 rounded-xl transition-all"
              >
                Cancelar
              </button>
              
              <button 
                onClick={() => {
                  useJogadorStore.getState().desbloquearEvolucao(modalEvolucao);
                  setModalEvolucao(null);
                }}
                disabled={galoCoins < 10 || (galos[modalEvolucao].rebirths || 0) < 10 || galos[modalEvolucao].evolucao_desbloqueada}
                className={`flex-1 font-black py-3 px-4 rounded-xl transition-all ${galoCoins < 10 || (galos[modalEvolucao].rebirths || 0) < 10 || galos[modalEvolucao].evolucao_desbloqueada ? 'bg-amber-600/20 text-amber-500/50 opacity-50 cursor-not-allowed' : 'bg-gradient-to-r from-amber-500 to-yellow-600 text-black shadow-[0_0_15px_rgba(245,158,11,0.5)] hover:scale-105'}`}
              >
                {galos[modalEvolucao].evolucao_desbloqueada ? 'Já Adquirido' : 'Comprar'}
              </button>
            </div>
          </div>
        </div>
      )}
'''

if 'modalEvolucao !== null' not in text:
    text = text.replace('</div>\n    </div>\n  );\n}\n', '</div>\n' + modal_html + '\n    </div>\n  );\n}\n')

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done modal setup")

