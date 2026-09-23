import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

# I will find `<GaloCard ... />` and insert the modals right after the `</div>` that closes `.flex-wrap`.

# Or just use `text.rpartition('</div>')`
parts = text.rsplit('</div>', 2)
# parts will be [everything before last two </div>, \n    , \n  );\n}\n]
# Actually, let's just find the last `  );`
parts = text.rsplit('  );\n}', 1)

modals = '''
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

      {modalRebirth !== null && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
          <div className="bg-zinc-900 border border-zinc-700 p-8 rounded-2xl w-full max-w-md shadow-2xl relative flex flex-col items-center text-center">
            <h2 className="text-3xl font-black text-purple-500 mb-2">Realizar Rebirth</h2>
            <p className="text-zinc-400 text-sm mb-6">O Rebirth reinicia o nível do seu galo para 1 e zera suas habilidades equipadas, mas concede um bônus vitalício de +15% nos Atributos Base (HP Máximo, Dano e Cura)!</p>
            
            <div className="w-full flex flex-col gap-4 mb-8">
              <div className="bg-zinc-800 p-4 rounded-xl flex justify-between items-center border border-zinc-700/50">
                <span className="font-bold text-zinc-300">Nível do Galo</span>
                <span className={`font-black text-lg ${galos[modalRebirth].nivel >= calcularNivelRebirth(galos[modalRebirth].rebirths || 0) ? 'text-green-500' : 'text-red-500'}`}>
                  {galos[modalRebirth].nivel} / {calcularNivelRebirth(galos[modalRebirth].rebirths || 0)}
                </span>
              </div>
            </div>
            
            <div className="w-full flex gap-4">
              <button 
                onClick={() => setModalRebirth(null)}
                className="flex-1 bg-zinc-800 hover:bg-zinc-700 text-white font-bold py-3 px-4 rounded-xl transition-all"
              >
                Cancelar
              </button>
              
              <button 
                onClick={() => {
                  useJogadorStore.getState().darRebirth(modalRebirth);
                  setModalRebirth(null);
                }}
                disabled={galos[modalRebirth].nivel < calcularNivelRebirth(galos[modalRebirth].rebirths || 0)}
                className={`flex-1 font-black py-3 px-4 rounded-xl transition-all ${galos[modalRebirth].nivel < calcularNivelRebirth(galos[modalRebirth].rebirths || 0) ? 'bg-purple-600/20 text-purple-500/50 opacity-50 cursor-not-allowed' : 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-[0_0_15px_rgba(147,51,234,0.5)] hover:scale-105'}`}
              >
                Confirmar
              </button>
            </div>
          </div>
        </div>
      )}
'''

final_text = parts[0] + modals + '  );\n}'

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(final_text)

print("Done inserting modals")

