import re
import json
import codecs

with codecs.open('src/logic/efeitos.ts', 'r', 'utf-8') as f:
    text = f.read()

effects = {}
# Match aplicarVariacaoHp
for match in re.finditer(r'"([^"]+)"\s*:\s*(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>\s*aplicarVariacaoHp\([^,]+,\s*[^,]+,\s*(-?\d+),\s*(-?\d+)', text):
    name = match.group(1)
    min_val = match.group(2)
    max_val = match.group(3)
    effects[name] = f"{min_val}-{max_val}"

# Match modificarDano
for match in re.finditer(r'"([^"]+)"\s*:\s*\([^)]*\)\s*=>\s*modificarDano\([^,]+,\s*(-?\d+)\)', text):
    name = match.group(1)
    val = match.group(2)
    effects[name] = str(val)

# Match stuns - we just add them with value "1" (or "2" for Double Stun) so they exist in EFEITOS_DADOS
for match in re.finditer(r'"([^"]+)"\s*:\s*aplicarImobilizacao', text):
    name = match.group(1)
    if name == "Double Stun":
        effects[name] = "2"
    else:
        effects[name] = "1"

effects["Life Steal"] = ""
effects["Trade Blood For Food"] = ""

output = "export const EFEITOS_DADOS: Record<string, string> = " + json.dumps(effects, indent=2) + ";"

with codecs.open('src/data/efeitosDb.ts', 'w', 'utf-8') as f:
    f.write(output)
print('Done!')

