import random
from data.galos_db import GALOS_DB
from logic.efeitos import EFEITOS_INICIO_TURNO, EFEITOS_DANO_RECEBIDO # Importação do motor de efeitos

class Galo:
    def __init__(self, nome, hp_max, caminho_imagem, nivel=1, xp=0, tipo="Normal", skills_equipadas=None, efeitos=None): 
        self.nome = nome
        self.tipo = tipo
        self.nivel = nivel
        self.xp = xp
        self.hp_max = hp_max
        self.hp_atual = hp_max
        self.caminho_imagem = caminho_imagem
        self.skills_equipadas = skills_equipadas if skills_equipadas is not None else [] 
        self.efeitos = efeitos if efeitos is not None else {} 

    def obter_skills_desbloqueadas(self):
        if self.nome not in GALOS_DB:
            return []
        skills_db = GALOS_DB[self.nome]["skills"]
        desbloqueadas = []
        for lvl, skill in skills_db.items():
            if lvl <= self.nivel:
                desbloqueadas.append((lvl, skill))
        return desbloqueadas

    def equipar_skills_bot(self):
        desbloqueadas = self.obter_skills_desbloqueadas()
        desbloqueadas.sort(key=lambda x: x[0], reverse=True)
        self.skills_equipadas = [skill for lvl, skill in desbloqueadas[:5]]
        while len(self.skills_equipadas) < 5:
            self.skills_equipadas.append(None)

    def atacar(self):
        skills_validas = [s for s in self.skills_equipadas if s is not None]
        if not skills_validas:
            self.equipar_skills_bot()
            skills_validas = [s for s in self.skills_equipadas if s is not None]
            
        if not skills_validas:
            return "Ataque Básico", 10, None

        skill = random.choice(skills_validas)
        dano_total = random.randint(skill["min"], skill["max"])
        
        dados_efeito = None
        if "efeito" in skill:
            dados_efeito = {
                "nome": skill["efeito"],
                "chance": skill.get("chance", 100),
                "turnos": skill.get("turnos", 1)
            }
            
        return skill["nome"], dano_total, dados_efeito

    def aplicar_efeito(self, dados_efeito):
        if not dados_efeito:
            return False
            
        if random.randint(1, 100) <= dados_efeito["chance"]:
            self.efeitos[dados_efeito["nome"]] = dados_efeito["turnos"]
            return True
            
        return False

    def processar_efeitos_inicio_turno(self):
        mensagens = []
        pode_atacar = True
        efeitos_para_remover = []

        for efeito, turnos in self.efeitos.items():
            if turnos > 0:
                if efeito in EFEITOS_INICIO_TURNO: # Delega o processamento da mecânica para o motor
                    msg, permite_atacar = EFEITOS_INICIO_TURNO[efeito](self, efeito)
                    if msg: mensagens.append(msg)
                    if not permite_atacar: pode_atacar = False

                self.efeitos[efeito] -= 1
                if self.efeitos[efeito] <= 0:
                    efeitos_para_remover.append(efeito)

        for efeito in efeitos_para_remover:
            del self.efeitos[efeito]

        if self.hp_atual < 0:
            self.hp_atual = 0

        return mensagens, pode_atacar

    def sofrer_dano(self, dano_recebido):
        dano_real = max(1, dano_recebido)
        efeitos_para_remover = []
        
        for efeito in list(self.efeitos.keys()): # Itera iterando cópia das chaves para processar mitigações reativas
            if efeito in EFEITOS_DANO_RECEBIDO and self.efeitos[efeito] > 0:
                dano_real = EFEITOS_DANO_RECEBIDO[efeito](dano_real)
                self.efeitos[efeito] -= 1
                if self.efeitos[efeito] <= 0:
                    efeitos_para_remover.append(efeito)
                    
        for efeito in efeitos_para_remover:
            del self.efeitos[efeito]

        self.hp_atual -= dano_real
        if self.hp_atual < 0:
            self.hp_atual = 0
        return dano_real

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        xp_necessario = 30 + (self.nivel - 1) * 60
        
        while self.xp >= xp_necessario:
            self.xp -= xp_necessario
            self.nivel += 1
            self.hp_max += 12
            self.hp_atual = self.hp_max
            xp_necessario = 30 + (self.nivel - 1) * 60

    def to_dict(self):
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "hp_max": self.hp_max,
            "caminho_imagem": self.caminho_imagem,
            "nivel": self.nivel,
            "xp": self.xp,
            "skills_equipadas": self.skills_equipadas,
            "efeitos": self.efeitos
        }

    @classmethod
    def from_dict(cls, data):
        skills_equipadas = data.get("skills_equipadas", [])
        while len(skills_equipadas) < 5:
            skills_equipadas.append(None)
            
        return cls(
            data["nome"], 
            data["hp_max"], 
            data["caminho_imagem"], 
            data.get("nivel", 1), 
            data.get("xp", 0),
            data.get("tipo", "Normal"),
            skills_equipadas,
            data.get("efeitos", {})
        )