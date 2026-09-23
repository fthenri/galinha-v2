import { calcularMultiplicadorRebirth } from '../store/jogadorStore';
import { GALOS_DB } from '../data/galosDb';
import type { Skill } from '../data/galosDb';
import { EFEITOS_INICIO_TURNO, EFEITOS_DANO_RECEBIDO } from './efeitos';
import { SISTEMA_TIPOS } from '../data/tiposDb';

export type DadosEfeito = {
    nome: string;
    chance: number;
    turnos: number;
};

export class Galo {
    nome: string;
    tipo: string;
    nivel: number;
    xp: number;
    hp_max: number;
    hp_atual: number;
    caminho_imagem: string;
    skills_equipadas: (Skill | null)[];
    rebirths: number;
    efeitos: Record<string, number>;

    constructor(
        nome: string,
        hp_max: number,
        caminho_imagem: string,
        nivel: number = 1,
        xp: number = 0,
        tipo: string = "Normal",
        skills_equipadas: (Skill | null)[] | null = null,
        efeitos: Record<string, number> | null = null,
        rebirths: number = 0
    ) {
        this.nome = nome;
        this.tipo = tipo;
        this.nivel = nivel;
        this.xp = xp;
        this.hp_max = hp_max;
        this.hp_atual = hp_max;
        this.caminho_imagem = caminho_imagem;
        this.skills_equipadas = skills_equipadas ?? [];
        this.efeitos = efeitos ?? {};
        this.rebirths = rebirths;
    }

    obterSkillsDesbloqueadas(): { level: number, skill: Skill }[] {
        if (!GALOS_DB[this.nome]) {
            return [];
        }
        
        const skillsDb = GALOS_DB[this.nome].skills;
        const desbloqueadas: { level: number, skill: Skill }[] = [];
        
        // Em TypeScript, a conversão da chave do objeto para número é necessária para manter a lógica original.
        for (const [lvlStr, skill] of Object.entries(skillsDb)) {
            const lvl = parseInt(lvlStr, 10);
            if (lvl <= this.nivel) {
                desbloqueadas.push({ level: lvl, skill });
            }
        }
        
        return desbloqueadas;
    }

    equiparSkillsBot(): void {
        const desbloqueadas = this.obterSkillsDesbloqueadas();
        desbloqueadas.sort((a, b) => b.level - a.level);
        
        this.skills_equipadas = desbloqueadas.slice(0, 5).map(item => item.skill);
        while (this.skills_equipadas.length < 5) {
            this.skills_equipadas.push(null);
        }
    }

    atacar(): [string, number, DadosEfeito | null] {
        let skillsValidas = this.skills_equipadas.filter(s => s !== null) as Skill[];
        
        if (skillsValidas.length === 0) {
            this.equiparSkillsBot();
            skillsValidas = this.skills_equipadas.filter(s => s !== null) as Skill[];
        }
        
        if (skillsValidas.length === 0) {
            return ["Ataque Básico", 10, null];
        }

        const skill = skillsValidas[Math.floor(Math.random() * skillsValidas.length)];
        const danoTotal = Math.floor(Math.random() * (skill.max - skill.min + 1)) + skill.min;
        
        let dadosEfeito: DadosEfeito | null = null;
        if (skill.efeito) {
            dadosEfeito = {
                nome: skill.efeito,
                chance: skill.chance ?? 100,
                turnos: skill.turnos ?? 1
            };
        }
        
        return [skill.nome, danoTotal, dadosEfeito];
    }

    aplicarEfeito(dadosEfeito: DadosEfeito | null): boolean {
        if (!dadosEfeito) return false;
        
        const roll = Math.floor(Math.random() * 100) + 1;
        if (roll <= dadosEfeito.chance) {
            this.efeitos[dadosEfeito.nome] = dadosEfeito.turnos;
            return true;
        }
        
        return false;
    }

