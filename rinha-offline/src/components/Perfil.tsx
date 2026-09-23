import { useState } from "react";
import { useJogadorStore, calcularNivelRebirth, calcularBonusTrial } from '../store/jogadorStore';
import { Galo } from '../logic/Galo';
import { GALOS_DB } from '../data/galosDb';
import { META_TIPOS } from '../data/tiposDb';

import { ITENS_DB } from '../data/itensDb';

function GaloCard({ galo, galoIndex, isAtivo, onEquipar, onOpenEvolucao, onOpenRebirth, onOpenItem, onOpenTrial }: { galo: Galo, galoIndex: number, isAtivo: boolean, onEquipar: () => void, onOpenEvolucao: (idx: number) => void, onOpenRebirth: (idx: number) => void, onOpenItem: (idx: number) => void, onOpenTrial: (idx: number) => void }) {
  const alterarSkillSlot = useJogadorStore(s => s.alterarSkillSlot);
  const equiparItem = useJogadorStore(s => s.equiparItem);
  const desbloqueadas = [...galo.obterSkillsDesbloqueadas()].sort((a, b) => a.level - b.level);
  
  const handleSelectChange = (slotIndex: number, val: string) => {
    const alreadySelected = galo.skills_equipadas.some((s, i) => s && s.nome === val && i !== slotIndex);
    if (alreadySelected && val !== "") return;
    alterarSkillSlot(galoIndex, slotIndex, val === "" ? null : val);
  };

  const isDisabled = desbloqueadas.length < 6;
  const raridade = GALOS_DB[galo.nome]?.raridade || "Common";

  let borderClass = "";
  let glowClass = "";
  let itemRarityColor = "text-zinc-400";

  const itemObj = galo.item_equipado ? ITENS_DB?.[galo.item_equipado] : null;
  if (itemObj) {
    if (itemObj.raridade === "Rare") itemRarityColor = "text-blue-500";
    else if (itemObj.raridade === "Epic") itemRarityColor = "text-purple-500";
    else if (itemObj.raridade === "Legendary") itemRarityColor = "text-orange-500";
    else if (itemObj.raridade === "Special") itemRarityColor = "text-red-500";
    else if (itemObj.raridade === "Mythic") itemRarityColor = "text-fuchsia-500";
  }

  switch (raridade) {
    case "Rare":
      borderClass = "ring-2 ring-blue-600";
      glowClass = "shadow-[0_0_20px_rgba(37,99,235,0.5)]";
      break;
    case "Epic":
      borderClass = "ring-2 ring-purple-500";
      glowClass = "shadow-[0_0_20px_rgba(168,85,247,0.5)]";
      break;
    case "Legendary":
      borderClass = "ring-2 ring-orange-500";
      glowClass = "shadow-[0_0_20px_rgba(249,115,22,0.5)]";
      break;
    case "Special":
      borderClass = "ring-2 ring-red-600";
      glowClass = "shadow-[0_0_20px_rgba(220,38,38,0.5)]";
      break;
    case "Divine":
      borderClass = "ring-2 ring-fuchsia-500";
      glowClass = "shadow-[0_0_20px_rgba(217,70,239,0.5)]";
      break;
    case "Mythic":
      borderClass = ""; 
      glowClass = "shadow-[0_0_20px_rgba(249,115,22,0.5)]";
      break;
    case "Common":
    default:
      borderClass = "ring-2 ring-zinc-400";
      glowClass = "shadow-[0_0_20px_rgba(161,161,170,0.5)]";
      break;
  }

  const bgClass = isAtivo ? 'bg-slate-800' : 'bg-zinc-800';
  const finalShadow = isAtivo ? glowClass : 'shadow-lg';

  const innerContent = (
    <>
      <img src={`/${galo.caminho_imagem}`} alt={galo.nome} className="w-36 h-36 object-contain mb-4" />
      <h3 className="text-xl font-bold mb-2">{galo.nome}</h3>
      <div className="flex gap-2 mb-2">
        <span className={`px-2 py-1 rounded-md text-xs font-bold ${META_TIPOS[galo.tipo]?.corFundo || 'bg-zinc-900'} ${META_TIPOS[galo.tipo]?.corTexto || 'text-zinc-300'}`}>
          {META_TIPOS[galo.tipo]?.icone || ''} {galo.tipo}
        </span>
        <span className="px-2 py-1 rounded-md text-xs font-bold bg-zinc-900 text-zinc-300">Nível: {galo.nivel} | RB: {galo.rebirths || 0}</span>
      </div>
      <p className="text-red-400 font-bold mb-4">HP: {galo.hp_max}</p>
      
      <button 
        onClick={onEquipar}
        disabled={isAtivo}
        className={`px-4 py-2 rounded font-bold mb-6 transition-all ${isAtivo ? 'opacity-0 cursor-default' : 'bg-amber-600 hover:bg-amber-500 text-white shadow-lg'}`}
      >
        Equipar Galo
      </button>

      <hr className="w-full border-zinc-700 mb-4" />
      
      <h4 className="text-sm font-bold mb-4">EQUIPAMENTO</h4>
      {itemObj ? (
        <div className="flex items-center justify-between bg-zinc-900 border border-zinc-700 p-3 rounded-lg w-full mb-6">
          <div className="flex flex-col text-left">
            <span className={`font-bold ${itemRarityColor}`}>{itemObj.nome}</span>
            <span className="text-xs text-zinc-500">{itemObj.raridade}</span>
            <span className="text-xs text-zinc-400 mt-1.5 leading-snug">{itemObj.descricao}</span>
          </div>
          <button 
            onClick={() => equiparItem(galoIndex, null)}
            className="text-zinc-500 hover:text-red-500 transition-colors font-bold text-lg px-2"
          >
            ✕
          </button>
        </div>
      ) : (
        <button 
          onClick={() => onOpenItem(galoIndex)}
          className="border-2 border-dashed border-zinc-700 text-zinc-500 hover:text-zinc-300 hover:border-zinc-500 p-3 rounded-lg w-full mb-6 transition-colors"
        >
          + Equipar Item
        </button>
      )}

      <h4 className="text-sm font-bold mb-4">HABILIDADES EQUIPADAS</h4>

      <div className="flex flex-col gap-2 w-full">
        {galo.skills_equipadas.map((skillObj, i) => {
          const val = skillObj ? skillObj.nome : "";
          const skillsInOutrosSlots = galo.skills_equipadas.filter((s, idx) => s && idx !== i).map(s => s?.nome);
          
          return (
            <select
              key={i}
              value={val}
              onChange={(e) => handleSelectChange(i, e.target.value)}
              disabled={isDisabled}
              className="bg-zinc-900 text-white p-2 rounded w-full border border-zinc-700 text-sm focus:outline-none focus:ring-1 focus:ring-amber-500 disabled:opacity-50 transition-colors"
            >
              {!val && <option value="">-- Vazio --</option>}
              {desbloqueadas.map((d) => {
                if (skillsInOutrosSlots.includes(d.skill.nome)) return null;
                return (
                  <option key={d.skill.nome} value={d.skill.nome}>
                    [Nv.{d.level}] {d.skill.nome} ({d.skill.min} - {d.skill.max})
                  </option>
                );
              })}
            </select>
          );
        })}
      </div>

            <button
        onClick={() => onOpenRebirth(galoIndex)}
        className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold py-2 rounded-lg mt-4 w-full hover:from-purple-500 hover:to-indigo-500 shadow-lg transition-all"
      >
        Rebirth
      </button>
      <button
        onClick={() => onOpenEvolucao(galoIndex)}
        className="bg-gradient-to-r from-amber-500 to-yellow-600 text-black font-bold py-2 rounded-lg mt-2 w-full hover:from-amber-400 hover:to-yellow-500 shadow-lg transition-all"
      >
        Evolução
      </button>
      <button
        onClick={() => onOpenTrial(galoIndex)}
        className="bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-bold py-2 rounded-lg mt-2 w-full hover:from-cyan-500 hover:to-blue-500 shadow-lg transition-all"
      >
        Trial do Tipo
      </button>
    </>
  );

  if (raridade === "Mythic") {
    return (
      <div className={`w-80 rounded-xl p-[2px] transition-all duration-300 hover:-translate-y-1 hover:shadow-xl bg-gradient-to-tr from-violet-500 via-orange-500 to-cyan-500 ${isAtivo ? glowClass : 'shadow-lg'}`}>
        <div className={`p-5 rounded-lg flex flex-col items-center w-full h-full ${bgClass}`}>
          {innerContent}
        </div>
      </div>
    );
  }

  return (
    <div className={`p-5 rounded-lg flex flex-col items-center w-80 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl ${bgClass} ${borderClass} ${finalShadow}`}>
      {innerContent}
    </div>
  );
}

