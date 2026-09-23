import codecs

with codecs.open('src/components/Rinha.tsx', 'r', 'utf-8') as f:
    text = f.read()

text = text.replace("        } else if (modo === 'Treino') {\n            setModoAtivo('treino');\n        \n    };", "        } else if (modo === 'Treino') {\n            setModoAtivo('treino');\n        }\n    };")

with codecs.open('src/components/Rinha.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Done brace")

