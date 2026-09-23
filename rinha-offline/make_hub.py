import codecs
import re

hub_code = """import { useState } from 'react';
import { useJogadorStore } from '../store/jogadorStore';
import ModoTreino from './ModoTreino';
import ModoTrial from './ModoTrial';

export default function Rinha() {
    const [modoAtivo, setModoAtivo] = useState<string | null>(null);
    const [modalInfo, setModalInfo] = useState<{titulo: string, texto: string} | null>(null);
    
    const meuGalo = useJogadorStore(s => s.galos[s.galoAtivoIndex]);

    if (!meuGalo) {
        return <div className="p-6 text-center text-red-500 font-bold">Equipe um galo no perfil primeiro!</div>;
    }

    const trialsAtual = useJogadorStore.getState().trialsPorClasse[meuGalo.nome] || 0;

    const handleModoClick = (modo: string) => {
        if (modo === 'Dungeon' || modo === 'Arena' || modo === 'Survival') {
            setModalInfo({
                titulo: 'Apenas um vislumbre...',
                texto: 'Os ventos sussurram sobre novos desafios se formando no horizonte. Esta área estará acessível em futuras atualizações.'
            });
        } else if (modo === 'Trial') {
            if (trialsAtual >= 20) {
                setModalInfo({
                    titulo: 'Maestria Alcançada',
                    texto: 'Você sobreviveu a todas as provações e dominou os segredos desta classe. Não há mais nada a aprender aqui.'
                });
            } else {
                setModoAtivo('trial');
            }
        } else if (modo === 'Treino') {
            setModoAtivo('treino');
        } else if (modo === 'Raid') {
            setModoAtivo('raid');
        }
    };

    if (modoAtivo === 'treino') {
        return (
            <div className="w-full flex flex-col items-center">
                <button onClick={() => setModoAtivo(null)} className="mb-4 bg-zinc-800 text-white font-bold py-2 px-4 rounded-lg hover:bg-zinc-700 w-full max-w-4xl mt-6 text-left">← Abandonar Batalha</button>
                <ModoTreino />
            </div>
        );
    }
    
    if (modoAtivo === 'trial') {
        return (
            <div className="w-full flex flex-col items-center">
                <button onClick={() => setModoAtivo(null)} className="mb-4 bg-zinc-800 text-white font-bold py-2 px-4 rounded-lg hover:bg-zinc-700 w-full max-w-4xl mt-6 text-left">← Abandonar Batalha</button>
                <ModoTrial />
            </div>
        );
    }

    if (modoAtivo === 'raid') {
        return (
            <div className="w-full flex flex-col items-center">
                <button onClick={() => setModoAtivo(null)} className="mb-4 bg-zinc-800 text-white font-bold py-2 px-4 rounded-lg hover:bg-zinc-700 w-full max-w-4xl mt-6 text-left">← Abandonar Batalha</button>
                <div className="text-center text-zinc-400 p-8">Raid em construção...</div>
            </div>
        );
    }

    return (
        <div className="p-6 flex flex-col items-center max-w-4xl mx-auto w-full">
            <h2 className="text-3xl font-bold mb-8 text-white">Hub de Batalhas</h2>
            
            <div className="flex flex-col gap-4 w-full max-w-md">
                {['Trial', 'Treino', 'Raid', 'Dungeon', 'Arena', 'Survival'].map((modo) => (
                    <button 
                        key={modo}
                        onClick={() => handleModoClick(modo)}
                        className="bg-zinc-800 border border-zinc-700 hover:border-zinc-500 text-white font-bold py-4 px-6 rounded-xl transition-all shadow-lg text-lg uppercase tracking-widest text-center w-full"
                    >
                        {modo}
                    </button>
                ))}
            </div>

            {modalInfo !== null && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
                    <div className="bg-zinc-900 border border-zinc-700 p-8 rounded-2xl w-full max-w-md shadow-2xl relative flex flex-col items-center text-center">
                        <h2 className="text-2xl font-black text-amber-500 mb-4">{modalInfo.titulo}</h2>
                        <p className="text-zinc-300 text-sm mb-8 leading-relaxed">{modalInfo.texto}</p>
                        <button 
                            onClick={() => setModalInfo(null)}
                            className="w-full bg-zinc-800 hover:bg-zinc-700 text-white font-bold py-3 px-4 rounded-xl transition-all"
                        >
                            Entendido
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
"""

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(hub_code)

print("Done Hub")

