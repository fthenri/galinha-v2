import { useState } from 'react';
import { GALOS_DB } from '../data/galosDb';
import { EFEITOS_DADOS } from '../data/efeitosDb';
import { formatarEfeitoString } from '../utils/formatters';
import { SISTEMA_TIPOS, META_TIPOS } from '../data/tiposDb';

const getRarityClasses = (rarity: string, isMythic: boolean = false) => {
  if (isMythic) return "bg-gradient-to-tr from-violet-500 via-orange-500 to-cyan-500 p-[2px] rounded-xl";
  switch (rarity) {
    case "Common": return "ring-1 ring-zinc-400 rounded-xl p-1";
    case "Rare": return "ring-1 ring-blue-600 rounded-xl p-1";
    case "Epic": return "ring-1 ring-purple-500 rounded-xl p-1";
    case "Legendary": return "ring-1 ring-orange-500 rounded-xl p-1";
    case "Special": return "ring-1 ring-red-600 rounded-xl p-1";
    case "Divine": return "ring-1 ring-fuchsia-500 rounded-xl p-1";
    default: return "ring-1 ring-zinc-400 rounded-xl p-1";
  }
};

const getRarityTextClasses = (rarity: string) => {
  switch (rarity) {
    case "Common": return "text-zinc-400";
    case "Rare": return "text-blue-500";
    case "Epic": return "text-purple-400";
    case "Legendary": return "text-orange-500";
    case "Special": return "text-red-500";
    case "Divine": return "text-fuchsia-400";
    case "Mythic": return "text-transparent bg-clip-text bg-gradient-to-tr from-violet-500 via-orange-500 to-cyan-500";
    default: return "text-zinc-400";
  }
};

const renderNomeGalo = (nome: string, raridade: string) => {
  if (nome.startsWith("Rooster ")) {
    return (
      <>{nome.substring(0, 8)}<span className={getRarityTextClasses(raridade)}>{nome.substring(8)}</span></>
    );
  }
  return <>{nome}</>;
};

export default function Codex() {
  const [galoSelecionado, setGaloSelecionado] = useState<string | null>(null);

  if (galoSelecionado && GALOS_DB[galoSelecionado]) {
    const galo = GALOS_DB[galoSelecionado];
    const raridade = galo.raridade || "Common";
    const habilidades = Object.entries(galo.skills);

    return (
      <div className="p-6 flex flex-col items-center max-w-4xl mx-auto w-full">
        <div className="w-full mb-6">
          <button 
            onClick={() => setGaloSelecionado(null)}
            className="text-zinc-400 hover:text-white flex items-center font-bold transition-colors"
          >
            ← Voltar
          </button>
        </div>

        <div className="w-full flex flex-col md:flex-row gap-8 mb-10">
          <div className="w-48 h-48 md:w-64 md:h-64 bg-zinc-800 rounded-2xl flex items-center justify-center p-4 flex-shrink-0">
            <img src={"/" + galo.caminho_imagem} alt={galoSelecionado} className="w-full h-full object-contain" />
          </div>

          <div className="flex flex-col justify-center">
            <h1 className="text-4xl md:text-5xl font-black text-zinc-100 mb-4">{renderNomeGalo(galoSelecionado, raridade)}</h1>
            <div className="flex gap-3 mb-6">
              <span className={"px-3 py-1 rounded-md text-sm font-bold bg-zinc-800 " + getRarityTextClasses(raridade)}>
                {raridade}
              </span>
              <span className={`px-3 py-1 rounded-md text-sm font-bold ${META_TIPOS[galo.tipo]?.corFundo || 'bg-zinc-800'} ${META_TIPOS[galo.tipo]?.corTexto || 'text-zinc-300'}`}>
                {META_TIPOS[galo.tipo]?.icone || ''} {galo.tipo}
              </span>
            </div>
            
            {SISTEMA_TIPOS[galo.tipo] && (
              // Inclusão da estrutura de vantagens e desvantagens
              <div className="flex justify-between w-full mt-6">
                <div className="flex flex-col">
                  <span className="text-emerald-400 text-xs font-bold tracking-widest uppercase mb-2">↑ +15% AGAINST</span>
                  <div className="flex flex-col">
                    {SISTEMA_TIPOS[galo.tipo].vantagem.map(t => (
                      <span key={t} className="text-zinc-300 text-sm font-medium">{t}</span>
                    ))}
                  </div>
                </div>
                <div className="flex flex-col">
                  <span className="text-red-400 text-xs font-bold tracking-widest uppercase mb-2">↓ -10% AGAINST</span>
                  <div className="flex flex-col">
                    {SISTEMA_TIPOS[galo.tipo].desvantagem.map(t => (
                      <span key={t} className="text-zinc-300 text-sm font-medium">{t}</span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="w-full flex flex-col gap-6">
          <h2 className="text-2xl font-bold text-zinc-300">{habilidades.length} attacks</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {habilidades.map(([lvl, skill], idx) => (
              <div key={idx} className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 flex flex-col relative">
                <div className="absolute top-4 right-4 text-xs font-bold text-zinc-500">
                  LEVEL {lvl}
                </div>
                
                <h3 className="text-zinc-200 font-bold text-lg mb-4 pr-16">{skill.nome}</h3>
                
                <div className="flex flex-col gap-2 mt-auto">
                  <div className="flex justify-between items-center">
                    <span className="text-zinc-500 text-xs tracking-widest font-semibold">MIN DAMAGE</span>
                    <span className="text-zinc-300 font-mono font-bold">{skill.min}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-zinc-500 text-xs tracking-widest font-semibold">MAX DAMAGE</span>
                    <span className="text-zinc-300 font-mono font-bold">{skill.max}</span>
                  </div>
                </div>

                {skill.efeito && (
                  <div className="mt-4 pt-4 border-t border-zinc-800/50">
                    <span className="text-indigo-400 text-[10px] font-bold uppercase tracking-widest mb-1 block">Effect</span>
                    <span className="text-indigo-300 text-xs flex gap-1 items-center">
                      <span className="font-bold text-indigo-400">{skill.efeito}</span>
                      <span>·</span>
                      <span>{formatarEfeitoString(skill.efeito, `${skill.chance ?? 100}% · ${skill.turnos ?? 1}t` + (EFEITOS_DADOS[skill.efeito] !== undefined ? ` · ${EFEITOS_DADOS[skill.efeito]}` : ""))}</span>
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const nomes = Object.keys(GALOS_DB);

  return (
    <div className="p-6 flex flex-col items-center max-w-5xl mx-auto w-full">
      <h2 className="text-3xl font-bold mb-8 w-full text-left">Codex</h2>
      
      <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-4 w-full">
        {nomes.map(nome => {
          const dados = GALOS_DB[nome];
          const raridade = dados.raridade || "Common";
          const isMythic = raridade === "Mythic";

          return (
            <div 
              key={nome}
              onClick={() => setGaloSelecionado(nome)}
              className={"cursor-pointer transition-transform hover:-translate-y-1 " + getRarityClasses(raridade, isMythic)}
            >
              <div className="bg-zinc-900 rounded-lg p-2 h-full flex flex-col items-center justify-between gap-2">
                <img src={"/" + dados.caminho_imagem} alt={nome} className="w-16 h-16 object-contain" />
                <span className="text-xs font-bold text-center text-zinc-300 leading-tight">{renderNomeGalo(nome, raridade)}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
