import { useState, useEffect } from 'react';
import { User, Swords, Store, BookOpen } from 'lucide-react';

import Perfil from './components/Perfil';
import Rinha from './components/Rinha';
import Loja from './components/Loja';
import Galinheiro from './components/Galinheiro';

export default function App() {
  const [activeTab, setActiveTab] = useState<'perfil' | 'treino' | 'loja' | 'codex'>('perfil');

  useEffect(() => {
    const handler = (e: any) => {
      if (e.detail?.tab) setActiveTab(e.detail.tab);
    };
    window.addEventListener('changeTab', handler);
    return () => window.removeEventListener('changeTab', handler);
  }, []);

  return (
    <div className="bg-zinc-900 min-h-screen text-white flex flex-col">
      <div className="flex-1 overflow-y-auto pb-16">
        {activeTab === 'perfil' && <Perfil />}
        {activeTab === 'treino' && <Rinha />}
        {activeTab === 'loja' && <Loja />}
        {activeTab === 'codex' && <Galinheiro />}
      </div>

      <div className="fixed bottom-0 w-full bg-zinc-800 border-t border-zinc-700 flex justify-around items-center h-16">
        <button 
          onClick={() => setActiveTab('perfil')}
          className={`flex flex-col items-center justify-center w-full h-full ${activeTab === 'perfil' ? 'text-amber-500' : 'text-zinc-400 hover:text-zinc-300'}`}
        >
          <User size={24} />
          <span className="text-xs mt-1">Perfil</span>
        </button>
        <button 
          onClick={() => setActiveTab('treino')}
          className={`flex flex-col items-center justify-center w-full h-full ${activeTab === 'treino' ? 'text-amber-500' : 'text-zinc-400 hover:text-zinc-300'}`}
        >
          <Swords size={24} />
          <span className="text-xs mt-1">Treino</span>
        </button>
        <button 
          onClick={() => setActiveTab('loja')}
          className={`flex flex-col items-center justify-center w-full h-full ${activeTab === 'loja' ? 'text-amber-500' : 'text-zinc-400 hover:text-zinc-300'}`}
        >
          <Store size={24} />
          <span className="text-xs mt-1">Loja</span>
        </button>
        <button 
          onClick={() => setActiveTab('codex')}
          className={`flex flex-col items-center justify-center w-full h-full ${activeTab === 'codex' ? 'text-amber-500' : 'text-zinc-400 hover:text-zinc-300'}`}
        >
          <BookOpen size={24} />
          <span className="text-xs mt-1">Galinheiro</span>
        </button>
      </div>
    </div>
  );
}
