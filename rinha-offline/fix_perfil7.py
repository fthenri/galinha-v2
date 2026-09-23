import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

# We want to insert modalRebirth right before `\n    </div>\n  );\n}\n`
# Or better, just search for `export default function Perfil() {` and find its return block.
# I will use a simple split/join on `    </div>\n  );\n}\n` (or similar) but some CRLF might mess it up.
text = re.sub(r'(\s*</div>\s*\);\s*\})', r'\n\n      {modalRebirth !== null && (\n        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">\n          <div className="bg-zinc-900 border border-zinc-700 p-8 rounded-2xl w-full max-w-md shadow-2xl relative flex flex-col items-center text-center">\n            <h2 className="text-3xl font-black text-purple-500 mb-2">Realizar Rebirth</h2>\n            <p className="text-zinc-400 text-sm mb-6">O Rebirth reinicia o nível do seu galo para 1 e zera suas habilidades equipadas, mas concede um bônus vitalício de +15% nos Atributos Base (HP Máximo, Dano e Cura)!</p>\n            \n            <div className="w-full flex flex-col gap-4 mb-8">\n              <div className="bg-zinc-800 p-4 rounded-xl flex justify-between items-center border border-zinc-700/50">\n                <span className="font-bold text-zinc-300">Nível do Galo</span>\n                <span className={`font-black text-lg ${galos[modalRebirth].nivel >= calcularNivelRebirth(galos[modalRebirth].rebirths || 0) ? \'text-green-500\' : \'text-red-500\'}`}>\n                  {galos[modalRebirth].nivel} / {calcularNivelRebirth(galos[modalRebirth].rebirths || 0)}\n                </span>\n              </div>\n            </div>\n            \n            <div className="w-full flex gap-4">\n              <button \n                onClick={() => setModalRebirth(null)}\n                className="flex-1 bg-zinc-800 hover:bg-zinc-700 text-white font-bold py-3 px-4 rounded-xl transition-all"\n              >\n                Cancelar\n              </button>\n              \n              <button \n                onClick={() => {\n                  useJogadorStore.getState().darRebirth(modalRebirth);\n                  setModalRebirth(null);\n                }}\n                disabled={galos[modalRebirth].nivel < calcularNivelRebirth(galos[modalRebirth].rebirths || 0)}\n                className={`flex-1 font-black py-3 px-4 rounded-xl transition-all ${galos[modalRebirth].nivel < calcularNivelRebirth(galos[modalRebirth].rebirths || 0) ? \'bg-purple-600/20 text-purple-500/50 opacity-50 cursor-not-allowed\' : \'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-[0_0_15px_rgba(147,51,234,0.5)] hover:scale-105\'}`}\n              >\n                Confirmar\n              </button>\n            </div>\n          </div>\n        </div>\n      )}\n\g<1>', text)

# I should also import `calcularNivelRebirth` if it was somehow removed? No, it says "is declared but its value is never read", so it's there.

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done Rebirth Modal Fixed")

