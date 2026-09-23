import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

# 1. Update GaloCard definition
old_def = 'function GaloCard({ galo, galoIndex, isAtivo, onEquipar, onOpenEvolucao }: { galo: Galo, galoIndex: number, isAtivo: boolean, onEquipar: () => void, onOpenEvolucao: (idx: number) => void }) {'
new_def = 'function GaloCard({ galo, galoIndex, isAtivo, onEquipar, onOpenEvolucao, onOpenRebirth }: { galo: Galo, galoIndex: number, isAtivo: boolean, onEquipar: () => void, onOpenEvolucao: (idx: number) => void, onOpenRebirth: (idx: number) => void }) {'
text = text.replace(old_def, new_def)

# 2. Update the Rebirth button in GaloCard
rebirth_btn_regex = r'<button\s*onClick=\{[^}]+\}\s*disabled=\{galo\.nivel < calcularNivelRebirth\(galo\.rebirths \|\| 0\)\}\s*className=\{`bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold py-2 rounded-lg mt-4 w-full \$\{galo\.nivel < calcularNivelRebirth\(galo\.rebirths \|\| 0\) \? \'opacity-50 cursor-not-allowed\' : \'hover:from-purple-500 hover:to-indigo-500\'\}`\}\s*>\s*Rebirth \(Lvl \{calcularNivelRebirth\(galo\.rebirths \|\| 0\)\}\)\s*</button>'

new_rebirth_btn = '''      <button
        onClick={() => onOpenRebirth(galoIndex)}
        className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold py-2 rounded-lg mt-4 w-full hover:from-purple-500 hover:to-indigo-500 shadow-lg transition-all"
      >
        Rebirth
      </button>'''

text = re.sub(rebirth_btn_regex, new_rebirth_btn, text)

# 3. Update GaloCard usage
old_usage = '''          <GaloCard 
            key={idx} 
            galo={galo} 
            galoIndex={idx}
            isAtivo={idx === galoAtivoIndex} 
            onEquipar={() => setGaloAtivo(idx)}
            onOpenEvolucao={setModalEvolucao}
          />'''
new_usage = '''          <GaloCard 
            key={idx} 
            galo={galo} 
            galoIndex={idx}
            isAtivo={idx === galoAtivoIndex} 
            onEquipar={() => setGaloAtivo(idx)}
            onOpenEvolucao={setModalEvolucao}
            onOpenRebirth={setModalRebirth}
          />'''
text = text.replace(old_usage, new_usage)

# 4. Add state to Perfil component
text = text.replace('const [modalEvolucao, setModalEvolucao] = useState<number | null>(null);', 'const [modalEvolucao, setModalEvolucao] = useState<number | null>(null);\n  const [modalRebirth, setModalRebirth] = useState<number | null>(null);')

# 5. Add Modal HTML inside Perfil return
modal_rebirth = '''
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

if 'modalRebirth !== null' not in text:
    text = text.replace('</div>\n    </div>\n  );\n}\n', '</div>\n' + modal_rebirth + '\n    </div>\n  );\n}\n')

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done Rebirth Modal")

