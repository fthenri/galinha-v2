import { Galo } from './Galo';

export function aplicarVariacaoHp(galo: Galo, nomeEfeito: string, minVal: number, maxVal: number, isHeal: boolean = false): [string, boolean] {
    const valor = Math.floor(Math.random() * (maxVal - minVal + 1)) + minVal;
    if (isHeal) {
        galo.hp_atual = Math.min(galo.hp_max, galo.hp_atual + valor);
        return [`${galo.nome} recuperou ${valor} HP por ${nomeEfeito}.`, true];
    } else {
        galo.hp_atual -= valor;
        return [`${galo.nome} perdeu ${valor} HP por ${nomeEfeito}.`, true];
    }
}

export function aplicarImobilizacao(galo: Galo, nomeEfeito: string): [string, boolean] {
    return [`${galo.nome} está imobilizado (${nomeEfeito}) e perdeu o turno!`, false];
}

export function modificarDano(dano: number, percentual: number): number {
    return Math.max(0, Math.floor(dano * (1 + (percentual / 100))));
}

export const BUFFS: string[] = [
    // Curas
    "Healing", "Powerful Healing", "Refilling", "Brazilian Way", "Gluing Pieces", 
    "Mummify", "Divine Healing", "Full Heal", "Crystallizing", "Infinite Healing", 
    "Redrawing", "Starring", "Warrior Dragon Aura", "Going Back in Time", 
    "Regenerate Mass 1", "Regenerate Mass 2", "Regenerate Mass 3", "Celestial Light", 
    "Immaculate Aura", "Paradise Blessing", "Veil of Sanctity", "Heavenly Healing", 
    "Guardian Heal", "Ascension to Heaven", "Salvation Aura", "Cthulhu Regeneration", 
    "Cthulhu Dream", "Dagon", "Cthulhu Ascension", "Healing Surge",
    
    // Escudos e Mitigações
    "Shield", "Iron Box", "Iron Maiden", "Divine Shield", "Protected", 
    "More Resistant", "Turn Into Air", "Rigorously Bandaged", "Kevlar Wrapped", 
    "Empowered Slime", "Censored", "Hiding", "Corpse Protection", "Barrier", 
    "Supreme Barrier", "Going to the Future", "Erase Attacks", "Cancel Attacks", 
    "Guardian Shield", "Supreme Guardian Shield", "Divine Guardian Shield", 
    
    // Efeitos Especiais Positivos
    "Reflection", "Life Steal", "Trade Blood For Food"
];

