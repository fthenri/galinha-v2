import random

# --- MOTORES BASE ---
def aplicar_variacao_hp(galo, nome_efeito, min_val, max_val, is_heal=False):
    valor = random.randint(min_val, max_val)
    if is_heal:
        galo.hp_atual = min(galo.hp_max, galo.hp_atual + valor)
        return f"{galo.nome} recuperou {valor} HP por {nome_efeito}.", True
    else:
        galo.hp_atual -= valor
        return f"{galo.nome} perdeu {valor} HP por {nome_efeito}.", True

def aplicar_imobilizacao(galo, nome_efeito):
    return f"{galo.nome} está imobilizado ({nome_efeito}) e perdeu o turno!", False

def modificar_dano(dano, percentual):
    # Valores negativos mitigam dano (Shield), valores positivos aumentam (Fragility)
    return max(0, int(dano * (1 + (percentual / 100))))


# --- LISTA GLOBAL DE BUFFS (Para o rinha.py saber em quem aplicar) ---
BUFFS = [
    # Curas
    "Healing", "Powerful Healing", "Refilling", "Brazilian Way", "Gluing Pieces", 
    "Mummify", "Divine Healing", "Full Heal", "Crystallizing", "Infinite Healing", 
    "Redrawing", "Starring", "Warrior Dragon Aura", "Going Back in Time", 
    "Regenerate Mass 1", "Regenerate Mass 2", "Regenerate Mass 3", "Celestial Light", 
    "Immaculate Aura", "Paradise Blessing", "Veil of Sanctity", "Heavenly Healing", 
    "Guardian Heal", "Ascension to Heaven", "Salvation Aura", "Cthulhu Regeneration", 
    "Cthulhu Dream", "Dagon", "Cthulhu Ascension", "Healing Surge",
    
    # Escudos e Mitigações
    "Shield", "Iron Box", "Iron Maiden", "Divine Shield", "Protected", 
    "More Resistant", "Turn Into Air", "Rigorously Bandaged", "Kevlar Wrapped", 
    "Empowered Slime", "Censored", "Hiding", "Corpse Protection", "Barrier", 
    "Supreme Barrier", "Going to the Future", "Erase Attacks", "Cancel Attacks", 
    "Guardian Shield", "Supreme Guardian Shield", "Divine Guardian Shield", 
    
    # Efeitos Especiais Positivos
    "Reflection", "Life Steal", "Trade Blood For Food"
]


# --- DICIONÁRIOS DE GATILHO (Trigger Dictionaries) ---

