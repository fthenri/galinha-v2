import { useState, useEffect, useRef } from 'react';
import { useJogadorStore, calcularMultiplicadorRebirth } from '../store/jogadorStore';
import { Galo } from '../logic/Galo';
import { GALOS_DB } from '../data/galosDb';
import { BUFFS } from '../logic/efeitos';
import { SISTEMA_TIPOS, META_TIPOS } from '../data/tiposDb';

const PESOS_RARIDADE: Record<string, number> = {
    Common: 1, Rare: 2, Epic: 3, Legendary: 4, Mythic: 5, Divine: 6
};

export default function Rinha() {
    const galos = useJogadorStore(s => s.galos);
    const galoAtivoIndex = useJogadorStore(s => s.galoAtivoIndex);
    const meuGalo = galoAtivoIndex >= 0 && galoAtivoIndex < galos.length ? galos[galoAtivoIndex] : null;

    // ConfiguraÃ§Ãµes
    const [velRinha, setVelRinha] = useState(useJogadorStore.getState().velRinha);
    const [difRinha, setDifRinha] = useState(useJogadorStore.getState().difRinha);
    const autoRevive = useJogadorStore(s => s.autoRevive);
    const setAutoRevive = useJogadorStore(s => s.setAutoRevive);

    // Salva configs sempre que mudam
    useEffect(() => {
        useJogadorStore.setState({ velRinha, difRinha });
    }, [velRinha, difRinha]);

    // Estados da UI
    const [, setTick] = useState(0);
    const forceUpdate = () => setTick(t => t + 1);

    const [log, setLog] = useState<string[]>(["Procurando oponente..."]);
    const [inimigo, setInimigo] = useState<Galo | null>(null);
    const [treinoEncerrado, setTreinoEncerrado] = useState(false);
    
    // ReferÃªncias para o loop assÃ­ncrono
    const isMounted = useRef(true);
    const loopRodando = useRef(false);
    const solicitarReiniciar = useRef(false);
    const autoReviveRef = useRef(autoRevive);
    const velRinhaRef = useRef(velRinha);
    const difRinhaRef = useRef(difRinha);

    // Atualiza as refs sempre que os states de config mudarem (para o loop async ler sempre o valor mais fresco)
    useEffect(() => { autoReviveRef.current = autoRevive; }, [autoRevive]);
    useEffect(() => { velRinhaRef.current = velRinha; }, [velRinha]);
    useEffect(() => { difRinhaRef.current = difRinha; }, [difRinha]);

    useEffect(() => {
        isMounted.current = true;
        if (meuGalo && !loopRodando.current) {
            loopRodando.current = true;
            iniciarLoop();
        }
        return () => {
            isMounted.current = false;
        };
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [meuGalo]);

    if (!meuGalo) {
        return <div className="p-6 text-center text-red-500 font-bold">Equipe um galo no perfil primeiro!</div>;
    }

    const adicionarLog = (msg: string) => {
        setLog(prev => {
            const novo = [...prev, msg];
            if (novo.length > 3) novo.shift(); // MantÃ©m os Ãºltimos 3 (semelhante a > 2 no python)
            return novo;
        });
    };

    const iniciarLoop = async () => {
        // Inicializar hp atual igual ao max
        meuGalo.hp_max = Math.floor(((GALOS_DB[meuGalo.nome]?.hp_base || 100) + ((meuGalo.nivel - 1) * 12)) * calcularMultiplicadorRebirth(meuGalo.rebirths || 0));
        meuGalo.hp_atual = meuGalo.hp_max;

        const sleep = (ms: number) => new Promise(r => setTimeout(r, ms * 1000));

        while (isMounted.current) {
            const dificuldade = difRinhaRef.current;
            const nivelBase = meuGalo.nivel;
            const raridadeJogador = GALOS_DB[meuGalo.nome]?.raridade || "Common";
            const pesoJogador = PESOS_RARIDADE[raridadeJogador] || 1;

            let galosPermitidos: string[] = [];
            for (const [nome, dados] of Object.entries(GALOS_DB)) {
                const pesoInim = PESOS_RARIDADE[dados.raridade || "Common"] || 1;
                if (dificuldade === "Facil" && pesoInim <= 5) galosPermitidos.push(nome);
                else if (dificuldade === "Medio" && pesoInim >= 2) galosPermitidos.push(nome);
                else if (dificuldade === "Dificil" && pesoInim >= 3) galosPermitidos.push(nome);
                else if (dificuldade === "Extremo" && pesoInim >= 4) galosPermitidos.push(nome);
                else if (dificuldade === "Insano" && pesoInim >= 5) galosPermitidos.push(nome);
            }
            if (galosPermitidos.length === 0) galosPermitidos = Object.keys(GALOS_DB);

            const nomeSorteado = galosPermitidos[Math.floor(Math.random() * galosPermitidos.length)];
            const dadosInimigo = GALOS_DB[nomeSorteado];
            const pesoInimigo = PESOS_RARIDADE[dadosInimigo.raridade || "Common"] || 1;

            let nivelInimigo = nivelBase;
            let multXp = 1.0;
            let bonusXp = 0;

            if (dificuldade === "Facil") {
                nivelInimigo = Math.max(1, nivelBase - 1);
                if (pesoInimigo > pesoJogador) {
                    nivelInimigo = Math.max(1, nivelInimigo - (pesoInimigo - pesoJogador));
                }
                multXp = 1.0; bonusXp = 0;
            } else if (dificuldade === "Medio") {
                multXp = 1.30; bonusXp = 1;
            } else if (dificuldade === "Dificil") {
                nivelInimigo = Math.floor(nivelBase * 1.40);
                multXp = 1.60; bonusXp = 2;
            } else if (dificuldade === "Extremo") {
                nivelInimigo = nivelBase * 2;
                multXp = 1.80; bonusXp = 5;
            } else if (dificuldade === "Insano") {
                nivelInimigo = nivelBase * 3;
                multXp = 2.65; bonusXp = 8;
            }

            const hpInimigo = dadosInimigo.hp_base + ((nivelInimigo - 1) * 12);
            const novoInimigo = new Galo(nomeSorteado, hpInimigo, dadosInimigo.caminho_imagem, nivelInimigo, 0, dadosInimigo.tipo);
            novoInimigo.hp_atual = hpInimigo;
            
            // @ts-ignore
            novoInimigo.equiparSkillsBot();
            
            meuGalo.hp_atual = meuGalo.hp_max;
            meuGalo.efeitos = {};
            novoInimigo.efeitos = {};

            setInimigo(novoInimigo);
            adicionarLog(`Um ${novoInimigo.nome} Lvl ${novoInimigo.nivel} apareceu!`);
            setTreinoEncerrado(false);
            forceUpdate();

            let vel = parseFloat(velRinhaRef.current);
            await sleep(vel);

            let turnoJogador = true;

            while (meuGalo.hp_atual > 0 && novoInimigo.hp_atual > 0) {
                if (!isMounted.current) return;
                vel = parseFloat(velRinhaRef.current);

                const atacante = turnoJogador ? meuGalo : novoInimigo;
                const defensor = turnoJogador ? novoInimigo : meuGalo;
                const nomeAtacante = turnoJogador ? useJogadorStore.getState().nome : novoInimigo.nome;

                const resEfeitos = atacante.processarEfeitosInicioTurno();
                const mensagensEfeito = resEfeitos[0];
                const podeAtacar = resEfeitos[1];

                if (mensagensEfeito && mensagensEfeito.length > 0) {
                    for (const msg of mensagensEfeito) adicionarLog(msg);
                    forceUpdate();
                    await sleep(vel / 2);
                }

                if (atacante.hp_atual <= 0) break;

                if (podeAtacar) {
                    const resAtaque = atacante.atacar();
                    const nomeSkill = resAtaque[0];
                    const danoAtaque = resAtaque[1];
                    const efeito = resAtaque[2];

                    const foiRefletido = (defensor.efeitos["Reflection"] || 0) > 0;
                    let msgAtaque = "";
                    let alvoEfeito;
                    let danoReal;

                    if (foiRefletido) {
                        defensor.efeitos["Reflection"] -= 1;
                        if (defensor.efeitos["Reflection"] <= 0) delete defensor.efeitos["Reflection"];

                        const alvoDano = atacante;
                        const tinhaEscudo = (alvoDano.efeitos["Shield"] || 0) > 0;
                        danoReal = alvoDano.sofrerDano(danoAtaque, defensor.tipo);

                        msgAtaque = `${defensor.nome} refletiu o ataque! ${nomeAtacante} sofreu ${danoReal} de dano`;
                        if (tinhaEscudo) msgAtaque += " (Bloqueado)";
                        alvoEfeito = atacante;
                    } else {
                        const alvoDano = defensor;
                        const tinhaEscudo = (alvoDano.efeitos["Shield"] || 0) > 0;
                        danoReal = alvoDano.sofrerDano(danoAtaque, atacante.tipo);

                        msgAtaque = `${nomeAtacante} usou ${nomeSkill} causando ${danoReal} de dano`;
                        if (tinhaEscudo) msgAtaque += " (Bloqueado)";
                        alvoEfeito = defensor;
                    }

                    if (efeito) {
                        const alvoCorreto = BUFFS.includes(efeito.nome) ? atacante : alvoEfeito;
                        const aplicou = alvoCorreto.aplicarEfeito(efeito);

                        if (aplicou) {
                            const acao = alvoCorreto === atacante ? "ativou" : "aplicou";
                            msgAtaque += ` e ${acao} ${efeito.nome}!`;
                        }

                        if (aplicou && (efeito.nome === "Life Steal" || efeito.nome === "Trade Blood For Food")) {
                            atacante.hp_atual = Math.min(atacante.hp_max, atacante.hp_atual + danoReal);
                            msgAtaque += ` roubando ${danoReal} HP!`;
                        }
                    }

                    adicionarLog(msgAtaque);
                }

                forceUpdate();
                await sleep(vel);
                turnoJogador = !turnoJogador;
            }

            if (!isMounted.current) return;

            if (meuGalo.hp_atual > 0) {
                const xpBase = 34;
                const xpGanho = Math.floor((xpBase * multXp) + bonusXp);
                const moedasGanhas = 6;

                meuGalo.ganharXp(xpGanho);
                const state = useJogadorStore.getState();
                useJogadorStore.setState({ 
                    moedas: state.moedas + moedasGanhas,
                    galos: [...state.galos] // Dispara re-render da store
                });

                adicionarLog(`VocÃª venceu!\n+${moedasGanhas} Moedas | +${xpGanho} XP\nProcurando prÃ³ximo...`);
                forceUpdate();
                await sleep(parseFloat(velRinhaRef.current) * 2);
            } else {
                if (autoReviveRef.current) {
                    adicionarLog(`O teu galo foi derrotado...\nAuto-Revive ativado! Curando e procurando prÃ³ximo...`);
                    forceUpdate();
                    await sleep(parseFloat(velRinhaRef.current) * 2);
                    continue;
                }

                adicionarLog(`O teu galo foi derrotado... Treino encerrado.`);
                setTreinoEncerrado(true);
                forceUpdate();

                // Idle loop aguardando usuÃ¡rio clicar em reiniciar
                let reiniciarAgora = false;
                while (isMounted.current) {
                    if (solicitarReiniciar.current) {
                        solicitarReiniciar.current = false;
                        reiniciarAgora = true;
                        break;
                    }
                    await sleep(0.5);
                }

                setTreinoEncerrado(false);

                if (reiniciarAgora) {
                    adicionarLog("Reiniciando treinamento...");
                    forceUpdate();
                    await sleep(1);
                    continue;
                } else {
                    break;
                }
            }
        }
        loopRodando.current = false;
    };

    const pctMeu = Math.max(0, Math.min(100, (meuGalo.hp_atual / meuGalo.hp_max) * 100));
    const pctInimigo = inimigo ? Math.max(0, Math.min(100, (inimigo.hp_atual / inimigo.hp_max) * 100)) : 100;

    return (
        <div className="p-6 flex flex-col items-center max-w-4xl mx-auto w-full">
            <h2 className="text-3xl font-bold mb-6">Treinamento</h2>
            {/* Controles Glassmorphism */}
            <div className="flex flex-wrap gap-6 mb-6 justify-center items-center bg-zinc-800/40 backdrop-blur-sm border border-zinc-700/50 p-6 rounded-2xl w-full shadow-lg">
                <div className="flex flex-col w-40">
                    <label className="text-sm text-zinc-400 mb-1 font-semibold">Velocidade</label>
                    <select 
                        value={velRinha} 
                        onChange={e => setVelRinha(e.target.value)}
                        className="bg-zinc-800 border border-zinc-700 text-zinc-200 text-sm rounded-lg focus:ring-amber-500 focus:outline-none block w-full p-2.5 cursor-pointer"
                    >
                        <option value="1.0">1x (Normal)</option>
                        <option value="0.5">2x (Rápido)</option>
                        <option value="0.1">10x (Flash)</option>
                    </select>
                </div>

                <div className="flex flex-col w-40">
                    <label className="text-sm text-zinc-400 mb-1 font-semibold">Dificuldade</label>
                    <select 
                        value={difRinha} 
                        onChange={e => setDifRinha(e.target.value)}
                        className="bg-zinc-800 border border-zinc-700 text-zinc-200 text-sm rounded-lg focus:ring-amber-500 focus:outline-none block w-full p-2.5 cursor-pointer"
                    >
                        <option value="Facil">Fácil</option>
                        <option value="Medio">Médio</option>
                        <option value="Dificil">Difícil</option>
                        <option value="Extremo">Extremo</option>
                        <option value="Insano">Insano</option>
                    </select>
                </div>

                <div className="flex flex-col justify-center items-center px-4 pt-6">
                    <label className="text-sm text-zinc-400 mb-2 font-semibold">Auto-Revive</label>
                    <input 
                        type="checkbox" 
                        checked={autoRevive}
                        onChange={e => setAutoRevive(e.target.checked)}
                        className="w-5 h-5 accent-amber-500 cursor-pointer"
                    />
                </div>
            </div>

            {/* Arena */}
            <div className="bg-black/80 w-full rounded-xl p-6 border border-zinc-800 shadow-xl relative">
                
                {/* Painel de Log Modernizado */}
                <div className="bg-black/40 h-32 p-4 rounded-xl mb-6 text-sm whitespace-pre-wrap flex flex-col justify-end overflow-y-auto" style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}>
                    {log.map((linha, idx) => {
                        const isUltima = idx === log.length - 1;
                        return (
                            <span key={idx} className={isUltima ? 'text-white font-bold drop-shadow-md transition-all duration-300' : 'text-zinc-500 mb-1'}>{linha}</span>
                        );
                    })}
                </div>

                {/* HP Bars */}
                <div className="flex justify-between items-start gap-16 relative z-0">
                    {/* Jogador */}
                    <div className="flex-1">
                        <div className="flex justify-between items-end mb-2">
                            <span className="font-bold text-lg">{useJogadorStore.getState().nome} <span className="text-sm text-zinc-400 font-normal">Nv.{meuGalo.nivel}</span></span>
                            <span className="text-sm font-bold text-zinc-300">{Math.floor(meuGalo.hp_atual)} / {meuGalo.hp_max}</span>
                        </div>
                        <div className="w-full bg-zinc-800 h-5 rounded-full overflow-hidden shadow-inner border border-zinc-700/50">
                            <div className="bg-green-500 h-full rounded-full transition-all duration-300 shadow-[0_0_10px_rgba(34,197,94,0.5)]" style={{ width: pctMeu + '%' }}></div>
                        </div>
                    </div>

                    {/* Inimigo */}
                    {inimigo && (
                        <div className="flex-1 text-right">
                            <div className="flex justify-between items-end mb-2 flex-row-reverse">
                                <span className="font-bold text-lg">{inimigo.nome} <span className="text-sm text-zinc-400 font-normal">Nv.{inimigo.nivel}</span></span>
                                <span className="text-sm font-bold text-zinc-300">{Math.floor(inimigo.hp_atual)} / {inimigo.hp_max}</span>
                            </div>
                            <div className="w-full bg-zinc-800 h-5 rounded-full overflow-hidden flex justify-end shadow-inner border border-zinc-700/50">
                                <div className="bg-purple-500 h-full rounded-full transition-all duration-300 shadow-[0_0_10px_rgba(168,85,247,0.5)]" style={{ width: pctInimigo + '%' }}></div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Personagens */}
                <div className="relative flex justify-around items-center w-full mt-8">
                    {/* VS Element movido para ca */}
                    {inimigo && (
                        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center justify-center z-10 w-16 h-16 bg-zinc-900 rounded-full border-2 border-amber-600 shadow-[0_0_20px_rgba(217,119,6,0.6)]">
                            <span className="text-amber-500 font-black italic text-2xl drop-shadow-lg">VS</span>
                        </div>
                    )}

                    <div className="flex flex-col items-center">
                        {inimigo && (
                            <div className="flex items-center justify-center gap-2 mb-3">
                                <span className={`px-3 py-1 rounded-md text-xs font-bold ${META_TIPOS[meuGalo.tipo]?.corFundo || 'bg-zinc-800'} ${META_TIPOS[meuGalo.tipo]?.corTexto || 'text-zinc-300'}`}>
                                    {META_TIPOS[meuGalo.tipo]?.icone || ''} {meuGalo.tipo}
                                </span>
                                {SISTEMA_TIPOS[meuGalo.tipo]?.vantagem.includes(inimigo.tipo) && (
                                    <span className="text-emerald-400 text-xs font-bold tracking-wide">↑ +15% Dano</span>
                                )}
                                {SISTEMA_TIPOS[meuGalo.tipo]?.desvantagem.includes(inimigo.tipo) && (
                                    <span className="text-red-400 text-xs font-bold tracking-wide">↓ -10% Dano</span>
                                )}
                            </div>
                        )}
                        <div className="w-32 h-32 md:w-48 md:h-48 relative">
                            <img src={"/" + meuGalo.caminho_imagem} className="w-full h-full object-contain drop-shadow-[0_0_15px_rgba(34,197,94,0.3)]" alt="Meu Galo" />
                        </div>
                    </div>
                    
                    <div className="flex flex-col items-center">
                        {inimigo && (
                            <>
                                <div className="flex items-center justify-center gap-2 mb-3">
                                    <span className={`px-3 py-1 rounded-md text-xs font-bold ${META_TIPOS[inimigo.tipo]?.corFundo || 'bg-zinc-800'} ${META_TIPOS[inimigo.tipo]?.corTexto || 'text-zinc-300'}`}>
                                        {META_TIPOS[inimigo.tipo]?.icone || ''} {inimigo.tipo}
                                    </span>
                                    {SISTEMA_TIPOS[inimigo.tipo]?.vantagem.includes(meuGalo.tipo) && (
                                        <span className="text-emerald-400 text-xs font-bold tracking-wide">↑ +15% Dano</span>
                                    )}
                                    {SISTEMA_TIPOS[inimigo.tipo]?.desvantagem.includes(meuGalo.tipo) && (
                                        <span className="text-red-400 text-xs font-bold tracking-wide">↓ -10% Dano</span>
                                    )}
                                </div>
                                <div className="w-32 h-32 md:w-48 md:h-48 relative">
                                    <img src={"/" + inimigo.caminho_imagem} className="w-full h-full object-contain scale-x-[-1] drop-shadow-[0_0_15px_rgba(168,85,247,0.3)]" alt="Inimigo" />
                                </div>
                            </>
                        )}
                    </div>
                </div>

            </div>

            {/* Reiniciar */}
            {treinoEncerrado && (
                <button 
                    onClick={() => { solicitarReiniciar.current = true; }}
                    className="mt-6 bg-green-700 hover:bg-green-600 text-white font-bold py-3 px-8 rounded-lg shadow-lg text-lg transition-colors"
                >
                    Treinar Novamente
                </button>
            )}

        </div>
    );
}
