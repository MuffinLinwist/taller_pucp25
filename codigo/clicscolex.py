import itertools
import collections
import csv
from cltoolkit import Wordlist
from pycldf import Dataset
from pyclts import CLTS

# Inicializar CLTS
clts = CLTS()

# Cargar dataset CLICS (ajusta la ruta al metadata.json de CLICS)
wl = Wordlist([Dataset.from_metadata("../clics4/cldf/Wordlist-metadata.json")], ts=clts.bipa)

# Diccionario: lengua -> forma (tokens) -> conceptos
lang_forms = collections.defaultdict(lambda: collections.defaultdict(set))

# Recorrer datos
for language in wl.languages:
    for form in language.forms:
        tokens = " ".join(str(s) for s in form.segments)  # representamos la forma como string
        concept = form.concept.name  # o .id si prefieres Concepticon ID
        if tokens:
            lang_forms[language.id][tokens].add(concept)

# Contador global de colexificaciones
colex_counts = collections.Counter()

for lang, forms in lang_forms.items():
    for tokens, concepts in forms.items():
        if len(concepts) > 1:  # misma forma, múltiples conceptos
            for c1, c2 in itertools.combinations(sorted(concepts), 2):
                colex_counts[(c1, c2)] += 1

# Guardar archivo output
with open("../data/clicscolexificaciones.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["Concepto 1", "Concepto 2", "Colexifican"])
    for (c1, c2), count in colex_counts.items():
        writer.writerow([c1, c2, count])
