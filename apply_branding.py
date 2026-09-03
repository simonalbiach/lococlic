"""
1. Centre la login-card sur login.html (cassé par l'injection disclaimer+footer)
2. Remplace tous les "LocoClic" (texte visible) par "lococlic" + ™ en petit
3. Préserve le hero "LOCOCLIC" en majuscule sur index.html (juste ajout du ™)
4. Ne touche pas aux classes CSS, commentaires, noms de fichiers
"""
import re
from pathlib import Path

ROOT = Path("/home/claude/lococlic_site_final")

# ========================================================
# PARTIE 1 : Fixer le centrage du login
# ========================================================
login_path = ROOT / "login.html"
text = login_path.read_text(encoding="utf-8")

# Stratégie : 
# - Body devient flex-direction: column
# - Wrapper .login-wrapper centre la card horizontalement et verticalement
# - Disclaimer et footer restent en bas naturellement

# Remplacer la règle CSS body
old_body_css = """  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8d 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    color: #1e293b;
    -webkit-font-smoothing: antialiased;
  }"""

new_body_css = """  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8d 100%);
    min-height: 100vh;
    margin: 0;
    padding: 0;
    color: #1e293b;
    -webkit-font-smoothing: antialiased;
    display: flex;
    flex-direction: column;
  }
  
  .login-wrapper {
    flex: 1 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    width: 100%;
  }"""

if old_body_css in text:
    text = text.replace(old_body_css, new_body_css)
    print("✅ Login body CSS refactorisé")
else:
    print("⚠️ CSS body de login.html non trouvé tel quel — patch manuel")

# Envelopper la .login-card dans un .login-wrapper
old_login_open = '<body>\n\n<div class="login-card">'
new_login_open = '<body>\n\n<div class="login-wrapper">\n<div class="login-card">'

if old_login_open in text:
    text = text.replace(old_login_open, new_login_open)
    print("✅ login-card enveloppée dans login-wrapper (ouverture)")

# Et fermer le wrapper après la card
# La card se ferme avant `<script>`. On insère </div> avant le script
old_close = '</div>\n\n<script>'
new_close = '</div>\n</div>\n\n<script>'

if old_close in text:
    text = text.replace(old_close, new_close)
    print("✅ login-wrapper fermé")

login_path.write_text(text, encoding="utf-8")

# ========================================================
# PARTIE 2 : Remplacements LocoClic → lococlic™ partout
# ========================================================

# Patterns SAFE (texte visible uniquement)
# Le ™ via <sup> rend bien naturellement dans le HTML

TM = "<sup>™</sup>"

# Liste de remplacements ordonnée (du plus spécifique au plus général)
REPLACEMENTS = [
    # Cas spécial INDEX hero : préserver LOCOCLIC mais ajouter ™
    ('<h1 class="hero-brand">LOCOCLIC</h1>', f'<h1 class="hero-brand">LOCOCLIC{TM}</h1>'),
    
    # Brand / logo dans HTML visible (avec balise)
    ('<div class="brand">LocoClic</div>', f'<div class="brand">lococlic{TM}</div>'),
    ('<span class="logo-name">LocoClic</span>', f'<span class="logo-name">lococlic{TM}</span>'),
    ('<h4>LocoClic</h4>', f'<h4>lococlic{TM}</h4>'),
    ('<strong>LocoClic</strong>', f'<strong>lococlic{TM}</strong>'),
    ('<strong>l\'administrateur LocoClic</strong>', f'<strong>l\'administrateur lococlic{TM}</strong>'),
    
    # Titles HTML : ™ simple (pas de balise dans <title>)
    ('<title>LocoClic ', '<title>lococlic™ '),
    ('<title>LocoClic—', '<title>lococlic™—'),
    
    # Attributs : remplacement simple sans ™ (impossible dans alt/content)
    ('alt="LocoClic"', 'alt="lococlic"'),
    
    # Cas spécifiques copyright + texte
    ('© 2026 LocoClic™', f'© 2026 lococlic{TM}'),
    ('© 2026 LocoClic ', f'© 2026 lococlic{TM} '),
    ('© 2026 LocoClic·', f'© 2026 lococlic{TM}·'),
    
    # Phrases courantes (texte avec ponctuation)
    # On capture l'espace+LocoClic et on insère le sup, puis on garde le suffixe
    (' LocoClic ', f' lococlic{TM} '),
    (' LocoClic.', f' lococlic{TM}.'),
    (' LocoClic,', f' lococlic{TM},'),
    (' LocoClic;', f' lococlic{TM};'),
    (' LocoClic:', f' lococlic{TM}:'),
    (' LocoClic!', f' lococlic{TM}!'),
    (' LocoClic?', f' lococlic{TM}?'),
    (' LocoClic\'', f' lococlic{TM}\''),
    (' LocoClic·', f' lococlic{TM}·'),
    
    # Cas avec — em dash
    ('— LocoClic ', f'— lococlic{TM} '),
    ('— LocoClic.', f'— lococlic{TM}.'),
    
    # Début de phrase juste après une balise
    ('>LocoClic ', f'>lococlic{TM} '),
    ('>LocoClic.', f'>lococlic{TM}.'),
    ('>LocoClic<', f'>lococlic{TM}<'),
    
    # Meta content (description) : texte sans ™ HTML
    ('content="Conditions générales d\'utilisation de LocoClic,', 
     'content="Conditions générales d\'utilisation de lococlic™,'),
    ('content="Mentions légales de LocoClic,',
     'content="Mentions légales de lococlic™,'),
    ('content="Politique de confidentialité et protection des données personnelles de LocoClic.',
     'content="Politique de confidentialité et protection des données personnelles de lococlic™.'),
]

stats = {"files_modified": 0, "replacements_total": 0}

def process_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    original = text
    local_count = 0
    for old, new in REPLACEMENTS:
        if old in text:
            count = text.count(old)
            text = text.replace(old, new)
            local_count += count
    if text != original:
        filepath.write_text(text, encoding="utf-8")
        stats["files_modified"] += 1
        stats["replacements_total"] += local_count
        return local_count
    return 0

# Pages racine
print("\n=== Pages racine ===")
for f in sorted(ROOT.glob("*.html")):
    n = process_file(f)
    if n > 0:
        print(f"  {f.name:50s} {n} remplacements")

# Fiches pathologies
print("\n=== Fiches pathologies ===")
fiches_count = 0
for f in sorted((ROOT / "fiches_pathologies").glob("*.html")):
    n = process_file(f)
    fiches_count += n
print(f"  Total fiches pathologies : {fiches_count} remplacements")

# Fiches patient
print("\n=== Fiches patient ===")
patient_count = 0
patient_dir = ROOT / "lococlic_fiches_patient"
if patient_dir.exists():
    for f in sorted(patient_dir.glob("*.html")):
        n = process_file(f)
        patient_count += n
print(f"  Total fiches patient : {patient_count} remplacements")

print(f"\n{'='*50}")
print(f"BILAN FINAL :")
print(f"  Fichiers modifiés : {stats['files_modified']}")
print(f"  Total remplacements : {stats['replacements_total']}")