EFEITOS_INICIO_TURNO = {
    # Damage Over Time (DoTs)
    "Bleeding": lambda g, n: aplicar_variacao_hp(g, n, 5, 20),
    "Hemorrhage": lambda g, n: aplicar_variacao_hp(g, n, 5, 20),
    "Origami": lambda g, n: aplicar_variacao_hp(g, n, 3, 10),
    "Strong Bleeding": lambda g, n: aplicar_variacao_hp(g, n, 30, 43),
    "Flames": lambda g, n: aplicar_variacao_hp(g, n, 5, 15),
    "Powerful Flames": lambda g, n: aplicar_variacao_hp(g, n, 16, 26),
    "Cremation": lambda g, n: aplicar_variacao_hp(g, n, 30, 40),
    "Hypothermia": lambda g, n: aplicar_variacao_hp(g, n, 9, 10),
    "Absolute Zero": lambda g, n: aplicar_variacao_hp(g, n, 14, 15),
    "Acid": lambda g, n: aplicar_variacao_hp(g, n, 5, 10),
    "Poison": lambda g, n: aplicar_variacao_hp(g, n, 15, 20),
    "Strong Acid": lambda g, n: aplicar_variacao_hp(g, n, 11, 15),
    "Divine Acid": lambda g, n: aplicar_variacao_hp(g, n, 20, 35),
    "Internal Hemorrhage": lambda g, n: aplicar_variacao_hp(g, n, 15, 25),
    "Allergic": lambda g, n: aplicar_variacao_hp(g, n, 7, 12),
    "Frustrated": lambda g, n: aplicar_variacao_hp(g, n, 14, 17),
    "Dense Plasma": lambda g, n: aplicar_variacao_hp(g, n, 10, 25),
    "Supreme Cremation": lambda g, n: aplicar_variacao_hp(g, n, 35, 43),
    "Curse": lambda g, n: aplicar_variacao_hp(g, n, 10, 20),
    "Plasma": lambda g, n: aplicar_variacao_hp(g, n, 1, 15),
    "Divine Plasma": lambda g, n: aplicar_variacao_hp(g, n, 10, 35),
    "Micro Robots": lambda g, n: aplicar_variacao_hp(g, n, 10, 15),
    "Shock": lambda g, n: aplicar_variacao_hp(g, n, 6, 15),
    "Strong Shock": lambda g, n: aplicar_variacao_hp(g, n, 15, 25),
    "Sandstorm": lambda g, n: aplicar_variacao_hp(g, n, 12, 17),
    "Golem": lambda g, n: aplicar_variacao_hp(g, n, 20, 22),
    "Radiation": lambda g, n: aplicar_variacao_hp(g, n, 4, 8),
    "Strong Radiation": lambda g, n: aplicar_variacao_hp(g, n, 10, 14),
    "Oxygen Suction": lambda g, n: aplicar_variacao_hp(g, n, 10, 20),
    "Battalion": lambda g, n: aplicar_variacao_hp(g, n, 40, 50),
    "Persecution": lambda g, n: aplicar_variacao_hp(g, n, 10, 20),
    "Necrosis": lambda g, n: aplicar_variacao_hp(g, n, 15, 20),
    "Ink": lambda g, n: aplicar_variacao_hp(g, n, 22, 27),
    "Black Ink": lambda g, n: aplicar_variacao_hp(g, n, 25, 35),
    "Death": lambda g, n: aplicar_variacao_hp(g, n, 70, 85),
    "Gravitational Attraction": lambda g, n: aplicar_variacao_hp(g, n, 1, 30),
    "Solar Cremation": lambda g, n: aplicar_variacao_hp(g, n, 55, 70),
    "Gravitational Field": lambda g, n: aplicar_variacao_hp(g, n, 15, 23),
    "Cold Moonlight": lambda g, n: aplicar_variacao_hp(g, n, 12, 20),
    "Possession": lambda g, n: aplicar_variacao_hp(g, n, 20, 35),
    "Eternal Eclipse": lambda g, n: aplicar_variacao_hp(g, n, 60, 90),
    "Degeneration": lambda g, n: aplicar_variacao_hp(g, n, 10, 15),
    "Zombie Attack": lambda g, n: aplicar_variacao_hp(g, n, 18, 30),
    "Powerful Degeneration": lambda g, n: aplicar_variacao_hp(g, n, 20, 35),
    "Covered By Ink": lambda g, n: aplicar_variacao_hp(g, n, 10, 15),
    "Exploding": lambda g, n: aplicar_variacao_hp(g, n, 5, 30),
    "Hypnotized": lambda g, n: aplicar_variacao_hp(g, n, 70, 120),
    "Disease": lambda g, n: aplicar_variacao_hp(g, n, 10, 15),
    "Dissolving": lambda g, n: aplicar_variacao_hp(g, n, 10, 20),
    "Infinite Mirage": lambda g, n: aplicar_variacao_hp(g, n, 40, 50),
    "Hypnotized Music": lambda g, n: aplicar_variacao_hp(g, n, 9, 12),
    "Sonic Explosion": lambda g, n: aplicar_variacao_hp(g, n, 30, 40),
    "Final Melody": lambda g, n: aplicar_variacao_hp(g, n, 45, 75),
    "Stellar Ruin Howl": lambda g, n: aplicar_variacao_hp(g, n, 50, 60),
    "Cresset": lambda g, n: aplicar_variacao_hp(g, n, 50, 70),
    "Phoenix Fire": lambda g, n: aplicar_variacao_hp(g, n, 110, 130),
    "Fading Existence": lambda g, n: aplicar_variacao_hp(g, n, 5, 10),
    "Fire": lambda g, n: aplicar_variacao_hp(g, n, 7, 12),
    "White Fire": lambda g, n: aplicar_variacao_hp(g, n, 20, 40),
    "Pure Flame": lambda g, n: aplicar_variacao_hp(g, n, 30, 45),
    "Purifying Touch": lambda g, n: aplicar_variacao_hp(g, n, 60, 75),
    "Ancestral Purity": lambda g, n: aplicar_variacao_hp(g, n, 160, 200),
    "Eternal Blessing": lambda g, n: aplicar_variacao_hp(g, n, 45, 55),
    "Illuminated Destiny": lambda g, n: aplicar_variacao_hp(g, n, 55, 75),
    "Divine Trial": lambda g, n: aplicar_variacao_hp(g, n, 45, 65),
    "Infernal Bite": lambda g, n: aplicar_variacao_hp(g, n, 60, 80),
    "Silent Tide": lambda g, n: aplicar_variacao_hp(g, n, 30, 50),
    "Cthulhu Bite": lambda g, n: aplicar_variacao_hp(g, n, 80, 120),
    "Cthulhu Fury": lambda g, n: aplicar_variacao_hp(g, n, 150, 320),
    "Orbital Bleeding": lambda g, n: aplicar_variacao_hp(g, n, 10, 15),
    "Keyblade Bleeding": lambda g, n: aplicar_variacao_hp(g, n, 12, 25),
    "Sonic Rush": lambda g, n: aplicar_variacao_hp(g, n, 100, 150),
    
    # Negative HoTs (Curas negativas operam como DoTs)
    "Depression": lambda g, n: aplicar_variacao_hp(g, n, 10, 15),
    "Strong Depression": lambda g, n: aplicar_variacao_hp(g, n, 30, 45),
    "Menstruation": lambda g, n: aplicar_variacao_hp(g, n, 40, 55),
    "Knife": lambda g, n: aplicar_variacao_hp(g, n, 30, 30),
    "Cursed Blessing": lambda g, n: aplicar_variacao_hp(g, n, 15, 15),

    # Heal Over Time (HoTs)
    "Healing": lambda g, n: aplicar_variacao_hp(g, n, 5, 10, True),
    "Powerful Healing": lambda g, n: aplicar_variacao_hp(g, n, 10, 20, True),
    "Refilling": lambda g, n: aplicar_variacao_hp(g, n, 5, 10, True),
    "Brazilian Way": lambda g, n: aplicar_variacao_hp(g, n, 15, 25, True),
    "Gluing Pieces": lambda g, n: aplicar_variacao_hp(g, n, 10, 15, True),
    "Mummify": lambda g, n: aplicar_variacao_hp(g, n, 8, 15, True),
    "Divine Healing": lambda g, n: aplicar_variacao_hp(g, n, 15, 25, True),
    "Full Heal": lambda g, n: aplicar_variacao_hp(g, n, 80, 100, True),
    "Crystallizing": lambda g, n: aplicar_variacao_hp(g, n, 17, 25, True),
    "Infinite Healing": lambda g, n: aplicar_variacao_hp(g, n, 160, 320, True),
    "Redrawing": lambda g, n: aplicar_variacao_hp(g, n, 15, 25, True),
    "Starring": lambda g, n: aplicar_variacao_hp(g, n, 50, 80, True),
    "Warrior Dragon Aura": lambda g, n: aplicar_variacao_hp(g, n, 37, 50, True),
    "Going Back in Time": lambda g, n: aplicar_variacao_hp(g, n, 95, 135, True),
    "Regenerate Mass 1": lambda g, n: aplicar_variacao_hp(g, n, 5, 10, True),
    "Regenerate Mass 2": lambda g, n: aplicar_variacao_hp(g, n, 15, 25, True),
    "Regenerate Mass 3": lambda g, n: aplicar_variacao_hp(g, n, 90, 125, True),
    "Celestial Light": lambda g, n: aplicar_variacao_hp(g, n, 45, 50, True),
    "Immaculate Aura": lambda g, n: aplicar_variacao_hp(g, n, 50, 65, True),
    "Paradise Blessing": lambda g, n: aplicar_variacao_hp(g, n, 70, 90, True),
    "Veil of Sanctity": lambda g, n: aplicar_variacao_hp(g, n, 85, 135, True),
    "Heavenly Healing": lambda g, n: aplicar_variacao_hp(g, n, 260, 330, True),
    "Guardian Heal": lambda g, n: aplicar_variacao_hp(g, n, 80, 200, True),
    "Ascension to Heaven": lambda g, n: aplicar_variacao_hp(g, n, 40, 45, True),
    "Salvation Aura": lambda g, n: aplicar_variacao_hp(g, n, 100, 165, True),
    "Cthulhu Regeneration": lambda g, n: aplicar_variacao_hp(g, n, 60, 100, True),
    "Cthulhu Dream": lambda g, n: aplicar_variacao_hp(g, n, 120, 200, True),
    "Dagon": lambda g, n: aplicar_variacao_hp(g, n, 185, 300, True),
    "Cthulhu Ascension": lambda g, n: aplicar_variacao_hp(g, n, 250, 450, True),
    "Healing Surge": lambda g, n: aplicar_variacao_hp(g, n, 150, 350, True),

    # Stuns (Imobilizações)
    "Stun": aplicar_imobilizacao,
    "Confusion": aplicar_imobilizacao,
    "Lack of Resources": aplicar_imobilizacao,
    "Double Stun": aplicar_imobilizacao
}

