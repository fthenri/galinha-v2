import json
import os
from logic.galo import Galo

class Jogador:
    def __init__(self, nome, moedas=500, vel_rinha="1.0", dif_rinha="Facil"):
        self.nome = nome
        self.moedas = moedas
        self.galo_coins = 0 # NOVA LINHA
        self.vel_rinha = vel_rinha
        self.dif_rinha = dif_rinha
        self.galos = []
        self.galo_ativo = None
        
        # NOVAS LINHAS (Sistema de Loja)
        self.loja_diaria = [] 
        self.loja_atualizacao = 0.0
        self.pity_bronze = 0
        self.pity_gold = 0
        self.pity_emerald = 0

    def adicionar_galo(self, galo):
        self.galos.append(galo)
        if self.galo_ativo is None:
            self.galo_ativo = galo

    def to_dict(self):
        return {
            "nome": self.nome,
            "moedas": self.moedas,
            "galo_coins": self.galo_coins, # NOVA LINHA
            "vel_rinha": self.vel_rinha,
            "dif_rinha": self.dif_rinha,
            "galos": [galo.to_dict() for galo in self.galos],
            "galo_ativo_index": self.galos.index(self.galo_ativo) if self.galo_ativo else -1,
            # NOVAS LINHAS
            "loja_diaria": self.loja_diaria,
            "loja_atualizacao": self.loja_atualizacao,
            "pity_bronze": self.pity_bronze,
            "pity_gold": self.pity_gold,
            "pity_emerald": self.pity_emerald
        }

    @classmethod
    def carregar(cls, arquivo="save.json"):
        if os.path.exists(arquivo):
            with open(arquivo, "r", encoding="utf-8") as f:
                data = json.load(f)
            jogador = cls(
                data["nome"], 
                data.get("moedas", 500),
                data.get("vel_rinha", "1.0"),
                data.get("dif_rinha", "Facil")
            )
            # NOVAS LINHAS RESGATANDO SAVES ANTIGOS
            jogador.galo_coins = data.get("galo_coins", 0)
            jogador.loja_diaria = data.get("loja_diaria", [])
            jogador.loja_atualizacao = data.get("loja_atualizacao", 0.0)
            jogador.pity_bronze = data.get("pity_bronze", 0)
            jogador.pity_gold = data.get("pity_gold", 0)
            jogador.pity_emerald = data.get("pity_emerald", 0)
            
            for galo_data in data.get("galos", []):
                jogador.adicionar_galo(Galo.from_dict(galo_data))
                
            idx = data.get("galo_ativo_index", -1)
            if idx >= 0 and idx < len(jogador.galos):
                jogador.galo_ativo = jogador.galos[idx]
                
            print(f"[DEBUG JOGADOR] Jogo carregado de {arquivo}. Galos carregados: {len(jogador.galos)}")
            return jogador
        return None

    def salvar(self, arquivo="save.json"):
        try:
            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, indent=4)
            print(f"[DEBUG JOGADOR] Jogo salvo em {arquivo} com sucesso!")
        except Exception as e:
            print(f"[DEBUG JOGADOR CRITICO] Falha ao salvar jogo em {arquivo}: {e}")