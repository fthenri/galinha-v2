import { useState, useEffect, useRef } from 'react';
import { useJogadorStore, calcularMultiplicadorRebirth } from '../store/jogadorStore';
import { Galo } from '../logic/Galo';
import { GALOS_DB } from '../data/galosDb';
import { BUFFS } from '../logic/efeitos';
import { SISTEMA_TIPOS, META_TIPOS } from '../data/tiposDb';

const PESOS_RARIDADE: Record<string, number> = {
    Common: 1, Rare: 2, Epic: 3, Legendary: 4, Mythic: 5, Divine: 6
};

type ConfigDificuldade = {
    cor: string;
    texto: string;
    calcNivel: (nivelBase: number) => number;
    calcRebirths: (rebirthsJogador: number) => number;
    inimigoEvoluido?: boolean;
    calcXp: (xpBase: number) => number;
};

const CONFIG_DIFICULDADE: Record<string, ConfigDificuldade> = {
    Facil: {
        cor: 'text-green-500',
        texto: 'Todos os galos são um nível a menos',
        calcNivel: (n) => Math.max(1, n - 1),
        calcRebirths: () => 0,
        calcXp: (xp) => xp
    },
    Medio: {
        cor: 'text-yellow-500',
        texto: 'Mesmo nível que o seu, com 1/3 dos resets. Benefícios: 30% de XP extra e +1 de XP fixo',
        calcNivel: (n) => n,
        calcRebirths: (r) => Math.floor(r / 3),
        calcXp: (xp) => xp * 1.3 + 1
    },
    Dificil: {
        cor: 'text-orange-500',
        texto: 'Galo com 40% a mais de nível, metade dos seus resets +2. Benefícios: 60% de XP extra e +2 de XP fixo',
        calcNivel: (n) => Math.floor(n * 1.4),
        calcRebirths: (r) => Math.floor(r / 2) + 2,
        calcXp: (xp) => xp * 1.6 + 2
    },
    Extremo: {
        cor: 'text-red-500',
        texto: '2x a mais de nível, metade dos seus resets +8, ataque evoluído. Benefícios: 80% de XP extra, +5 de XP fixo',
        calcNivel: (n) => n * 2,
        calcRebirths: (r) => Math.floor(r / 2) + 8,
        inimigoEvoluido: true,
        calcXp: (xp) => xp * 1.8 + 5
    },
    Insano: {
        cor: 'text-purple-500',
        texto: '3x a mais de nível, seus resets +20, ataque evoluído. Benefícios: 165% de XP extra, +8 de XP fixo',
        calcNivel: (n) => n * 3,
        calcRebirths: (r) => r + 20,
        inimigoEvoluido: true,
        calcXp: (xp) => xp * 2.65 + 8
    }
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
    const [modalDificuldadeOpen, setModalDificuldadeOpen] = useState(false);
    
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

            const configDif = CONFIG_DIFICULDADE[dificuldade] || CONFIG_DIFICULDADE.Facil;
            let nivelInimigo = configDif.calcNivel(nivelBase);
            if (dificuldade === "Facil" && pesoInimigo > pesoJogador) {
                nivelInimigo = Math.max(1, nivelInimigo - (pesoInimigo - pesoJogador));
            }
            const rebirthsInimigo = configDif.calcRebirths(meuGalo.rebirths || 0);

            const hpInimigoSemRebirth = dadosInimigo.hp_base + ((nivelInimigo - 1) * 12);
            const hpInimigoComRebirth = Math.floor(hpInimigoSemRebirth * calcularMultiplicadorRebirth(rebirthsInimigo));

            const novoInimigo = new Galo(
                nomeSorteado, 
                hpInimigoComRebirth, 
                dadosInimigo.caminho_imagem, 
                nivelInimigo, 
                0, 
                dadosInimigo.tipo,
                null,
                null,
                rebirthsInimigo,
                configDif.inimigoEvoluido || false
            );
            novoInimigo.hp_atual = hpInimigoComRebirth;
            
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
                const configDif = CONFIG_DIFICULDADE[difRinhaRef.current] || CONFIG_DIFICULDADE.Facil;
                const xpGanho = Math.floor(configDif.calcXp(xpBase));
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
                    <button
                        onClick={() => setModalDificuldadeOpen(true)}
                        className="bg-zinc-800 border border-zinc-700 text-zinc-200 p-2.5 rounded-lg w-full flex justify-between items-center hover:bg-zinc-700 transition-colors"
                    >
                        <span>Dificuldade: {difRinha}</span>
                        <span className="text-zinc-500">▼</span>
                    </button>
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

            {/* Modal de Seleção de Dificuldade */}
            {modalDificuldadeOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm p-4">
                    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 w-full max-w-md flex flex-col">
                        <h3 className="text-xl font-bold text-zinc-100 mb-4 text-center">Train difficulty</h3>
                        
                        <div className="flex flex-wrap gap-3 justify-center mb-6">
                            {Object.keys(CONFIG_DIFICULDADE).map((dificuldadeKey) => (
                                <button
                                    key={dificuldadeKey}
                                    onClick={() => setDifRinha(dificuldadeKey)}
                                    className={`py-2 px-4 rounded-lg font-bold transition-all ${
                                        difRinha === dificuldadeKey 
                                        ? 'bg-zinc-800 ring-2 ring-amber-500 text-white' 
                                        : 'bg-zinc-900 opacity-70 text-zinc-400 hover:opacity-100 border border-zinc-700'
                                    }`}
                                >
                                    {dificuldadeKey}
                                </button>
                            ))}
                        </div>

                        <div className="text-sm text-zinc-300 mt-2 bg-zinc-950 p-4 rounded-lg border border-zinc-800 text-center">
                            {CONFIG_DIFICULDADE[difRinha]?.texto}
                        </div>

                        <button 
                            onClick={() => setModalDificuldadeOpen(false)}
                            className="w-full bg-amber-600 hover:bg-amber-500 text-white font-bold py-2 rounded-lg mt-6 transition-colors"
                        >
                            Confirmar
                        </button>
                    </div>
                </div>
            )}

        </div>
    );
}
