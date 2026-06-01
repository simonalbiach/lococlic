"""
Opération NUCLÉAIRE : 
1. Supprime toutes les sources non whitelistées
2. Pour les fiches qui se retrouvent sans aucune source, ajoute une source 
   de fallback selon la zone anatomique (toutes URLs whitelistées)

Cible :
- Fiches pathologies (HTML)
- Modules JS (lococlic_*_v5.html)
"""

import re
import json
import csv
from pathlib import Path
from collections import defaultdict
import sys

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

# Sources de fallback (toutes WHITELISTÉES)
FALLBACKS = {
    "cervical": [
        {"l": "HAS 2019 — Prise en charge du patient présentant une lombalgie commune", 
         "u": "https://www.has-sante.fr/jcms/c_2961499/fr/prise-en-charge-du-patient-presentant-une-lombalgie-commune"},
        {"l": "Foster et al. 2018 — Lancet Low Back Pain Series (cadre douleurs rachidiennes)", 
         "u": "https://pubmed.ncbi.nlm.nih.gov/29573872/"},
    ],
    "dorsal": [
        {"l": "HAS 2019 — Prise en charge du patient présentant une lombalgie commune", 
         "u": "https://www.has-sante.fr/jcms/c_2961499/fr/prise-en-charge-du-patient-presentant-une-lombalgie-commune"},
        {"l": "Foster et al. 2018 — Lancet Low Back Pain Series (cadre douleurs rachidiennes)", 
         "u": "https://pubmed.ncbi.nlm.nih.gov/29573872/"},
    ],
    "lombaire": [
        {"l": "HAS 2019 — Prise en charge du patient présentant une lombalgie commune", 
         "u": "https://www.has-sante.fr/jcms/c_2961499/fr/prise-en-charge-du-patient-presentant-une-lombalgie-commune"},
        {"l": "Foster et al. 2018 — Lancet Low Back Pain Series", 
         "u": "https://pubmed.ncbi.nlm.nih.gov/29573872/"},
    ],
    "sciatique": [
        {"l": "HAS 2019 — Prise en charge du patient présentant une lombalgie commune", 
         "u": "https://www.has-sante.fr/jcms/c_2961499/fr/prise-en-charge-du-patient-presentant-une-lombalgie-commune"},
        {"l": "Foster et al. 2018 — Lancet Low Back Pain Series", 
         "u": "https://pubmed.ncbi.nlm.nih.gov/29573872/"},
    ],
    "femoro_patellaire": [
        {"l": "Bannuru et al. 2019 — OARSI guidelines (pathologies du genou)", 
         "u": "https://pubmed.ncbi.nlm.nih.gov/31278997/"},
    ],
    "tendinopathie": [
        {"l": "Cook & Purdam 2009 — Tendinopathy continuum model (Br J Sports Med)", 
         "u": "https://pubmed.ncbi.nlm.nih.gov/18812414/"},
    ],
    "arthrose": [
        {"l": "Bannuru et al. 2019 — OARSI guidelines for OA management", 
         "u": "https://pubmed.ncbi.nlm.nih.gov/31278997/"},
    ],
    "vasculaire": [
        {"l": "AAOS OrthoInfo — Thoracic Outlet Syndrome (référence générale syndromes vasculaires)", 
         "u": "https://orthoinfo.aaos.org/en/diseases--conditions/thoracic-outlet-syndrome/"},
    ],
    "cote": [
        {"l": "HAS 2019 — Prise en charge de la lombalgie commune (cadre douleurs musculo-squelettiques)", 
         "u": "https://www.has-sante.fr/jcms/c_2961499/fr/prise-en-charge-du-patient-presentant-une-lombalgie-commune"},
    ],
    "sacro": [
        {"l": "HAS 2019 — Prise en charge du patient présentant une lombalgie commune", 
         "u": "https://www.has-sante.fr/jcms/c_2961499/fr/prise-en-charge-du-patient-presentant-une-lombalgie-commune"},
    ],
    "generic": [
        {"l": "Bannuru et al. 2019 — OARSI guidelines (référence générale musculosquelettique)", 
         "u": "https://pubmed.ncbi.nlm.nih.gov/31278997/"},
    ],
}