// O uso do Record e de funções (galo, nome) => [string, boolean] tipa os gatilhos corretamente em TS.
export const EFEITOS_INICIO_TURNO: Record<string, (galo: Galo, nome: string) => [string, boolean]> = {
    // Damage Over Time (DoTs)
    "Bleeding": (g, n) => aplicarVariacaoHp(g, n, 5, 20),
    "Hemorrhage": (g, n) => aplicarVariacaoHp(g, n, 5, 20),
    "Origami": (g, n) => aplicarVariacaoHp(g, n, 3, 10),
    "Strong Bleeding": (g, n) => aplicarVariacaoHp(g, n, 30, 43),
    "Flames": (g, n) => aplicarVariacaoHp(g, n, 5, 15),
    "Powerful Flames": (g, n) => aplicarVariacaoHp(g, n, 16, 26),
    "Cremation": (g, n) => aplicarVariacaoHp(g, n, 30, 40),
    "Hypothermia": (g, n) => aplicarVariacaoHp(g, n, 9, 10),
    "Absolute Zero": (g, n) => aplicarVariacaoHp(g, n, 14, 15),
    "Acid": (g, n) => aplicarVariacaoHp(g, n, 5, 10),
    "Poison": (g, n) => aplicarVariacaoHp(g, n, 15, 20),
    "Strong Acid": (g, n) => aplicarVariacaoHp(g, n, 11, 15),
    "Divine Acid": (g, n) => aplicarVariacaoHp(g, n, 20, 35),
    "Internal Hemorrhage": (g, n) => aplicarVariacaoHp(g, n, 15, 25),
    "Allergic": (g, n) => aplicarVariacaoHp(g, n, 7, 12),
    "Frustrated": (g, n) => aplicarVariacaoHp(g, n, 14, 17),
    "Dense Plasma": (g, n) => aplicarVariacaoHp(g, n, 10, 25),
    "Supreme Cremation": (g, n) => aplicarVariacaoHp(g, n, 35, 43),
    "Curse": (g, n) => aplicarVariacaoHp(g, n, 10, 20),
    "Plasma": (g, n) => aplicarVariacaoHp(g, n, 1, 15),
    "Divine Plasma": (g, n) => aplicarVariacaoHp(g, n, 10, 35),
    "Micro Robots": (g, n) => aplicarVariacaoHp(g, n, 10, 15),
    "Shock": (g, n) => aplicarVariacaoHp(g, n, 6, 15),
    "Strong Shock": (g, n) => aplicarVariacaoHp(g, n, 15, 25),
    "Sandstorm": (g, n) => aplicarVariacaoHp(g, n, 12, 17),
    "Golem": (g, n) => aplicarVariacaoHp(g, n, 20, 22),
    "Radiation": (g, n) => aplicarVariacaoHp(g, n, 4, 8),
    "Strong Radiation": (g, n) => aplicarVariacaoHp(g, n, 10, 14),
    "Oxygen Suction": (g, n) => aplicarVariacaoHp(g, n, 10, 20),
    "Battalion": (g, n) => aplicarVariacaoHp(g, n, 40, 50),
    "Persecution": (g, n) => aplicarVariacaoHp(g, n, 10, 20),
    "Necrosis": (g, n) => aplicarVariacaoHp(g, n, 15, 20),
    "Ink": (g, n) => aplicarVariacaoHp(g, n, 22, 27),
    "Black Ink": (g, n) => aplicarVariacaoHp(g, n, 25, 35),
    "Death": (g, n) => aplicarVariacaoHp(g, n, 70, 85),
    "Gravitational Attraction": (g, n) => aplicarVariacaoHp(g, n, 1, 30),
    "Solar Cremation": (g, n) => aplicarVariacaoHp(g, n, 55, 70),
    "Gravitational Field": (g, n) => aplicarVariacaoHp(g, n, 15, 23),
    "Cold Moonlight": (g, n) => aplicarVariacaoHp(g, n, 12, 20),
    "Possession": (g, n) => aplicarVariacaoHp(g, n, 20, 35),
    "Eternal Eclipse": (g, n) => aplicarVariacaoHp(g, n, 60, 90),
    "Degeneration": (g, n) => aplicarVariacaoHp(g, n, 10, 15),
    "Zombie Attack": (g, n) => aplicarVariacaoHp(g, n, 18, 30),
    "Powerful Degeneration": (g, n) => aplicarVariacaoHp(g, n, 20, 35),
    "Covered By Ink": (g, n) => aplicarVariacaoHp(g, n, 10, 15),
    "Exploding": (g, n) => aplicarVariacaoHp(g, n, 5, 30),
    "Hypnotized": (g, n) => aplicarVariacaoHp(g, n, 70, 120),
    "Disease": (g, n) => aplicarVariacaoHp(g, n, 10, 15),
    "Dissolving": (g, n) => aplicarVariacaoHp(g, n, 10, 20),
    "Infinite Mirage": (g, n) => aplicarVariacaoHp(g, n, 40, 50),
    "Hypnotized Music": (g, n) => aplicarVariacaoHp(g, n, 9, 12),
    "Sonic Explosion": (g, n) => aplicarVariacaoHp(g, n, 30, 40),
    "Final Melody": (g, n) => aplicarVariacaoHp(g, n, 45, 75),
    "Stellar Ruin Howl": (g, n) => aplicarVariacaoHp(g, n, 50, 60),
    "Cresset": (g, n) => aplicarVariacaoHp(g, n, 50, 70),
    "Phoenix Fire": (g, n) => aplicarVariacaoHp(g, n, 110, 130),
    "Fading Existence": (g, n) => aplicarVariacaoHp(g, n, 5, 10),
    "Fire": (g, n) => aplicarVariacaoHp(g, n, 7, 12),
    "White Fire": (g, n) => aplicarVariacaoHp(g, n, 20, 40),
    "Pure Flame": (g, n) => aplicarVariacaoHp(g, n, 30, 45),
    "Purifying Touch": (g, n) => aplicarVariacaoHp(g, n, 60, 75),
    "Ancestral Purity": (g, n) => aplicarVariacaoHp(g, n, 160, 200),
    "Eternal Blessing": (g, n) => aplicarVariacaoHp(g, n, 45, 55),
    "Illuminated Destiny": (g, n) => aplicarVariacaoHp(g, n, 55, 75),
    "Divine Trial": (g, n) => aplicarVariacaoHp(g, n, 45, 65),
    "Infernal Bite": (g, n) => aplicarVariacaoHp(g, n, 60, 80),
    "Silent Tide": (g, n) => aplicarVariacaoHp(g, n, 30, 50),
    "Cthulhu Bite": (g, n) => aplicarVariacaoHp(g, n, 80, 120),
    "Cthulhu Fury": (g, n) => aplicarVariacaoHp(g, n, 150, 320),
    "Orbital Bleeding": (g, n) => aplicarVariacaoHp(g, n, 10, 15),
    "Keyblade Bleeding": (g, n) => aplicarVariacaoHp(g, n, 12, 25),
    "Sonic Rush": (g, n) => aplicarVariacaoHp(g, n, 100, 150),
    
    // Negative HoTs
    "Depression": (g, n) => aplicarVariacaoHp(g, n, 10, 15),
    "Strong Depression": (g, n) => aplicarVariacaoHp(g, n, 30, 45),
    "Menstruation": (g, n) => aplicarVariacaoHp(g, n, 40, 55),
    "Knife": (g, n) => aplicarVariacaoHp(g, n, 30, 30),
    "Cursed Blessing": (g, n) => aplicarVariacaoHp(g, n, 15, 15),

    // Heal Over Time (HoTs)
    "Healing": (g, n) => aplicarVariacaoHp(g, n, 5, 10, true),
    "Powerful Healing": (g, n) => aplicarVariacaoHp(g, n, 10, 20, true),
    "Refilling": (g, n) => aplicarVariacaoHp(g, n, 5, 10, true),
    "Brazilian Way": (g, n) => aplicarVariacaoHp(g, n, 15, 25, true),
    "Gluing Pieces": (g, n) => aplicarVariacaoHp(g, n, 10, 15, true),
    "Mummify": (g, n) => aplicarVariacaoHp(g, n, 8, 15, true),
    "Divine Healing": (g, n) => aplicarVariacaoHp(g, n, 15, 25, true),
    "Full Heal": (g, n) => aplicarVariacaoHp(g, n, 80, 100, true),
    "Crystallizing": (g, n) => aplicarVariacaoHp(g, n, 17, 25, true),
    "Infinite Healing": (g, n) => aplicarVariacaoHp(g, n, 160, 320, true),
    "Redrawing": (g, n) => aplicarVariacaoHp(g, n, 15, 25, true),
    "Starring": (g, n) => aplicarVariacaoHp(g, n, 50, 80, true),
    "Warrior Dragon Aura": (g, n) => aplicarVariacaoHp(g, n, 37, 50, true),
    "Going Back in Time": (g, n) => aplicarVariacaoHp(g, n, 95, 135, true),
    "Regenerate Mass 1": (g, n) => aplicarVariacaoHp(g, n, 5, 10, true),
    "Regenerate Mass 2": (g, n) => aplicarVariacaoHp(g, n, 15, 25, true),
    "Regenerate Mass 3": (g, n) => aplicarVariacaoHp(g, n, 90, 125, true),
    "Celestial Light": (g, n) => aplicarVariacaoHp(g, n, 45, 50, true),
    "Immaculate Aura": (g, n) => aplicarVariacaoHp(g, n, 50, 65, true),
    "Paradise Blessing": (g, n) => aplicarVariacaoHp(g, n, 70, 90, true),
    "Veil of Sanctity": (g, n) => aplicarVariacaoHp(g, n, 85, 135, true),
    "Heavenly Healing": (g, n) => aplicarVariacaoHp(g, n, 260, 330, true),
    "Guardian Heal": (g, n) => aplicarVariacaoHp(g, n, 80, 200, true),
    "Ascension to Heaven": (g, n) => aplicarVariacaoHp(g, n, 40, 45, true),
    "Salvation Aura": (g, n) => aplicarVariacaoHp(g, n, 100, 165, true),
    "Cthulhu Regeneration": (g, n) => aplicarVariacaoHp(g, n, 60, 100, true),
    "Cthulhu Dream": (g, n) => aplicarVariacaoHp(g, n, 120, 200, true),
    "Dagon": (g, n) => aplicarVariacaoHp(g, n, 185, 300, true),
    "Cthulhu Ascension": (g, n) => aplicarVariacaoHp(g, n, 250, 450, true),
    "Healing Surge": (g, n) => aplicarVariacaoHp(g, n, 150, 350, true),

    // Stuns
    "Stun": aplicarImobilizacao,
    "Confusion": aplicarImobilizacao,
    "Lack of Resources": aplicarImobilizacao,
    "Double Stun": aplicarImobilizacao
};

