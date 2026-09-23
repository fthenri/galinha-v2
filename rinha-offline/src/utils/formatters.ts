export function formatarEfeitoString(nomeEfeito: string, rawString: string): string {
  let prefix = "";
  let baseValue = rawString;

  // Se a string já tiver sido montada em Codex.tsx com prefixos (ex: "100% · 2t · 15-20 Min damage")
  // Precisamos extrair o prefixo
  const parts = rawString.split("·");
  if (parts.length > 1) {
    // Pegar o último fragmento como baseValue e os anteriores como prefixo
    baseValue = parts.pop()?.trim() || "";
    prefix = parts.join("·").trim() + " · ";
  }

  // Removemos qualquer sufixo prévio que possa ter sido colocado, ficando apenas com os números/valores
  const justValue = baseValue.replace(" Min damage", "").trim();

  // Listas de categorias baseadas na regra do usuário
  const cura = ["Healing", "Refilling", "Brazilian Way", "Gluing Pieces", "Mummify", "Divine Healing", "Full Heal", "Crystallizing", "Redrawing", "Starring", "Warrior Dragon Aura", "Going Back in Time", "Regenerate Mass 1", "Regenerate Mass 2", "Regenerate Mass 3", "Celestial Light", "Immaculate Aura", "Paradise Blessing", "Veil of Sanctity", "Heavenly Healing", "Guardian Heal", "Ascension to Heaven", "Salvation Aura", "Cthulhu Regeneration", "Cthulhu Dream", "Dagon", "Cthulhu Ascension", "Healing Surge"];
  const danoASiMesmo = ["Depression", "Strong Depression", "Menstruation", "Knife", "Cursed Blessing"];
  const reducaoDano = ["Shield", "Iron Box", "Iron Maiden", "Divine Shield", "Protected", "More Resistant", "Turn Into Air", "Rigorously Bandaged", "Kevlar Wrapped", "Empowered Slime", "Corpse Protection", "Censored", "Hiding", "Erase Attacks", "Cancel Attacks", "Guardian Shield", "Supreme Guardian Shield", "Divine Guardian Shield"];
  const atordoamento = ["Stun", "Lack of Resources", "Confusion"];
  const fragilidade = ["Fragility", "Frightened", "Malnutrition", "Haunted", "Transcend", "Aging", "Fragile Existence 1", "Fragile Existence 2", "Berserker Fragility", "Glass Mantle", "Critical Exposure", "Imminent Impact"];
  const rouboVida = ["Life Steal", "Trade Blood For Food"];
  const bloqueioAbsoluto = ["Barrier", "Supreme Barrier"];
  const reflexao = ["Reflection"];

  let novoSufixo = "";

  if (cura.includes(nomeEfeito)) {
    novoSufixo = `${justValue} Min heal`;
  } else if (danoASiMesmo.includes(nomeEfeito)) {
    const nums = justValue.match(/\d+/g);
    const finalVal = nums && nums.length >= 2 ? `${nums[0]}-${nums[1]}` : (nums ? nums[0] : "");
    novoSufixo = `${finalVal} Self-damage`;
  } else if (reducaoDano.includes(nomeEfeito)) {
    const num = justValue.replace(/-/g, "");
    novoSufixo = `Reduced damage ${num}%`;
  } else if (atordoamento.includes(nomeEfeito)) {
    novoSufixo = `Stun: 1 turn`;
  } else if (nomeEfeito === "Double Stun") {
    novoSufixo = `Stun: 2 turns`;
  } else if (fragilidade.includes(nomeEfeito)) {
    const num = justValue.replace(/-/g, "");
    novoSufixo = `Fragility ${num}%`;
  } else if (rouboVida.includes(nomeEfeito)) {
    novoSufixo = `damage dealt = damage healed`;
  } else if (bloqueioAbsoluto.includes(nomeEfeito)) {
    novoSufixo = `block 100%`;
  } else if (reflexao.includes(nomeEfeito)) {
    novoSufixo = `Reflect next attack`;
  } else {
    // Dano Padrão
    novoSufixo = `${justValue} Min damage`;
  }

  return prefix + novoSufixo;
}