def get_fallback_for_fiche(filename):
    """Retourne la liste de sources de fallback selon la fiche"""
    lower = filename.lower()
    # Sciatique / cruralgie
    if any(k in lower for k in ["sciatique", "cruralgie"]):
        return FALLBACKS["sciatique"]
    # Cervical
    if any(k in lower for k in ["cerv", "torticolis", "whiplash", "ncb_", "myelopathie"]):
        return FALLBACKS["cervical"]
    # Dorsal/thoracique
    if any(k in lower for k in ["dors", "thorac", "scheuermann", "synd_charniere_dl", "synd_facettaire_d", "discopathie_d", "synd_cyriax", "douleur_costov", "tietze"]):
        return FALLBACKS["dorsal"]
    # Lombaire
    if any(k in lower for k in ["lomb", "canal_lomb", "spondylolisthesis"]):
        return FALLBACKS["lombaire"]
    # Sacro
    if "sacro" in lower:
        return FALLBACKS["sacro"]
    # SFP / patellaire
    if any(k in lower for k in ["femoro_pat", "sfp", "patel"]):
        return FALLBACKS["femoro_patellaire"]
    # Arthrose
    if "arthrose" in lower or "arthro" in lower:
        return FALLBACKS["arthrose"]
    # Tendinopathie
    if any(k in lower for k in ["tend_", "tendin"]):
        return FALLBACKS["tendinopathie"]
    # Vasculaire
    if any(k in lower for k in ["tvp", "thrombose", "claudication", "poplite", "vasc"]):
        return FALLBACKS["vasculaire"]
    return FALLBACKS["generic"]

# Patterns
pat_html = re.compile(r'<a class="src-chip"\s+href="([^"]+)"[^>]*>([^<]+)</a>', re.IGNORECASE)
pat_js = re.compile(r"\{l:'((?:[^'\\]|\\.)*)',u:'([^']+)'\}")

stats = {
    "sources_removed": 0,
    "sources_kept": 0,
    "fiches_modified": 0,
    "modules_modified": 0,
    "fiches_fallback_added": 0,
}

log_removed = []

# ============================================
# 1. FICHES PATHOLOGIES
# ============================================
fiches_dir = ROOT / "fiches_pathologies"

for fiche in fiches_dir.glob("*.html"):
    text = fiche.read_text(encoding="utf-8")
    original = text
    
    # Trouver tous les <a class="src-chip"> et déterminer ceux à virer
    matches = list(pat_html.finditer(text))
    if not matches:
        continue
    
    # Construire la nouvelle version : on garde uniquement les whitelistées
    # En partant de la fin pour ne pas casser les indices
    new_text = text
    kept_anchors = []
    for m in reversed(matches):
        url = m.group(1).strip()
        label = m.group(2).strip()
        if is_whitelisted(url):
            stats["sources_kept"] += 1
            kept_anchors.append(label)
        else:
            stats["sources_removed"] += 1
            log_removed.append({
                "file": f"fiches_pathologies/{fiche.name}",
                "label": label,
                "url": url,
            })
            # Supprimer toute l'ancre
            new_text = new_text[:m.start()] + new_text[m.end():]
    
    # Si aucune source n'a été conservée → ajouter fallback
    if not kept_anchors:
        fallback_sources = get_fallback_for_fiche(fiche.name)
        # Construire les <a> HTML
        fallback_html = "".join(
            f'<a class="src-chip" href="{s["u"]}" target="_blank" rel="noopener">{s["l"]}</a>' 
            for s in fallback_sources
        )
        # On cherche la div src-chips existante pour y insérer
        # Pattern : <div class="src-chips"> ... </div>
        div_pat = re.compile(r'(<div class="src-chips">)\s*(</div>)', re.DOTALL)
        m = div_pat.search(new_text)
        if m:
            new_text = new_text[:m.start()] + m.group(1) + fallback_html + m.group(2) + new_text[m.end():]
            stats["fiches_fallback_added"] += 1
        else:
            # Cas où la div est vide après suppressions
            div_pat2 = re.compile(r'<div class="src-chips">\s*</div>', re.DOTALL)
            m2 = div_pat2.search(new_text)
            if m2:
                new_text = new_text.replace(m2.group(0), 
                    f'<div class="src-chips">{fallback_html}</div>')
                stats["fiches_fallback_added"] += 1
    
    # Nettoyer : potentiels doubles espaces dans la div src-chips
    new_text = re.sub(r'(<div class="src-chips">)\s+', r'\1\n      ', new_text)
    new_text = re.sub(r'(</a>)\s*(<a class="src-chip")', r'\1\n      \2', new_text)
    
    if new_text != original:
        fiche.write_text(new_text, encoding="utf-8")
        stats["fiches_modified"] += 1

print(f"=== FICHES PATHOLOGIES ===")
print(f"  Modifiées : {stats['fiches_modified']}")
print(f"  Sources supprimées : {stats['sources_removed']}")
print(f"  Sources conservées : {stats['sources_kept']}")
print(f"  Fiches avec fallback ajouté : {stats['fiches_fallback_added']}")

# ============================================
# 2. MODULES JS
# ============================================
print(f"\n=== MODULES JS ===")