export default function Perfil() {
  const { nome, moedas, galoCoins, galos, galoAtivoIndex, setGaloAtivo } = useJogadorStore();
  const [modalEvolucao, setModalEvolucao] = useState<number | null>(null);
  const [modalRebirth, setModalRebirth] = useState<number | null>(null);
  const [modalItemGaloIndex, setModalItemGaloIndex] = useState<number | null>(null);
  const [modalTrialGalo, setModalTrialGalo] = useState<number | null>(null);

  return (
    <div className="p-6 flex flex-col items-center">
      <h2 className="text-3xl font-bold mb-4">Perfil de {nome}</h2>
      <p className="text-lg text-amber-500 mb-6 font-semibold">
        🪙 Moedas: {moedas} | 🐔 Galo Coins: {galoCoins}
      </p>
      
      <div className="w-full max-w-6xl border-t border-zinc-700 my-6"></div>
      
      <h3 className="text-2xl font-bold mb-8">Seu Time (Galos):</h3>

      <div className="flex flex-wrap justify-center gap-6">
        {galos.map((galo, idx) => (
          <GaloCard 
            key={idx} 
            galo={galo} 
            galoIndex={idx}
            isAtivo={idx === galoAtivoIndex} 
            onEquipar={() => setGaloAtivo(idx)}
            onOpenEvolucao={setModalEvolucao}
            onOpenRebirth={setModalRebirth}
            onOpenItem={setModalItemGaloIndex}
            onOpenTrial={setModalTrialGalo}
          />
        ))}

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

      {modalItemGaloIndex !== null && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm p-4">
          <div className="bg-zinc-900 border border-zinc-700 p-6 rounded-2xl w-full max-w-2xl max-h-[90vh] flex flex-col">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white">Selecione um Item (Modo Teste)</h2>
              <button 
                onClick={() => setModalItemGaloIndex(null)}
                className="text-zinc-500 hover:text-white font-bold text-xl px-2"
              >
                ✕
              </button>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 overflow-y-auto pr-2 flex-1 max-h-[70vh]">
              {Object.entries(ITENS_DB || {}).map(([id, item]) => {
                let itemRarityColor = "text-zinc-400";
                if (item.raridade === "Rare") itemRarityColor = "text-blue-500";
                else if (item.raridade === "Epic") itemRarityColor = "text-purple-500";
                else if (item.raridade === "Legendary") itemRarityColor = "text-orange-500";
                else if (item.raridade === "Special") itemRarityColor = "text-red-500";
                else if (item.raridade === "Mythic") itemRarityColor = "text-fuchsia-500";

                return (
                  <button
                    key={id}
                    onClick={() => {
                      useJogadorStore.getState().equiparItem(modalItemGaloIndex, id);
                      setModalItemGaloIndex(null);
                    }}
                    className="flex flex-col bg-zinc-800 border border-zinc-700 hover:border-zinc-500 p-4 rounded-xl transition-all text-left"
                  >
                    <span className={`font-bold text-lg mb-1 ${itemRarityColor}`}>{item.nome}</span>
                    <span className="text-xs text-zinc-500 font-semibold">{item.raridade}</span>
                    <span className="text-xs text-zinc-400 mt-1.5 leading-snug">{item.descricao}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {modalTrialGalo !== null && (() => {
          const galo = galos[modalTrialGalo];
          const trialsAtual = useJogadorStore.getState().trialsPorClasse[galo.nome] || 0;
          const bonus = calcularBonusTrial(trialsAtual);
          const bloqueado = trialsAtual >= 20 || galo.nivel < 15;
          
          return (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm p-4">
              <div className="bg-zinc-900 border border-zinc-700 p-6 rounded-2xl w-full max-w-md flex flex-col items-center text-center shadow-2xl">
                <h2 className="text-3xl font-bold text-white mb-2">Trial de {galo.nome}</h2>
                <p className="text-zinc-400 mb-6">Vença desafios desta classe para conceder bônus globais para todos os galos da mesma espécie.</p>

                <div className="w-full bg-zinc-800 rounded-xl p-4 mb-4 border border-zinc-700/50">
                  <h3 className="text-lg font-bold text-zinc-300 mb-2">Progresso Atual</h3>
                  <div className="text-2xl font-black text-cyan-400 mb-4">{trialsAtual} / 20</div>
                  <div className="flex justify-between w-full text-sm text-zinc-400">
                    <span>Bônus de Dano: <strong className="text-green-400">{(bonus.dano * 100).toFixed(0)}%</strong></span>
                    <span>Bônus de Vida: <strong className="text-green-400">{(bonus.vida * 100).toFixed(0)}%</strong></span>
                  </div>
                </div>
                
                {galo.nivel < 15 && (
                    <div className="w-full p-3 rounded-lg mb-6 font-bold bg-red-500/20 text-red-400">
                        Requer Nível 15 para participar
                    </div>
                )}

                <div className="w-full flex gap-4">
                  <button 
                    onClick={() => setModalTrialGalo(null)}
                    className="flex-1 bg-zinc-800 hover:bg-zinc-700 text-white font-bold py-3 px-4 rounded-xl transition-all"
                  >
                    Cancelar
                  </button>
                  <button 
                    disabled={bloqueado}
                    onClick={() => {
                        useJogadorStore.getState().setTrialMode(true);
                        setGaloAtivo(modalTrialGalo);
                        setModalTrialGalo(null);
                        window.dispatchEvent(new CustomEvent('changeTab', { detail: { tab: 'treino' } }));
                    }}
                    className={`flex-1 font-bold py-3 px-4 rounded-xl transition-all ${bloqueado ? 'bg-cyan-900/50 text-cyan-500/50 cursor-not-allowed' : 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-lg hover:scale-105'}`}
                  >
                    {trialsAtual >= 20 ? 'Maximizada' : 'Iniciar Trial'}
                  </button>
                </div>
              </div>
            </div>
          );
      })()}

      </div>
    </div>
  );
}
