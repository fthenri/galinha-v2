import { useJogadorStore } from '../store/jogadorStore';
import { Galo } from '../logic/Galo';
import { GALOS_DB } from '../data/galosDb';
import { META_TIPOS } from '../data/tiposDb';

function GaloCard({ galo, galoIndex, isAtivo, onEquipar }: { galo: Galo, galoIndex: number, isAtivo: boolean, onEquipar: () => void }) {
  const alterarSkillSlot = useJogadorStore(s => s.alterarSkillSlot);
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
        <span className="px-2 py-1 rounded-md text-xs font-bold bg-zinc-900 text-zinc-300">Nível: {galo.nivel}</span>
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
          />
        ))}
      </div>
    </div>
  );
}
