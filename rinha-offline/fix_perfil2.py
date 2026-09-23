import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Import
if 'calcularNivelRebirth' not in text:
    text = text.replace("useJogadorStore } from '../store/jogadorStore';", "useJogadorStore, calcularNivelRebirth } from '../store/jogadorStore';")

# Level badge
level_regex = r'<span className="px-2 py-1 rounded-md text-xs font-bold bg-zinc-900 text-zinc-300">N[^:]+: \{galo\.nivel\}</span>'
good_level = '<span className="px-2 py-1 rounded-md text-xs font-bold bg-zinc-900 text-zinc-300">Nível: {galo.nivel} | RB: {galo.rebirths || 0}</span>'
text = re.sub(level_regex, good_level, text)

# Rebirth button
# The end of innerContent looks like:
#         })}
#       </div>
#     </>
#   );

btn_code = '''        })}
      </div>

      <button
        onClick={() => useJogadorStore.getState().darRebirth(index)}
        disabled={galo.nivel < calcularNivelRebirth(galo.rebirths || 0)}
        className={`bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold py-2 rounded-lg mt-4 w-full ${galo.nivel < calcularNivelRebirth(galo.rebirths || 0) ? 'opacity-50 cursor-not-allowed' : 'hover:from-purple-500 hover:to-indigo-500'}`}
      >
        Rebirth (Lvl {calcularNivelRebirth(galo.rebirths || 0)})
      </button>
    </>
  );'''

text = text.replace('''        })}
      </div>
    </>
  );''', btn_code)

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done Perfil")
