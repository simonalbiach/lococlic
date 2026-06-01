"""
Passe complémentaire : remplacer tous les LocoClic résiduels via regex,
en préservant les classes CSS et noms de fichiers.
"""
import re
from pathlib import Path

ROOT = Path("/home/claude/lococlic_site_final")

# Regex : LocoClic qui n'est PAS dans une classe/attr/path/identifier
# - Pas précédé par : a-z A-Z 0-9 - _ / " = (donc pas dans class="lococlic-..." ou path)
# - Pas suivi par : a-z A-Z 0-9 - _ (donc pas Lococlicien, LocoClic-medical, etc.)
# Mais OK suivi par ™, ., ,, ;, espace, <, etc.

PATTERN = re.compile(r'(?<![a-zA-Z0-9\-_/"=])LocoClic(?![a-zA-Z0-9\-_])')

TM = "<sup>™</sup>"

# Contextes où le ™ avec <sup> ne fonctionne PAS (attributs HTML qui n'acceptent pas de balises)
# alt="..." content="..." title="..." → ™ simple sans balise

# Stratégie : pour chaque match, vérifier si on est dans un attribut
# Plus simple : faire d'abord remplacement attributs, puis le reste

stats = {"files_modified": 0, "replacements_text": 0, "replacements_attr": 0}

def process_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    original = text
    
    # 1. Attributs : remplacer LocoClic par lococlic (sans ™ HTML) dans alt/content/title
    #    On gère les guillemets simples et doubles
    # Pattern : un attr nom="..." qui contient LocoClic
    def replace_in_attr(m):
        full = m.group(0)
        # Remplacer LocoClic par lococlic dans le contenu de l'attribut
        attr_value = m.group(1)
        new_value = re.sub(r'\bLocoClic\b', 'lococlic™', attr_value)
        stats["replacements_attr"] += attr_value.count("LocoClic")
        return full.replace(attr_value, new_value)
    
    text = re.sub(r'(?:alt|title|content)="([^"]*LocoClic[^"]*)"', replace_in_attr, text)
    text = re.sub(r"(?:alt|title|content)='([^']*LocoClic[^']*)'", replace_in_attr, text)
    
    # 2. Texte visible : LocoClic → lococlic<sup>™</sup>
    def replace_text(m):
        stats["replacements_text"] += 1
        return f'lococlic{TM}'
    
    text = PATTERN.sub(replace_text, text)
    
    if text != original:
        filepath.write_text(text, encoding="utf-8")
        stats["files_modified"] += 1
        return True
    return False

# Traiter tous les HTML
total_files = 0
for html_path in list(ROOT.glob("*.html")) + \
                 list((ROOT / "fiches_pathologies").glob("*.html")) + \
                 list((ROOT / "lococlic_fiches_patient").glob("*.html")):
    if process_file(html_path):
        total_files += 1

print(f"=== PASSE COMPLÉMENTAIRE ===")
print(f"Fichiers modifiés : {stats['files_modified']}")
print(f"Remplacements (texte) : {stats['replacements_text']}")
print(f"Remplacements (attributs) : {stats['replacements_attr']}")
print(f"Total : {stats['replacements_text'] + stats['replacements_attr']}")