    processarEfeitosInicioTurno(): [string[], boolean] {
        const mensagens: string[] = [];
        let podeAtacar = true;
        const efeitosParaRemover: string[] = [];

        for (const [efeito, turnos] of Object.entries(this.efeitos)) {
            if (turnos > 0) {
                if (EFEITOS_INICIO_TURNO[efeito]) {
                    const [msg, permiteAtacar] = EFEITOS_INICIO_TURNO[efeito](this, efeito);
                    if (msg) mensagens.push(msg);
                    if (!permiteAtacar) podeAtacar = false;
                }

                this.efeitos[efeito] -= 1;
                if (this.efeitos[efeito] <= 0) {
                    efeitosParaRemover.push(efeito);
                }
            }
        }

        for (const efeito of efeitosParaRemover) {
            delete this.efeitos[efeito];
        }

        if (this.hp_atual < 0) {
            this.hp_atual = 0;
        }

        return [mensagens, podeAtacar];
    }

    sofrerDano(danoRecebido: number, tipoAtacante?: string): number {
        let danoReal = Math.max(1, danoRecebido);

        if (tipoAtacante && SISTEMA_TIPOS[tipoAtacante]) {
            const relacao = SISTEMA_TIPOS[tipoAtacante];
            if (relacao.vantagem.includes(this.tipo)) {
                danoReal = Math.round(danoReal * 1.15);
            } else if (relacao.desvantagem.includes(this.tipo)) {
                danoReal = Math.round(danoReal * 0.90);
            }
        }

        const efeitosParaRemover: string[] = [];
        
        // No TypeScript criamos um array de chaves para evitar problemas de mutação durante a iteração
        const chavesEfeitos = Object.keys(this.efeitos);
        for (const efeito of chavesEfeitos) {
            if (EFEITOS_DANO_RECEBIDO[efeito] && this.efeitos[efeito] > 0) {
                danoReal = EFEITOS_DANO_RECEBIDO[efeito](danoReal);
                this.efeitos[efeito] -= 1;
                if (this.efeitos[efeito] <= 0) {
                    efeitosParaRemover.push(efeito);
                }
            }
        }

        for (const efeito of efeitosParaRemover) {
            delete this.efeitos[efeito];
        }

        this.hp_atual -= danoReal;
        if (this.hp_atual < 0) {
            this.hp_atual = 0;
        }
        
        return danoReal;
    }

    ganharXp(quantidade: number): void {
        this.xp += quantidade;
        let xpNecessario = 30 + (this.nivel - 1) * 60;
        
        while (this.xp >= xpNecessario) {
            this.xp -= xpNecessario;
            this.nivel += 1;
            this.hp_max += Math.floor(12 * calcularMultiplicadorRebirth(this.rebirths));
            this.hp_atual = this.hp_max;
            
            if (GALOS_DB[this.nome]) {
                const skillsNoNovoNivel = [];
                for (const [lvlStr, skill] of Object.entries(GALOS_DB[this.nome].skills)) {
                    if (parseInt(lvlStr, 10) === this.nivel) {
                        skillsNoNovoNivel.push(skill);
                    }
                }
                
                if (skillsNoNovoNivel.length > 0) {
                    this.skills_equipadas = [...skillsNoNovoNivel, ...this.skills_equipadas];
                    this.skills_equipadas = this.skills_equipadas.slice(0, 5);
                }
            }
            
            while (this.skills_equipadas.length < 5) {
                this.skills_equipadas.push(null);
            }

            xpNecessario = 30 + (this.nivel - 1) * 60;
        }
    }

    toDict(): any {
        return {
            nome: this.nome,
            tipo: this.tipo,
            hp_max: this.hp_max,
            caminho_imagem: this.caminho_imagem,
            nivel: this.nivel,
            xp: this.xp,
            skills_equipadas: this.skills_equipadas,
            efeitos: this.efeitos,
            rebirths: this.rebirths
        };
    }

    static fromDict(data: any): Galo {
        const skills_equipadas = Array.isArray(data.skills_equipadas) ? [...data.skills_equipadas] : [];
        while (skills_equipadas.length < 5) {
            skills_equipadas.push(null);
        }
        
        return new Galo(
            data.nome,
            data.hp_max,
            data.caminho_imagem,
            data.nivel ?? 1,
            data.xp ?? 0,
            data.tipo ?? "Normal",
            skills_equipadas,
            data.efeitos ? { ...data.efeitos } : {},
            data.rebirths ?? 0
        );
    }
}

