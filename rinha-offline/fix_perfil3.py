import codecs
import re

with codecs.open('src/components/Perfil.tsx', 'r', 'utf-8') as f:
    text = f.read()

btn_code = '''        </button>
        
        {!galo.evolucao_desbloqueada && (
          <button
            onClick={() => useJogadorStore.getState().desbloquearEvolucao(galoIndex)}
            disabled={(galo.rebirths || 0) < 10 || galoCoins < 10}
            className={`bg-gradient-to-r from-amber-500 to-yellow-600 text-black font-bold py-2 rounded-lg mt-2 w-full transition-all ${((galo.rebirths || 0) < 10 || galoCoins < 10) ? 'opacity-50 cursor-not-allowed' : 'hover:from-amber-400 hover:to-yellow-500 shadow-lg'}`}
          >
            {(galo.rebirths || 0) < 10 ? 'Requer 10 Rebirths' : 'Desbloquear Ataque Evoluído (10 Galo Coins)'}
          </button>
        )}
      </>'''

text = text.replace('''        </button>
      </>''', btn_code)

with codecs.open('src/components/Perfil.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Done Perfil")

