import codecs
import re

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

bad_block_regex = r'const foiRefletido = \(defensor\.efeitos\["Reflection"\] \|\| 0\) > 0;\s*let msgAtaque = "";\s*let alvoEfeito;\s*const alvoDano = defensor;\s*const tinhaEscudo = \(alvoDano\.efeitos\["Shield"\] \|\| 0\) > 0;\s*danoReal = alvoDano\.sofrerDano\(danoAtaque\);\s*msgAtaque = `\$\{nomeAtacante\} usou \$\{nomeSkill\} causando \$\{danoReal\} de dano`;\s*if \(tinhaEscudo\) msgAtaque \+= " \(Bloqueado\)";\s*alvoEfeito = defensor;\s*\}'

good_block = '''const foiRefletido = (defensor.efeitos["Reflection"] || 0) > 0;
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
                    }'''

if re.search(bad_block_regex, text):
    text = re.sub(bad_block_regex, good_block, text)
    with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
        f.write(text)
    print('Done replacing.')
else:
    print('Bad block not found!')