export const EFEITOS_DANO_RECEBIDO: Record<string, (d: number) => number> = {
    // Reduções de Dano
    "Shield": (d) => modificarDano(d, -50),
    "Iron Box": (d) => modificarDano(d, -20),
    "Iron Maiden": (d) => modificarDano(d, -20),
    "Divine Shield": (d) => modificarDano(d, -70),
    "Protected": (d) => modificarDano(d, -20),
    "More Resistant": (d) => modificarDano(d, -40),
    "Turn Into Air": (d) => modificarDano(d, -100),
    "Rigorously Bandaged": (d) => modificarDano(d, -20),
    "Kevlar Wrapped": (d) => modificarDano(d, -50),
    "Empowered Slime": (d) => modificarDano(d, -30),
    "Censored": (d) => modificarDano(d, -70),
    "Hiding": (d) => modificarDano(d, -100),
    "Corpse Protection": (d) => modificarDano(d, -50),
    "Barrier": (d) => modificarDano(d, -100),
    "Supreme Barrier": (d) => modificarDano(d, -100),
    "Going to the Future": (d) => modificarDano(d, -100),
    "Erase Attacks": (d) => modificarDano(d, -50),
    "Cancel Attacks": (d) => modificarDano(d, -100),
    "Guardian Shield": (d) => modificarDano(d, -75),
    "Supreme Guardian Shield": (d) => modificarDano(d, -120),
    "Divine Guardian Shield": (d) => modificarDano(d, -200),
    "Reflection": (d) => modificarDano(d, -100),

    // Aumento de Dano
    "Fragility": (d) => modificarDano(d, 90),
    "Frightened": (d) => modificarDano(d, 35),
    "Haunted": (d) => modificarDano(d, 55),
    "Malnutrition": (d) => modificarDano(d, 15),
    "Transcend": (d) => modificarDano(d, 170),
    "Aging": (d) => modificarDano(d, 240),
    "Fragile Existence 1": (d) => modificarDano(d, 35),
    "Fragile Existence 2": (d) => modificarDano(d, 200),
    "Berserker Fragility": (d) => modificarDano(d, 300),
    "Glass Mantle": (d) => modificarDano(d, 50),
    "Critical Exposure": (d) => modificarDano(d, 75),
    "Imminent Impact": (d) => modificarDano(d, 150)
};

