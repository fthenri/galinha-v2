import re
import json

with open('src/logic/efeitos.ts', 'r', encoding='utf-8') as f:
    text = f.read()

effects = {}
for match in re.finditer(r'"([^"]+)"\s*:\s*(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>\s*aplicarVariacaoHp\([^,]+,\s*[^,]+,\s*(\d+),\s*(\d+)', text):
    name = match.group(1)
    min_val = match.group(2)
    max_val = match.group(3)
    effects[name] = f"{min_val}-{max_val}"

output = "export const EFEITOS_DADOS: Record<string, string> = " + json.dumps(effects, indent=2) + ";"

with open('src/data/efeitosDb.ts', 'w', encoding='utf-8') as f:
    f.write(output)
print('Done!')

