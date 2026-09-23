import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Galo } from '../logic/Galo';
import { GALOS_DB } from '../data/galosDb';

export interface ItemLoja {
    nome: string;
    comprado: boolean;
    moeda: "moedas" | "galo_coins";
    valor: number;
    raridade: string;
}

export const calcularNivelRebirth = (rebirths: number = 0) => Math.floor(34 + (rebirths * 1.55));
export const calcularMultiplicadorRebirth = (rebirths: number = 0) => 1 + (0.15 * rebirths);

export const calcularValorVenda = (galo: Galo): { valor: number, moeda: "moedas" | "galo_coins" } => {
    const raridade = GALOS_DB[galo.nome]?.raridade || "Common";
    let base = 0;
    let mult = 0;
    let tipoMoeda: "moedas" | "galo_coins" = "moedas";

    if (raridade === "Common") { base = 30; mult = 6; tipoMoeda = "moedas"; }
    else if (raridade === "Rare") { base = 120; mult = 25; tipoMoeda = "moedas"; }
    else if (raridade === "Epic") { base = 300; mult = 60; tipoMoeda = "moedas"; }
    else if (raridade === "Legendary") { base = 1000; mult = 200; tipoMoeda = "moedas"; }
    else if (raridade === "Special" || raridade === "Mythic") { base = 10; mult = 2; tipoMoeda = "galo_coins"; }
    else if (raridade === "Divine") { base = 50; mult = 5; tipoMoeda = "galo_coins"; }

    return {
        valor: Math.floor(base + ((galo.nivel - 1) * mult)),
        moeda: tipoMoeda
    };
};

export interface JogadorState {
    nome: string;
    moedas: number;
    galoCoins: number;
    velRinha: string;
    difRinha: string;
    autoRevive: boolean;
    galos: Galo[];
    galoAtivoIndex: number;
    
    lojaDiaria: ItemLoja[];
    lojaAtualizacao: number;
    pityBronze: number;
    pityGold: number;
    pityEmerald: number;

    adicionarGalo: (galo: Galo) => void;
    setGaloAtivo: (index: number) => void;
    atualizarLoja: (loja: ItemLoja[], atualizacao: number) => void;
    comprarItemLoja: (index: number) => void;
    gastarMoeda: (valor: number, tipo: "moedas" | "galo_coins") => boolean;
    incrementarPity: (tipo: "Bronze" | "Gold" | "Emerald") => void;
    resetarPity: (tipo: "Bronze" | "Gold" | "Emerald") => void;
    alterarSkillSlot: (galoIndex: number, slotIndex: number, novaSkillNome: string | null) => void;
    venderGalo: (galoIndex: number) => void;
    setAutoRevive: (valor: boolean) => void;
    darRebirth: (galoIndex: number) => void;
}

// O middleware persist salva o estado automaticamente no localStorage.
// O merge é utilizado para garantir que os objetos puros de galos (do JSON)
// sejam instanciados novamente como a classe Galo, mantendo seus métodos ativos.
export const useJogadorStore = create<JogadorState>()(
    persist(
        (set, get) => ({
            nome: "Jogador",
            moedas: 500,
            galoCoins: 0,
            velRinha: "1.0",
            difRinha: "Facil",
            autoRevive: false,
            galos: [new Galo("Rooster Normal", 100, "assets/galos/00_2.png", 1, 0, "Basic")],
            galoAtivoIndex: 0,
            
            lojaDiaria: [],
            lojaAtualizacao: 0,
            pityBronze: 0,
            pityGold: 0,
            pityEmerald: 0,

            adicionarGalo: (galo) => set((state) => {
                const novosGalos = [...state.galos, galo];
                return {
                    galos: novosGalos,
                    galoAtivoIndex: state.galoAtivoIndex === -1 ? 0 : state.galoAtivoIndex
                };
            }),

            setGaloAtivo: (index) => set({ galoAtivoIndex: index }),

            atualizarLoja: (loja, atualizacao) => set({ lojaDiaria: loja, lojaAtualizacao: atualizacao }),

            comprarItemLoja: (index) => set((state) => {
                const novaLoja = [...state.lojaDiaria];
                novaLoja[index] = { ...novaLoja[index], comprado: true };
                return { lojaDiaria: novaLoja };
            }),

            gastarMoeda: (valor, tipo) => {
                const state = get();
                if (tipo === "moedas" && state.moedas >= valor) {
                    set({ moedas: state.moedas - valor });
                    return true;
                } else if (tipo === "galo_coins" && state.galoCoins >= valor) {
                    set({ galoCoins: state.galoCoins - valor });
                    return true;
                }
                return false;
            },

            incrementarPity: (tipo) => set((state) => {
                if (tipo === "Bronze") return { pityBronze: state.pityBronze + 1 };
                if (tipo === "Gold") return { pityGold: state.pityGold + 1 };
                if (tipo === "Emerald") return { pityEmerald: state.pityEmerald + 1 };
                return {};
            }),

            resetarPity: (tipo) => set(() => {
                if (tipo === "Bronze") return { pityBronze: 0 };
                if (tipo === "Gold") return { pityGold: 0 };
                if (tipo === "Emerald") return { pityEmerald: 0 };
                return {};
            }),

            alterarSkillSlot: (galoIndex, slotIndex, novaSkillNome) => set((state) => {
                const novosGalos = [...state.galos];
                const galo = novosGalos[galoIndex];
                if (!galo) return state;
                
                let skillObj = null;
                if (novaSkillNome) {
                    const desbloqueadas = galo.obterSkillsDesbloqueadas();
                    const found = desbloqueadas.find(d => d.skill.nome === novaSkillNome);
                    if (found) skillObj = found.skill;
                }
                
                galo.skills_equipadas[slotIndex] = skillObj;
                return { galos: novosGalos };
            }),

            venderGalo: (galoIndex) => set((state) => {
                if (state.galos.length <= 1) return state;
                if (galoIndex === state.galoAtivoIndex) return state;

                const galo = state.galos[galoIndex];
                if (!galo) return state;

                const calc = calcularValorVenda(galo);
                const valor = calc.valor;
                const tipoMoeda = calc.moeda === 'galo_coins' ? 'galoCoins' : 'moedas';

                const novosGalos = [...state.galos];
                novosGalos.splice(galoIndex, 1);

                let novoAtivoIndex = state.galoAtivoIndex;
                if (galoIndex < state.galoAtivoIndex) {
                    novoAtivoIndex -= 1;
                }

                return {
                    galos: novosGalos,
                    galoAtivoIndex: novoAtivoIndex,
                    [tipoMoeda]: state[tipoMoeda] + valor
                };
            }),
            setAutoRevive: (valor) => set({ autoRevive: valor })
        }),
        {
            name: 'jogador-storage',
            merge: (persistedState: any, currentState) => {
                const state = { ...currentState, ...(persistedState || {}) };
                if (persistedState?.galos) {
                    state.galos = persistedState.galos.map((g: any) => Galo.fromDict(g));
                }
                
                if (state.galos.length === 0) {
                    const defaultGalo = new Galo("Rooster Normal", 100, "assets/galos/00_2.png", 1, 0, "Basic");
                    state.galos.push(defaultGalo);
                    state.galoAtivoIndex = 0;
                }
                
                return state;
            }
        }
    )
);
