import sys
import os
import json

sys.path.append(os.path.join('D:\\projects\\galinha-v2\\rinha-offline\\codigo_antigo', 'data'))
from galos_db import GALOS_DB

output = []
output.append('export type Skill = {')
output.append('  nome: string;')
output.append('  min: number;')
output.append('  max: number;')
output.append('  efeito?: string;')
output.append('  chance?: number;')
output.append('  turnos?: number;')
output.append('};')
output.append('')
output.append('export type GaloData = {')
output.append('  tipo: string;')
output.append('  raridade: string;')
output.append('  hp_base: number;')
output.append('  caminho_imagem: string;')
output.append('  skills: Record<number, Skill>;')
output.append('};')
output.append('')
output.append('export const GALOS_DB: Record<string, GaloData> = {')

for galo, data in GALOS_DB.items():
    output.append(f'  "{galo}": {{')
    output.append(f'    tipo: "{data["tipo"]}",')
    output.append(f'    raridade: "{data["raridade"]}",')
    output.append(f'    hp_base: {data["hp_base"]},')
    output.append(f'    caminho_imagem: "{data["caminho_imagem"]}",')
    output.append('    skills: {')
    for level, skill in data['skills'].items():
        skill_json = json.dumps(skill, ensure_ascii=False)
        output.append(f'      {level}: {skill_json},')
    output.append('    }')
    output.append('  },')

output.append('};')

with open('D:\\projects\\galinha-v2\\rinha-offline\\src\\data\\galosDb.ts', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('Done')
