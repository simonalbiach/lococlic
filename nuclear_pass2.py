"""
Passe complémentaire : pour chaque module JS, parcourir CHAQUE entrée
{l:'...',u:'...'} indépendamment et supprimer celles non whitelistées.
Au lieu de bloc complet, on travaille item par item.
"""
import re
import json
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path("/home/claude/lococlic_site_final")
wl = json.loads(Path("/home/claude/audit/whitelist.json").read_text())
WHITELIST_EXACT = set(wl["exact"])
WHITELIST_PREFIXES = wl["prefixes"]

def is_whitelisted(url):
    if url in WHITELIST_EXACT:
        return True
    for p in WHITELIST_PREFIXES:
        if url.startswith(p):
            return True
    return False

stats = {"removed": 0, "modules": 0}
log_removed = []

# Pattern : un item complet {l:'...',u:'...'}
pat_item = re.compile(r"\{l:'((?:[^'\\]|\\.)*)',u:'([^']+)'\}")

for module in ROOT.glob("lococlic_*_v5.html"):
    text = module.read_text(encoding="utf-8")
    original = text
    
    # Pour chaque item, vérifier la whitelist et virer si pas OK
    # Stratégie : on traite de la fin vers le début pour ne pas casser les indices
    matches = list(pat_item.finditer(text))
    
    # Identifier les ranges à supprimer (avec gestion des virgules)
    ranges_to_remove = []
    for m in matches:
        url = m.group(2).strip()
        if not is_whitelisted(url):
            label = m.group(1).replace("\\'", "'")
            log_removed.append({
                "file": module.name,
                "label": label,
                "url": url,
            })
            ranges_to_remove.append((m.start(), m.end(), label, url))
            stats["removed"] += 1
    
    # Procéder à la suppression de la fin vers le début
    # Avec gestion intelligente des virgules : si l'item suivant est `,` on l'enlève aussi
    # Si l'item précédent est `,` on l'enlève aussi
    for start, end, _, _ in reversed(ranges_to_remove):
        # Regarder le contexte
        # Cas 1 : précédé d'une virgule "...,{...}"  → enlever ",{...}"
        # Cas 2 : suivi d'une virgule "{...},..."   → enlever "{...},"
        # Cas 3 : seul "[{...}]"                     → enlever juste "{...}"
        
        # On commence par l'élément lui-même
        new_start = start
        new_end = end
        
        # Si suivi de "," → englober la virgule
        if new_end < len(text) and text[new_end] == ",":
            new_end += 1
        # Sinon, si précédé de "," → englober la virgule précédente
        elif new_start > 0 and text[new_start - 1] == ",":
            new_start -= 1
        
        text = text[:new_start] + text[new_end:]
    
    # Nettoyer les blocs sources:[] vides (résultat possible)
    # Sources vide → on doit ajouter un fallback (déjà géré dans premier script, mais re-vérifions)
    # On laisse les sources:[] en l'état si vides (à corriger en visuel après)
    
    if text != original:
        module.write_text(text, encoding="utf-8")
        stats["modules"] += 1
        print(f"  ✅ {module.name}")

print(f"\n=== STATS ===")
print(f"Modules touchés : {stats['modules']}")
print(f"Sources supprimées : {stats['removed']}")

# Update CSV
existing_csv = Path("/mnt/user-data/outputs/LocoClic_audit_NUCLEAIRE_rapport.csv")
existing_rows = []
if existing_csv.exists():
    with existing_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_rows = list(reader)

# Append log_removed
all_rows = existing_rows + log_removed
with existing_csv.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "label", "url"])
    w.writeheader()
    w.writerows(all_rows)

print(f"\n📊 CSV cumulatif : {len(all_rows)} suppressions")
