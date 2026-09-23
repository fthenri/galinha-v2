import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

regex = r'<div className="w-32 h-32 md:w-48 md:h-48 relative">\s*<img src=\{"/" \+ meuGalo\.caminho_imagem\} className="w-full h-full object-contain drop-shadow-\[0_0_15px_rgba\(34,197,94,0\.3\)\]" alt="Meu Galo" />\s*</div>\s*<div className="w-32 h-32 md:w-48 md:h-48 relative">\s*\{inimigo && \(\s*<img src=\{"/" \+ inimigo\.caminho_imagem\} className="w-full h-full object-contain scale-x-\[-1\] drop-shadow-\[0_0_15px_rgba\(168,85,247,0\.3\)\]" alt="Inimigo" />\s*\)\}\s*</div>'

good_block = '''<div className="flex flex-col items-center">
                        {inimigo && (
                            <div className="flex items-center justify-center gap-2 mb-3">
                                <span className="bg-zinc-800 px-3 py-1 rounded-md text-xs font-bold text-zinc-300">
                                    {meuGalo.tipo}
                                </span>
                                {SISTEMA_TIPOS[meuGalo.tipo]?.vantagem.includes(inimigo.tipo) && (
                                    <span className="text-emerald-400 text-xs font-bold tracking-wide">↑ +15% Dano</span>
                                )}
                                {SISTEMA_TIPOS[meuGalo.tipo]?.desvantagem.includes(inimigo.tipo) && (
                                    <span className="text-red-400 text-xs font-bold tracking-wide">↓ -10% Dano</span>
                                )}
                            </div>
                        )}
                        <div className="w-32 h-32 md:w-48 md:h-48 relative">
                            <img src={"/" + meuGalo.caminho_imagem} className="w-full h-full object-contain drop-shadow-[0_0_15px_rgba(34,197,94,0.3)]" alt="Meu Galo" />
                        </div>
                    </div>
                    
                    <div className="flex flex-col items-center">
                        {inimigo && (
                            <>
                                <div className="flex items-center justify-center gap-2 mb-3">
                                    <span className="bg-zinc-800 px-3 py-1 rounded-md text-xs font-bold text-zinc-300">
                                        {inimigo.tipo}
                                    </span>
                                    {SISTEMA_TIPOS[inimigo.tipo]?.vantagem.includes(meuGalo.tipo) && (
                                        <span className="text-emerald-400 text-xs font-bold tracking-wide">↑ +15% Dano</span>
                                    )}
                                    {SISTEMA_TIPOS[inimigo.tipo]?.desvantagem.includes(meuGalo.tipo) && (
                                        <span className="text-red-400 text-xs font-bold tracking-wide">↓ -10% Dano</span>
                                    )}
                                </div>
                                <div className="w-32 h-32 md:w-48 md:h-48 relative">
                                    <img src={"/" + inimigo.caminho_imagem} className="w-full h-full object-contain scale-x-[-1] drop-shadow-[0_0_15px_rgba(168,85,247,0.3)]" alt="Inimigo" />
                                </div>
                            </>
                        )}
                    </div>'''

if re.search(regex, text):
    text = re.sub(regex, good_block, text)
    with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
        f.write(text)
    print("Done")
else:
    print("Regex not found!")

