import { useState, useEffect } from 'react';
import { useJogadorStore, calcularValorVenda } from '../store/jogadorStore';
import { atualizarLojaDiaria, comprarItemLoja, abrirLootbox } from '../logic/lojaLogica';
import { GALOS_DB } from '../data/galosDb';
import { META_TIPOS } from '../data/tiposDb';
import { Galo } from '../logic/Galo';

export default function Loja() {
  const moedas = useJogadorStore(s => s.moedas);
  const galoCoins = useJogadorStore(s => s.galoCoins);
  const lojaDiaria = useJogadorStore(s => s.lojaDiaria);
  
  const pityBronze = useJogadorStore(s => s.pityBronze);
  const pityGold = useJogadorStore(s => s.pityGold);
  const pityEmerald = useJogadorStore(s => s.pityEmerald);
  
  const gastarMoeda = useJogadorStore(s => s.gastarMoeda);

  const galos = useJogadorStore(s => s.galos);
  const galoAtivoIndex = useJogadorStore(s => s.galoAtivoIndex);
  const venderGalo = useJogadorStore(s => s.venderGalo);

  const [tempoRestante, setTempoRestante] = useState("");
  const [logMessage, setLogMessage] = useState<{ text: string, isError: boolean } | null>(null);
  const [galoSorteado, setGaloSorteado] = useState<any>(null);

  const [galoSelecionadoParaVenda, setGaloSelecionadoParaVenda] = useState<{ galo: Galo, index: number } | null>(null);

  useEffect(() => {
    atualizarLojaDiaria();
    
    const interval = setInterval(() => {
      const agora = Date.now() / 1000;
      const faltam = Math.max(0, useJogadorStore.getState().lojaAtualizacao - agora);
      
      if (faltam === 0) {
        atualizarLojaDiaria();
      }
      
      const h = Math.floor(faltam / 3600);
      const m = Math.floor((faltam % 3600) / 60);
      setTempoRestante(h + "h " + m + "m");
      
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);

  const handleComprarDiario = (index: number) => {
    const item = lojaDiaria[index];
    if (item.comprado) return;
    
    const sucesso = comprarItemLoja(index);
    if (sucesso) {
      setLogMessage({ text: "Você comprou " + item.nome + "!", isError: false });
    } else {
      setLogMessage({ text: "Saldo insuficiente!", isError: true });
    }
  };

  const handleComprarLootbox = (tipo: "Bronze" | "Gold" | "Emerald", preco: number, moeda: "moedas" | "galo_coins") => {
    const sucesso = gastarMoeda(preco, moeda);
    if (!sucesso) {
      setLogMessage({ text: "Saldo insuficiente!", isError: true });
      return;
    }
    
    const galoGanho = abrirLootbox(tipo);
    setGaloSorteado(galoGanho);
  };

  const handleConfirmarVenda = () => {
    if (galoSelecionadoParaVenda) {
      venderGalo(galoSelecionadoParaVenda.index);
      setLogMessage({ text: "Galo vendido com sucesso!", isError: false });
      setGaloSelecionadoParaVenda(null);
    }
  };

  return (
    <div className="p-6 flex flex-col items-center max-w-4xl mx-auto w-full relative">
      <h2 className="text-3xl font-bold mb-6">Loja</h2>

      <div className="flex gap-8 mb-6 text-xl font-bold">
        <span className="text-amber-500">🪙 Moedas: {moedas}</span>
        <span className="text-amber-500">🐔 Galo Coins: {galoCoins}</span>
      </div>

      {logMessage && (
        <div className={"mb-6 p-3 rounded font-bold text-center w-full max-w-md " + (logMessage.isError ? 'bg-red-900/50 text-red-400' : 'bg-green-900/50 text-green-400')}>
          {logMessage.text}
        </div>
      )}

      <hr className="w-full border-zinc-700 my-6" />

      <h3 className="text-2xl font-bold mb-2">Loja Diária</h3>
      <p className="text-zinc-400 mb-6">Próxima atualização em: {tempoRestante}</p>

      <div className="flex flex-col gap-4 w-full max-w-md mb-8">
        {lojaDiaria.map((item, idx) => (
          <div key={idx} className="flex justify-between items-center bg-zinc-800 p-4 rounded-lg shadow">
            <span className="font-semibold text-lg">{item.nome} ({item.raridade})</span>
            {item.comprado ? (
              <span className="text-red-400 font-bold px-4 py-2">Esgotado</span>
            ) : (
              <button 
                onClick={() => handleComprarDiario(idx)}
                className="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded transition-colors"
              >
                {item.valor} {item.moeda === 'moedas' ? 'Moedas' : 'Galo Coins'}
              </button>
            )}
          </div>
        ))}
      </div>

      <hr className="w-full border-zinc-700 my-6" />

      <h3 className="text-2xl font-bold mb-8">Lootboxes</h3>

      <div className="flex flex-wrap justify-center gap-6 w-full">
        <div className="bg-orange-900/40 border border-orange-700 p-6 rounded-xl flex flex-col items-center w-64 shadow-lg">
          <h4 className="text-xl font-bold text-orange-400 mb-4">Caixa Bronze</h4>
          <button 
            onClick={() => handleComprarLootbox("Bronze", 400, "moedas")}
            className="bg-amber-600 hover:bg-amber-500 text-white font-bold py-3 w-full rounded mb-4 transition-colors"
          >
            400 Moedas
          </button>
          <span className="text-sm text-zinc-400 font-semibold">Pity Épico: {pityBronze}/15</span>
        </div>

        <div className="bg-yellow-900/40 border border-yellow-700 p-6 rounded-xl flex flex-col items-center w-64 shadow-lg">
          <h4 className="text-xl font-bold text-yellow-400 mb-4">Caixa Gold</h4>
          <button 
            onClick={() => handleComprarLootbox("Gold", 5000, "moedas")}
            className="bg-amber-600 hover:bg-amber-500 text-white font-bold py-3 w-full rounded mb-4 transition-colors"
          >
            5000 Moedas
          </button>
          <span className="text-sm text-zinc-400 font-semibold">Pity Lendário: {pityGold}/30</span>
        </div>

        <div className="bg-emerald-900/40 border border-emerald-700 p-6 rounded-xl flex flex-col items-center w-64 shadow-lg">
          <h4 className="text-xl font-bold text-emerald-400 mb-4">Caixa Emerald</h4>
          <button 
            onClick={() => handleComprarLootbox("Emerald", 5, "galo_coins")}
            className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 w-full rounded mb-4 transition-colors"
          >
            5 Galo Coins
          </button>
          <span className="text-sm text-zinc-400 font-semibold">Pity Mítico: {pityEmerald}/50</span>
        </div>
      </div>
      
      <hr className="w-full border-zinc-700 my-6" />

      <h3 className="text-2xl font-bold mb-8">Mercado de Vendas</h3>

      <div className="flex flex-wrap justify-center gap-4 w-full">
        {galos.map((galo, idx) => {
          const isAtivo = idx === galoAtivoIndex;
          const isOnly = galos.length <= 1;
          const canSell = !isAtivo && !isOnly;

          return (
            <div key={idx} className="bg-zinc-800 p-4 rounded-lg flex flex-col items-center w-40 shadow-lg border border-zinc-700">
              <img src={"/" + galo.caminho_imagem} alt={galo.nome} className="w-20 h-20 object-contain mb-2" />
              <h5 className="font-bold text-sm text-center mb-1">{galo.nome}</h5>
              <span className="text-xs text-zinc-400 mb-3">Nível {galo.nivel}</span>
              <button 
                onClick={() => setGaloSelecionadoParaVenda({ galo, index: idx })}
                disabled={!canSell}
                className={"w-full py-1 rounded text-sm font-bold transition-all " + (canSell ? "bg-red-900/50 text-red-400 hover:bg-red-800 hover:text-white border border-red-700" : "bg-zinc-700 text-zinc-500 cursor-not-allowed")}
              >
                Vender
              </button>
            </div>
          );
        })}
      </div>

      {galoSelecionadoParaVenda && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
          <div className="bg-zinc-900 border border-zinc-700 p-6 rounded-xl flex flex-col items-center max-w-sm w-full shadow-2xl">
            <h3 className="text-2xl font-bold mb-4">Confirmar Venda</h3>
            <img src={"/" + galoSelecionadoParaVenda.galo.caminho_imagem} alt={galoSelecionadoParaVenda.galo.nome} className="w-32 h-32 object-contain mb-4" />
            <p className="text-lg font-bold mb-1">{galoSelecionadoParaVenda.galo.nome}</p>
            <p className="text-sm text-zinc-400 mb-6">Nível {galoSelecionadoParaVenda.galo.nivel}</p>
            
            <div className="bg-zinc-800 w-full p-3 rounded text-center mb-6 border border-zinc-700">
              <span className="text-sm text-zinc-300 block mb-1">Valor de Venda:</span>
              <span className="text-xl font-bold text-amber-500">
                {calcularValorVenda(galoSelecionadoParaVenda.galo).valor} {calcularValorVenda(galoSelecionadoParaVenda.galo).moeda === 'moedas' ? 'Moedas' : 'Galo Coins'}
              </span>
            </div>

            <div className="flex gap-4 w-full">
              <button 
                onClick={() => setGaloSelecionadoParaVenda(null)}
                className="flex-1 py-2 rounded bg-zinc-700 hover:bg-zinc-600 text-white font-bold transition-colors"
              >
                Cancelar
              </button>
              <button 
                onClick={handleConfirmarVenda}
                className="flex-1 py-2 rounded bg-red-600 hover:bg-red-500 text-white font-bold transition-colors"
              >
                Confirmar Venda
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Recompensa Gacha */}
      {galoSorteado && (() => {
        const raridade = GALOS_DB[galoSorteado.nome]?.raridade || "Common";
        const isMythic = raridade === "Mythic";
        let rarityClasses = "ring-zinc-400 shadow-[0_0_30px_rgba(161,161,170,0.5)]";
        if (raridade === "Rare") rarityClasses = "ring-blue-600 shadow-[0_0_30px_rgba(37,99,235,0.5)]";
        else if (raridade === "Epic") rarityClasses = "ring-purple-500 shadow-[0_0_30px_rgba(168,85,247,0.5)]";
        else if (raridade === "Legendary") rarityClasses = "ring-orange-500 shadow-[0_0_30px_rgba(249,115,22,0.5)]";
        else if (raridade === "Special") rarityClasses = "ring-red-600 shadow-[0_0_30px_rgba(220,38,38,0.5)]";
        else if (raridade === "Divine") rarityClasses = "ring-fuchsia-500 shadow-[0_0_30px_rgba(217,70,239,0.5)]";

        const CardContent = (
          <div className={"bg-zinc-800 p-6 rounded-xl flex flex-col items-center ring-2 " + (isMythic ? "" : rarityClasses)}>
            <img src={"/" + galoSorteado.caminho_imagem} className="w-48 h-48 object-contain mb-4" alt={galoSorteado.nome} />
            <h3 className="text-3xl font-bold text-white mb-2 text-center">{galoSorteado.nome}</h3>
            <span className={`px-4 py-2 rounded-md text-xl font-bold mb-6 ${META_TIPOS[galoSorteado.tipo]?.corFundo || 'bg-zinc-800'} ${META_TIPOS[galoSorteado.tipo]?.corTexto || 'text-amber-500'}`}>
              {META_TIPOS[galoSorteado.tipo]?.icone || ''} {galoSorteado.tipo}
            </span>
            <button 
              onClick={() => setGaloSorteado(null)}
              className="w-full bg-amber-600 hover:bg-amber-500 text-white font-bold py-4 px-8 rounded-lg text-2xl transition-colors shadow-lg"
            >
              Coletar
            </button>
          </div>
        );

        return (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm">
            <div className="flex flex-col items-center animate-bounce-short scale-110">
              <h2 className="text-4xl md:text-5xl font-black text-amber-500 mb-8 drop-shadow-[0_0_15px_rgba(245,158,11,0.8)] text-center tracking-wider italic uppercase">
                Novo Galo Conquistado!
              </h2>
              
              {isMythic ? (
                <div className="bg-gradient-to-tr from-violet-500 via-orange-500 to-cyan-500 p-[3px] rounded-xl shadow-[0_0_30px_rgba(249,115,22,0.8)]">
                  {CardContent}
                </div>
              ) : (
                CardContent
              )}
            </div>
          </div>
        );
      })()}

    </div>
  );
}