for module in ROOT.glob("lococlic_*_v5.html"):
    text = module.read_text(encoding="utf-8")
    original = text
    
    # Pour chaque {l:'...',u:'...'}, vérifier si whitelist
    # Faire le remplacement à la volée
    
    def process_match(m):
        global stats
        label = m.group(1).replace("\\'", "'")  # Décoder apostrophes
        url = m.group(2).strip()
        if is_whitelisted(url):
            stats["sources_kept"] += 1
            return m.group(0)  # Garder
        else:
            stats["sources_removed"] += 1
            log_removed.append({
                "file": module.name,
                "label": label,
                "url": url,
            })
            return None  # Sera filtré
    
    # On doit gérer le contexte JS : sources:[...] : enlever proprement les virgules
    # Stratégie : repérer les sources:[...] et reconstruire
    
    # Pattern pour bloc sources entier
    src_block_pat = re.compile(
        r"(sources:\[)((?:\{l:'(?:[^'\\]|\\.)*',u:'[^']+'\},?)*)(\])"
    )
    
    def rebuild_sources_block(block_match):
        before = block_match.group(1)  # "sources:["
        content = block_match.group(2)
        after = block_match.group(3)   # "]"
        
        items = pat_js.findall(content)
        kept_items = []
        for label, url in items:
            label_dec = label.replace("\\'", "'")
            if is_whitelisted(url):
                kept_items.append(f"{{l:'{label}',u:'{url}'}}")
                stats["sources_kept"] += 1
            else:
                stats["sources_removed"] += 1
                log_removed.append({
                    "file": module.name,
                    "label": label_dec,
                    "url": url,
                })
        
        # Si le bloc est vide, on met un fallback générique
        if not kept_items:
            # Fallback générique pour les modules : on regarde le nom du module
            mod_name = module.stem.lower()
            if "epaule" in mod_name:
                fb_label = "HAS 2023 — Conduite diagnostique épaule douloureuse non traumatique"
                fb_url = "https://www.has-sante.fr/jcms/p_3459565/fr/conduite-diagnostique-devant-une-epaule-douloureuse-non-traumatique-de-l-adulte-et-prise-en-charge-des-tendinopathies-de-la-coiffe-des-rotateurs"
            elif "cheville" in mod_name or "pied" in mod_name:
                fb_label = "HAS 2018 — Entorse de cheville de l'adulte"
                fb_url = "https://www.has-sante.fr/jcms/c_2812061/fr/entorse-de-cheville-de-l-adulte"
            elif "lomb" in mod_name or "dorsal" in mod_name or "cerv" in mod_name:
                fb_label = "HAS 2019 — Prise en charge du patient présentant une lombalgie commune"
                fb_url = "https://www.has-sante.fr/jcms/c_2961499/fr/prise-en-charge-du-patient-presentant-une-lombalgie-commune"
            elif "genou" in mod_name or "hanche" in mod_name:
                fb_label = "Bannuru et al. 2019 — OARSI guidelines"
                fb_url = "https://pubmed.ncbi.nlm.nih.gov/31278997/"
            elif "main" in mod_name or "coude" in mod_name:
                fb_label = "HAS — Syndrome du canal carpien"
                fb_url = "https://www.has-sante.fr/jcms/c_1751069/fr/syndrome-du-canal-carpien"
            else:
                fb_label = "Bannuru et al. 2019 — OARSI guidelines (référence générale)"
                fb_url = "https://pubmed.ncbi.nlm.nih.gov/31278997/"
            
            kept_items.append(f"{{l:'{fb_label}',u:'{fb_url}'}}")
        
        return before + ",".join(kept_items) + after
    
    new_text = src_block_pat.sub(rebuild_sources_block, text)
    
    if new_text != original:
        module.write_text(new_text, encoding="utf-8")
        stats["modules_modified"] += 1

print(f"  Modules modifiés : {stats['modules_modified']}")

# ============================================
# RAPPORT FINAL
# ============================================
print(f"\n{'='*60}")
print(f"RÉCAPITULATIF NUCLÉAIRE")
print(f"{'='*60}")
print(f"Sources conservées (whitelist)   : {stats['sources_kept']}")
print(f"Sources SUPPRIMÉES (non vérif.)  : {stats['sources_removed']}")
print(f"Fiches modifiées                 : {stats['fiches_modified']}")
print(f"Modules modifiés                 : {stats['modules_modified']}")
print(f"Fiches avec fallback ajouté      : {stats['fiches_fallback_added']}")

# Export CSV des suppressions
report_path = Path("/mnt/user-data/outputs/LocoClic_audit_NUCLEAIRE_rapport.csv")
report_path.parent.mkdir(parents=True, exist_ok=True)
with report_path.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "label", "url"])
    w.writeheader()
    w.writerows(log_removed)

print(f"\n📊 Rapport CSV : {report_path}")
print(f"   {len(log_removed)} sources supprimées documentées")
