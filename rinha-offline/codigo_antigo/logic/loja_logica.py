import random
import time
from data.galos_db import GALOS_DB
from logic.galo import Galo

PRECOS_LOJA = {
    "Common": {"moeda": "moedas", "valor": 500},
    "Rare": {"moeda": "moedas", "valor": 2000},
    "Epic": {"moeda": "moedas", "valor": 5000},
    "Legendary": {"moeda": "galo_coins", "valor": 4},
    "Mythic": {"moeda": "galo_coins", "valor": 50},
    "Divine": {"moeda": "galo_coins", "valor": 250}
}

def obter_galos_por_raridade():
    raridades = {"Common": [], "Rare": [], "Epic": [], "Legendary": [], "Mythic": [], "Divine": []}
    for nome, dados in GALOS_DB.items():
        raridade = dados.get("raridade", "Common")
        if raridade in raridades:
            raridades[raridade].append(nome)
    return raridades

def atualizar_loja_diaria(jogador):
    agora = time.time()
    if agora >= jogador.loja_atualizacao:
        jogador.loja_diaria = []
        galos_por_raridade = obter_galos_por_raridade()
        
        opcoes_raridade = ["Common"] * 50 + ["Rare"] * 30 + ["Epic"] * 12 + ["Legendary"] * 5 + ["Mythic"] * 2 + ["Divine"] * 1
        
        for _ in range(5):
            raridade = random.choice(opcoes_raridade)
            if not galos_por_raridade[raridade]:
                raridade = "Common"
            nome_galo = random.choice(galos_por_raridade[raridade])
            jogador.loja_diaria.append({
                "nome": nome_galo,
                "comprado": False,
                "moeda": PRECOS_LOJA[raridade]["moeda"],
                "valor": PRECOS_LOJA[raridade]["valor"],
                "raridade": raridade
            })
        jogador.loja_atualizacao = agora + (6 * 3600)
        jogador.salvar()

def abrir_lootbox(jogador, tipo):
    galos_por_raridade = obter_galos_por_raridade()
    
    if tipo == "Bronze":
        jogador.pity_bronze += 1
        if jogador.pity_bronze >= 15:
            raridade = "Epic"
            jogador.pity_bronze = 0
        else:
            roll = random.uniform(0, 100)
            if roll <= 0.1: raridade = "Legendary"
            elif roll <= 5.0: raridade = "Epic"
            elif roll <= 30.0: raridade = "Rare"
            else: raridade = "Common"
            
    elif tipo == "Gold":
        jogador.pity_gold += 1
        if jogador.pity_gold >= 30:
            raridade = "Legendary"
            jogador.pity_gold = 0
        else:
            roll = random.uniform(0, 100)
            if roll <= 0.02: raridade = "Mythic"
            elif roll <= 2.92: raridade = "Legendary"
            else: raridade = "Epic"
            
    elif tipo == "Emerald":
        jogador.pity_emerald += 1
        if jogador.pity_emerald >= 50:
            raridade = "Mythic"
            jogador.pity_emerald = 0
        else:
            roll = random.uniform(0, 100)
            if roll <= 1.5: raridade = "Mythic"
            else: raridade = "Legendary"
            
    if raridade in ["Epic", "Legendary", "Mythic", "Divine"] and tipo == "Bronze":
        jogador.pity_bronze = 0
    if raridade in ["Legendary", "Mythic", "Divine"] and tipo == "Gold":
        jogador.pity_gold = 0
    if raridade in ["Mythic", "Divine"] and tipo == "Emerald":
        jogador.pity_emerald = 0

    nome_galo = random.choice(galos_por_raridade[raridade])
    novo_galo = Galo(nome_galo, GALOS_DB[nome_galo]["hp_base"], GALOS_DB[nome_galo]["caminho_imagem"])
    jogador.adicionar_galo(novo_galo)
    jogador.salvar()
    return novo_galo