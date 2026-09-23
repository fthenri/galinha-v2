export type ItemRarity = 'Common' | 'Rare' | 'Epic' | 'Legendary' | 'Special' | 'Mythic';

export interface ItemModifiers {
  ataqueBonus?: number;
  vidaBonus?: number;
  bloqueioDano?: number;
  chanceEfeitoBonus?: number;
  danoEfeitoBonus?: number;
  regeneracao?: number;
  xpBonus?: number;
  dinheiroBonus?: number;
  curaBonus?: number;
  curaOponenteReducao?: number;
  bloqueioEfeito?: number;
  voodoo?: number;
  reducaoChanceEfeitoOponente?: number;
  xpShare?: number;
  efeitoAoAtacar?: { nome: string; chance: number };
}

export interface Item {
  id: string;
  nome: string;
  raridade: ItemRarity;
  descricao: string;
  modificadores: ItemModifiers;
}

