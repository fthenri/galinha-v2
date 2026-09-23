import { GALOS_DB } from '../data/galosDb';
import { Galo } from './Galo';
import { useJogadorStore } from '../store/jogadorStore';
import type { ItemLoja } from '../store/jogadorStore';

export const PRECOS_LOJA = {
    Common: { moeda: "moedas" as const, valor: 500 },
    Rare: { moeda: "moedas" as const, valor: 2000 },
    Epic: { moeda: "moedas" as const, valor: 5000 },
    Legendary: { moeda: "galo_coins" as const, valor: 4 },
    Mythic: { moeda: "galo_coins" as const, valor: 50 },
    Divine: { moeda: "galo_coins" as const, valor: 250 }
};

export function obterGalosPorRaridade(): Record<string, string[]> {
    const raridades: Record<string, string[]> = {
        Common: [], Rare: [], Epic: [], Legendary: [], Mythic: [], Divine: []
    };
    
    for (const [nome, dados] of Object.entries(GALOS_DB)) {
        const raridade = dados.raridade || "Common";
        if (raridades[raridade]) {
            raridades[raridade].push(nome);
        }
    }
    return raridades;
}

export function atualizarLojaDiaria(): void {
    const state = useJogadorStore.getState();
    const agora = Date.now() / 1000; // Tempo em segundos (similar ao time.time() do Python)

    if (agora >= state.lojaAtualizacao) {
        const galosPorRaridade = obterGalosPorRaridade();
        
        // Simulação do Array dinâmico de pesos do Python
        const opcoesRaridade: string[] = [
            ...Array(50).fill("Common"),
            ...Array(30).fill("Rare"),
            ...Array(12).fill("Epic"),
            ...Array(5).fill("Legendary"),
            ...Array(2).fill("Mythic"),
            ...Array(1).fill("Divine")
        ];

        const novaLoja: ItemLoja[] = [];

        for (let i = 0; i < 5; i++) {
            let raridade = opcoesRaridade[Math.floor(Math.random() * opcoesRaridade.length)];
            if (!galosPorRaridade[raridade] || galosPorRaridade[raridade].length === 0) {
                raridade = "Common";
            }
            
            const nomeGalo = galosPorRaridade[raridade][Math.floor(Math.random() * galosPorRaridade[raridade].length)];
            
            novaLoja.push({
                nome: nomeGalo,
                comprado: false,
                moeda: PRECOS_LOJA[raridade as keyof typeof PRECOS_LOJA].moeda,
                valor: PRECOS_LOJA[raridade as keyof typeof PRECOS_LOJA].valor,
                raridade: raridade
            });
        }
        
        const proximaAtualizacao = agora + (6 * 3600);
        state.atualizarLoja(novaLoja, proximaAtualizacao);
    }
}

export function abrirLootbox(tipo: "Bronze" | "Gold" | "Emerald"): Galo {
    const state = useJogadorStore.getState();
    const galosPorRaridade = obterGalosPorRaridade();
    let raridade = "Common";

    if (tipo === "Bronze") {
        state.incrementarPity("Bronze");
        const currentPity = useJogadorStore.getState().pityBronze;
        if (currentPity >= 15) {
            raridade = "Epic";
            state.resetarPity("Bronze");
        } else {
            const roll = Math.random() * 100;
            if (roll <= 0.1) raridade = "Legendary";
            else if (roll <= 5.0) raridade = "Epic";
            else if (roll <= 30.0) raridade = "Rare";
            else raridade = "Common";
        }
    } else if (tipo === "Gold") {
        state.incrementarPity("Gold");
        const currentPity = useJogadorStore.getState().pityGold;
        if (currentPity >= 30) {
            raridade = "Legendary";
            state.resetarPity("Gold");
        } else {
            const roll = Math.random() * 100;
            if (roll <= 0.02) raridade = "Mythic";
            else if (roll <= 2.92) raridade = "Legendary";
            else raridade = "Epic";
        }
    } else if (tipo === "Emerald") {
        state.incrementarPity("Emerald");
        const currentPity = useJogadorStore.getState().pityEmerald;
        if (currentPity >= 50) {
            raridade = "Mythic";
            state.resetarPity("Emerald");
        } else {
            const roll = Math.random() * 100;
            if (roll <= 1.5) raridade = "Mythic";
            else raridade = "Legendary";
        }
    }

    if (["Epic", "Legendary", "Mythic", "Divine"].includes(raridade) && tipo === "Bronze") {
        state.resetarPity("Bronze");
    }
    if (["Legendary", "Mythic", "Divine"].includes(raridade) && tipo === "Gold") {
        state.resetarPity("Gold");
    }
    if (["Mythic", "Divine"].includes(raridade) && tipo === "Emerald") {
        state.resetarPity("Emerald");
    }

    const nomeGalo = galosPorRaridade[raridade][Math.floor(Math.random() * galosPorRaridade[raridade].length)];
    const dadosGalo = GALOS_DB[nomeGalo];
    const novoGalo = new Galo(nomeGalo, dadosGalo.hp_base, dadosGalo.caminho_imagem, 1, 0, dadosGalo.tipo);
    
    useJogadorStore.getState().adicionarGalo(novoGalo);
    
    return novoGalo;
}

export function comprarItemLoja(index: number): boolean {
    const state = useJogadorStore.getState();
    const item = state.lojaDiaria[index];
    
    if (!item || item.comprado) return false;
    
    const podeComprar = state.gastarMoeda(item.valor, item.moeda);
    if (podeComprar) {
        state.comprarItemLoja(index);
        const dadosGalo = GALOS_DB[item.nome];
        const novoGalo = new Galo(item.nome, dadosGalo.hp_base, dadosGalo.caminho_imagem, 1, 0, dadosGalo.tipo);
        state.adicionarGalo(novoGalo);
        return true;
    }
    
    return false;
}
