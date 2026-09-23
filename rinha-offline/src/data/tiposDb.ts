export type RelacaoTipos = {
    vantagem: string[];
    desvantagem: string[];
};

export const SISTEMA_TIPOS: Record<string, RelacaoTipos> = {
    "Basic": { vantagem: ['Illusion', 'Mystic'], desvantagem: ['Wild', 'Craft'] },
    "Craft": { vantagem: ['Basic', 'Aquatic'], desvantagem: ['Ruin', 'Warrior'] },
    "Ruin": { vantagem: ['Wild', 'Craft'], desvantagem: ['Aquatic', 'Shadow'] },
    "Aquatic": { vantagem: ['Ruin', 'Radiant'], desvantagem: ['Wild', 'Craft'] },
    "Wild": { vantagem: ['Aquatic', 'Basic'], desvantagem: ['Ruin', 'Illusion'] },
    "Illusion": { vantagem: ['Warrior', 'Wild'], desvantagem: ['Radiant', 'Basic'] },
    "Radiant": { vantagem: ['Shadow', 'Illusion'], desvantagem: ['Aquatic', 'Mystic'] },
    "Warrior": { vantagem: ['Shadow', 'Craft'], desvantagem: ['Mystic', 'Illusion'] },
    "Mystic": { vantagem: ['Warrior', 'Radiant'], desvantagem: ['Shadow', 'Basic'] },
    "Shadow": { vantagem: ['Mystic', 'Ruin'], desvantagem: ['Radiant', 'Warrior'] }
};

export type MetaTipo = {
    icone: string;
    corTexto: string;
    corFundo: string;
};

export const META_TIPOS: Record<string, MetaTipo> = {
    "Basic": { icone: "🐾", corTexto: "text-zinc-400", corFundo: "bg-zinc-800" },
    "Craft": { icone: "⚙️", corTexto: "text-amber-400", corFundo: "bg-amber-950" },
    "Ruin": { icone: "💀", corTexto: "text-red-500", corFundo: "bg-red-950" },
    "Aquatic": { icone: "💧", corTexto: "text-blue-400", corFundo: "bg-blue-950" },
    "Wild": { icone: "🌿", corTexto: "text-emerald-400", corFundo: "bg-emerald-950" },
    "Illusion": { icone: "🌀", corTexto: "text-fuchsia-400", corFundo: "bg-fuchsia-950" },
    "Radiant": { icone: "✨", corTexto: "text-yellow-400", corFundo: "bg-yellow-950" },
    "Warrior": { icone: "⚔️", corTexto: "text-orange-500", corFundo: "bg-orange-950" },
    "Mystic": { icone: "🔮", corTexto: "text-purple-400", corFundo: "bg-purple-950" },
    "Shadow": { icone: "🌙", corTexto: "text-indigo-400", corFundo: "bg-indigo-950" }
};
