import { useState } from 'react';
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
        if (modo === 'Raid' || modo === 'Dungeon' || modo === 'Arena' || modo === 'Survival') {
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
        }
    };

    if (modoAtivo === 'treino') {
        return (
            <div className="w-full flex flex-col items-center">
                <button onClick={() => setModoAtivo(null)} className="mb-4 bg-zinc-800 text-white font-bold py-2 px-4 rounded-lg hover:bg-zinc-700 w-full max-w-4xl mt-6 text-left">← Abandonar Batalha</button>
                <ModoTreino jogador={meuGalo} />
            </div>
        );
    }
    
    if (modoAtivo === 'trial') {
        return (
            <div className="w-full flex flex-col items-center">
                <button onClick={() => setModoAtivo(null)} className="mb-4 bg-zinc-800 text-white font-bold py-2 px-4 rounded-lg hover:bg-zinc-700 w-full max-w-4xl mt-6 text-left">← Abandonar Batalha</button>
                <ModoTrial jogador={meuGalo} />
            </div>
        );
    }

    return (
        <div className="p-6 flex flex-col items-center max-w-4xl mx-auto w-full">
            <h2 className="text-3xl font-bold mb-8 text-white">Hub de Batalhas</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl px-4 mt-8">
                <button onClick={() => handleModoClick('Trial')} className="bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700 rounded-2xl p-6 text-left flex flex-col justify-start transition-all duration-200 shadow-lg group">
                    <h3 className="text-xl font-black text-zinc-100 uppercase tracking-wider group-hover:text-amber-500 transition-colors">TRIAL</h3>
                    <p className="text-sm text-zinc-400 mt-3 leading-relaxed">Enfrente provações exclusivas da sua classe para obter bônus globais de atributos.</p>
                </button>

                <button onClick={() => handleModoClick('Treino')} className="bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700 rounded-2xl p-6 text-left flex flex-col justify-start transition-all duration-200 shadow-lg group">
                    <h3 className="text-xl font-black text-zinc-100 uppercase tracking-wider group-hover:text-amber-500 transition-colors">TREINO</h3>
                    <p className="text-sm text-zinc-400 mt-3 leading-relaxed">Batalhas infinitas e casuais para ganhar XP, subir de nível e farmar moedas.</p>
                </button>

                <button onClick={() => handleModoClick('Raid')} className="bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700 rounded-2xl p-6 text-left flex flex-col justify-start transition-all duration-200 shadow-lg group opacity-75 hover:opacity-100">
                    <h3 className="text-xl font-black text-zinc-100 uppercase tracking-wider group-hover:text-amber-500 transition-colors">RAID</h3>
                    <p className="text-sm text-zinc-400 mt-3 leading-relaxed">Desafie chefões colossais em batalhas extremas para saques raros.</p>
                    <div className="mt-5 inline-block bg-amber-500/10 border border-amber-500/30 text-amber-500 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider w-max">Em breve</div>
                </button>
                
                <button onClick={() => handleModoClick('Dungeon')} className="bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700 rounded-2xl p-6 text-left flex flex-col justify-start transition-all duration-200 shadow-lg group opacity-75 hover:opacity-100">
                    <h3 className="text-xl font-black text-zinc-100 uppercase tracking-wider group-hover:text-amber-500 transition-colors">DUNGEON</h3>
                    <p className="text-sm text-zinc-400 mt-3 leading-relaxed">Explore masmorras profundas e enfrente ondas perigosas de inimigos.</p>
                    <div className="mt-5 inline-block bg-amber-500/10 border border-amber-500/30 text-amber-500 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider w-max">Em breve</div>
                </button>

                <button onClick={() => handleModoClick('Arena')} className="bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700 rounded-2xl p-6 text-left flex flex-col justify-start transition-all duration-200 shadow-lg group opacity-75 hover:opacity-100">
                    <h3 className="text-xl font-black text-zinc-100 uppercase tracking-wider group-hover:text-amber-500 transition-colors">ARENA</h3>
                    <p className="text-sm text-zinc-400 mt-3 leading-relaxed">Prove o seu valor contra as equipas de outros jogadores.</p>
                    <div className="mt-5 inline-block bg-amber-500/10 border border-amber-500/30 text-amber-500 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider w-max">Em breve</div>
                </button>

                <button onClick={() => handleModoClick('Survival')} className="bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700 rounded-2xl p-6 text-left flex flex-col justify-start transition-all duration-200 shadow-lg group opacity-75 hover:opacity-100">
                    <h3 className="text-xl font-black text-zinc-100 uppercase tracking-wider group-hover:text-amber-500 transition-colors">SURVIVAL</h3>
                    <p className="text-sm text-zinc-400 mt-3 leading-relaxed">Sobreviva o máximo que puder contra hordas infinitas e implacáveis.</p>
                    <div className="mt-5 inline-block bg-amber-500/10 border border-amber-500/30 text-amber-500 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider w-max">Em breve</div>
                </button>
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