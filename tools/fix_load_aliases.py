# tools/fix_load_aliases.py
# Corrige toutes les fixtures d'alias (1 à 10) en ajoutant la catégorie à partir d'IndexEntry.
# Exécution : python .\tools\fix_load_aliases.py (Windows / PowerShell)

import os
import sys
import json
from pathlib import Path
from collections import Counter
from unidecode import unidecode

# --- Initialisation Django ---
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
import django
django.setup()

from apps.core.app_index.models import IndexEntry

# --- Dossier des fixtures ---
FIXTURES_DIR = Path("apps/core/app_index/fixtures")

# --- Parcours des fichiers initial_index_aliases_X.json (X = 1 à 10) ---
for i in range(1, 11):
    src = FIXTURES_DIR / f"initial_index_aliases_{i}.json"
    if not src.exists():
        print(f"[SKIP] Fichier non trouvé : {src.name}")
        continue

    print(f"\n[INFO] Traitement du fichier : {src.name}")
    data = json.loads(src.read_text(encoding="utf-8"))
    fixed, missing, alias_vides = [], [], []

    for obj in data:
        if obj.get("model") != "app_index.indexalias":
            fixed.append(obj)
            continue

        fields = obj.get("fields", {})
        
        # Ajoute alias_normalized si manquant
        if not fields.get("alias_normalized"):
            alias = fields.get("alias", "")
            normalized = unidecode(alias).lower().strip()
            fields["alias_normalized"] = normalized

        alias = fields.get("alias", "").strip()

        if not alias:
            alias_vides.append(obj)
            continue  # Ignore complètement les alias vides

        name = fields.get("entry", [None])[0]

        if name and not fields.get("category"):
            entries = IndexEntry.objects.filter(name=name).only("category_id")
            if entries.count() == 1:
                fields["category"] = entries.first().category_id
            elif entries.count() == 0:
                missing.append(name)
            else:
                raise ValueError(f"Doublon inattendu pour le nom : {name}")

        obj["fields"] = fields
        fixed.append(obj)

    # Écriture du fichier corrigé (même nom que l’original)
    src.write_text(json.dumps(fixed, ensure_ascii=False, indent=2), encoding="utf-8")

    # Résumé
    print(f"[OK] {len(fixed)} objets enregistrés.")
    if alias_vides:
        print(f"[WARN] {len(alias_vides)} alias vides ignorés.")
    if missing:
        noms_uniques = sorted(set(missing))
        print(f"[WARN] {len(noms_uniques)} noms introuvables dans IndexEntry :")
        for name in noms_uniques:
            print(f" - {name}")

    # Vérification globale
    print("[CHECK] Vérification finale des noms manquants dans IndexEntry...")
    counter = Counter()
    for obj in data:
        if obj.get("model") == "app_index.indexalias":
            fields = obj.get("fields", {})
            name = fields.get("entry", [None])[0]
            if name and not IndexEntry.objects.filter(name=name).exists():
                counter[name] += 1

    if counter:
        print(f"[RESULTAT] {len(counter)} noms sans correspondance :")
        for name, count in sorted(counter.items()):
            print(f" - {name} ({count} occurrence{'s' if count > 1 else ''})")
    else:
        print("[OK] Tous les noms ont une correspondance IndexEntry.")