EFEITOS_DANO_RECEBIDO = {
    # Reduções de Dano (Mitigações / Escudos)
    "Shield": lambda d: modificar_dano(d, -50),
    "Iron Box": lambda d: modificar_dano(d, -20),
    "Iron Maiden": lambda d: modificar_dano(d, -20),
    "Divine Shield": lambda d: modificar_dano(d, -70),
    "Protected": lambda d: modificar_dano(d, -20),
    "More Resistant": lambda d: modificar_dano(d, -40),
    "Turn Into Air": lambda d: modificar_dano(d, -100),
    "Rigorously Bandaged": lambda d: modificar_dano(d, -20),
    "Kevlar Wrapped": lambda d: modificar_dano(d, -50),
    "Empowered Slime": lambda d: modificar_dano(d, -30),
    "Censored": lambda d: modificar_dano(d, -70),
    "Hiding": lambda d: modificar_dano(d, -100),
    "Corpse Protection": lambda d: modificar_dano(d, -50),
    "Barrier": lambda d: modificar_dano(d, -100),
    "Supreme Barrier": lambda d: modificar_dano(d, -100),
    "Going to the Future": lambda d: modificar_dano(d, -100),
    "Erase Attacks": lambda d: modificar_dano(d, -50),
    "Cancel Attacks": lambda d: modificar_dano(d, -100),
    "Guardian Shield": lambda d: modificar_dano(d, -75),
    "Supreme Guardian Shield": lambda d: modificar_dano(d, -120),
    "Divine Guardian Shield": lambda d: modificar_dano(d, -200),
    "Reflection": lambda d: modificar_dano(d, -100), # Bloqueia o dano atual

    # Aumento de Dano (Fragilidade)
    "Fragility": lambda d: modificar_dano(d, 90),
    "Frightened": lambda d: modificar_dano(d, 35),
    "Haunted": lambda d: modificar_dano(d, 55),
    "Malnutrition": lambda d: modificar_dano(d, 15),
    "Transcend": lambda d: modificar_dano(d, 170),
    "Aging": lambda d: modificar_dano(d, 240),
    "Fragile Existence 1": lambda d: modificar_dano(d, 35),
    "Fragile Existence 2": lambda d: modificar_dano(d, 200),
    "Berserker Fragility": lambda d: modificar_dano(d, 300),
    "Glass Mantle": lambda d: modificar_dano(d, 50),
    "Critical Exposure": lambda d: modificar_dano(d, 75),
    "Imminent Impact": lambda d: modificar_dano(d, 150)
}