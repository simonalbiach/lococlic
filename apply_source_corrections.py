"""
Applique les corrections de sources sur le site LocoClic.

Modifie 2 endroits :
1. Modules JS lococlic_*_v5.html : sources:[{l:'...',u:'...'}]
2. Fiches pathologies : <a class="src-chip" href="..." ...>label</a>

Génère aussi un fichier CSV de rapport pour audit.
"""
import re
import sys
import csv
from pathlib import Path
sys.path.insert(0, '/home/claude/audit')
from corrections_final import CORRECTIONS

ROOT = Path("/home/claude/lococlic_site_final")

# Stats
stats = {
    "modules_modified": 0,
    "fiches_modified": 0,
    "occurrences_replaced": 0,
}

# Log pour CSV
log_rows = []

# ========================================
# 1. MODULES JS : sources:[{l:'...',u:'...'}]
# ========================================
modules = sorted(ROOT.glob("lococlic_*_v5.html"))
print(f"\n=== Modules JS ({len(modules)}) ===")

# Pattern pour matcher {l:'...',u:'...'} avec gestion des apostrophes échappées
# On va faire un remplacement intelligent : pour chaque ancien couple, on remplace
# par le nouveau couple en gardant la structure JS
for module in modules:
    text = module.read_text(encoding="utf-8")
    original = text
    n_local = 0
    
    for (old_url, old_label), new_data in CORRECTIONS.items():
        new_url = new_data["new_url"]
        new_label = new_data["new_label"]
        
        # Échapper les apostrophes pour la regex
        old_label_esc = old_label.replace("'", "\\\\'")
        # Pattern : {l:'<label>',u:'<url>'}
        # Le label peut contenir des apostrophes échappées
        pattern = re.compile(
            r"\{l:'" + re.escape(old_label_esc) + r"',u:'" + re.escape(old_url) + r"'\}"
        )
        
        # Nouveau bloc (échapper aussi les apostrophes du nouveau label)
        new_label_esc = new_label.replace("'", "\\'")
        replacement = "{l:'" + new_label_esc + "',u:'" + new_url + "'}"
        
        matches = pattern.findall(text)
        if matches:
            text = pattern.sub(replacement, text)
            n_local += len(matches)
            stats["occurrences_replaced"] += len(matches)
            for _ in matches:
                log_rows.append({
                    "file": module.name,
                    "old_label": old_label,
                    "old_url": old_url,
                    "new_label": new_label,
                    "new_url": new_url,
                })
    
    if text != original:
        module.write_text(text, encoding="utf-8")
        stats["modules_modified"] += 1
        print(f"  ✅ {module.name}: {n_local} sources corrigées")

# ========================================
# 2. FICHES PATHOLOGIES : <a class="src-chip" href="..."
# ========================================
fiches_dir = ROOT / "fiches_pathologies"
fiches = sorted(fiches_dir.glob("*.html"))
print(f"\n=== Fiches pathologies ({len(fiches)}) ===")

for fiche in fiches:
    text = fiche.read_text(encoding="utf-8")
    original = text
    n_local = 0
    
    for (old_url, old_label), new_data in CORRECTIONS.items():
        new_url = new_data["new_url"]
        new_label = new_data["new_label"]
        
        # Pattern : <a class="src-chip" href="<old_url>" target=...>label</a>
        # On accepte des variations légères de l'attribut target
        pattern = re.compile(
            r'<a class="src-chip"\s+href="' + re.escape(old_url) + r'"([^>]*)>' + 
            re.escape(old_label) + r'</a>'
        )
        
        matches = pattern.findall(text)
        if matches:
            new_anchor = f'<a class="src-chip" href="{new_url}" target="_blank" rel="noopener">{new_label}</a>'
            text = pattern.sub(new_anchor, text)
            n_local += len(matches)
            stats["occurrences_replaced"] += len(matches)
            for _ in matches:
                log_rows.append({
                    "file": f"fiches_pathologies/{fiche.name}",
                    "old_label": old_label,
                    "old_url": old_url,
                    "new_label": new_label,
                    "new_url": new_url,
                })
    
    if text != original:
        fiche.write_text(text, encoding="utf-8")
        stats["fiches_modified"] += 1

print(f"  ✅ {stats['fiches_modified']} fiches modifiées sur {len(fiches)}")

# ========================================
# RÉCAPITULATIF
# ========================================
print(f"\n{'='*60}")
print(f"RÉCAPITULATIF")
print(f"{'='*60}")
print(f"Modules JS modifiés     : {stats['modules_modified']}")
print(f"Fiches modifiées        : {stats['fiches_modified']}")
print(f"Total occurrences fixées: {stats['occurrences_replaced']}")

# ========================================
# CSV REPORT
# ========================================
report_path = Path("/mnt/user-data/outputs/LocoClic_audit_sources_rapport.csv")
report_path.parent.mkdir(parents=True, exist_ok=True)
with report_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["file", "old_label", "old_url", "new_label", "new_url"])
    writer.writeheader()
    writer.writerows(log_rows)

print(f"\n📊 Rapport CSV : {report_path}")
print(f"   {len(log_rows)} lignes")
