import csv
import itertools
import collections

# Archivo de entrada
input_file = "../data/quechua_modern_wordlist.tsv"
output_file = "../data/colexificaciones.tsv"

# Diccionario: lengua -> forma (tokens) -> conjunto de conceptos
lang_forms = collections.defaultdict(lambda: collections.defaultdict(set))

# Leer archivo
with open(input_file, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        lang = row["DOCULECT"].strip()
        concept = row["CONCEPT"].strip()
        tokens = row["TOKENS"].strip()
        if tokens:  # solo consideramos entradas con forma
            lang_forms[lang][tokens].add(concept)

# Contador global de colexificaciones
colex_counts = collections.Counter()

for lang, forms in lang_forms.items():
    for tokens, concepts in forms.items():
        if len(concepts) > 1:  # hay más de un concepto con la misma forma
            for c1, c2 in itertools.combinations(sorted(concepts), 2):
                colex_counts[(c1, c2)] += 1

# Guardar salida
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["Concepto 1", "Concepto 2", "Colexifican"])
    for (c1, c2), count in colex_counts.items():
        writer.writerow([c1, c2, count])