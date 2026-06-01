#!/usr/bin/env python3
"""
Injecte le disclaimer médico-légal et le footer juridique dans toutes les pages HTML du site LocoClic.

Comportement :
- Pages racine (index, login, lococlic_*_v5) : disclaimer + footer juste avant </body>
- Fiches pathologies (fiches_pathologies/) : footer seul (un disclaimer existe déjà)
- Fiches patient (lococlic_fiches_patient/) : footer seul
- Pages légales (mentions-legales, confidentialite, cgu) : ignorées (footer déjà intégré)

Idempotent : si déjà injecté, ne ré-injecte pas (cherche le marqueur).
"""

import os
import re
from pathlib import Path

# Marqueur pour idempotence
MARKER = "<!-- LOCOCLIC-LEGAL-INJECTED -->"

# Bandeau disclaimer médico-légal complet
DISCLAIMER_FULL = """
<!-- LOCOCLIC-LEGAL-INJECTED -->
<style>
  .lococlic-medical-disclaimer {
    background: #fef3c7;
    border-left: 4px solid #f59e0b;
    color: #92400e;
    padding: 14px 20px;
    margin: 20px;
    border-radius: 0 8px 8px 0;
    font-size: 13px;
    line-height: 1.6;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    max-width: 1100px;
    margin-left: auto;
    margin-right: auto;
  }
  .lococlic-medical-disclaimer strong { color: #78350f; display: block; margin-bottom: 4px; }
  .lococlic-medical-disclaimer a { color: #92400e; text-decoration: underline; font-weight: 700; }
  .lococlic-footer {
    background: #1e3a5f;
    color: rgba(255,255,255,0.85);
    padding: 24px 32px;
    text-align: center;
    font-size: 13px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin-top: 32px;
  }
  .lococlic-footer nav a {
    color: rgba(255,255,255,0.85);
    text-decoration: none;
    margin: 0 12px;
    font-weight: 500;
    transition: color 0.2s;
  }
  .lococlic-footer nav a:hover { color: #10b981; }
  .lococlic-footer .copyright { margin-top: 12px; opacity: 0.7; font-size: 12px; }
  @media (max-width: 640px) {
    .lococlic-medical-disclaimer { font-size: 12px; padding: 12px 14px; margin: 14px; }
    .lococlic-footer { padding: 20px 16px; }
    .lococlic-footer nav a { display: inline-block; margin: 4px 8px; font-size: 12px; }
  }
</style>
<div class="lococlic-medical-disclaimer">
  <strong>⚠️ Outil d'aide à la décision pédagogique réservé aux professionnels de santé.</strong>
  LocoClic n'est pas un dispositif médical. Il ne remplace ni l'examen clinique ni le jugement médical du praticien. La responsabilité du diagnostic, du traitement et de l'orientation du patient appartient exclusivement au médecin utilisateur.
  <a href="/cgu.html">Voir les CGU</a>
</div>
<footer class="lococlic-footer">
  <nav>
    <a href="/">Accueil</a>
    <a href="/mentions-legales.html">Mentions légales</a>
    <a href="/confidentialite.html">Confidentialité</a>
    <a href="/cgu.html">CGU</a>
    <a href="mailto:contact@lococlic.com">Contact</a>
  </nav>
  <div class="copyright">© 2026 LocoClic™ — Tous droits réservés. Marque déposée à l'INPI.</div>
</footer>
"""

# Version légère : footer seul (pour fiches qui ont déjà un disclaimer)
FOOTER_ONLY = """
<!-- LOCOCLIC-LEGAL-INJECTED -->
<style>
  .lococlic-footer {
    background: #1e3a5f;
    color: rgba(255,255,255,0.85);
    padding: 20px 24px;
    text-align: center;
    font-size: 13px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin-top: 24px;
  }
  .lococlic-footer nav a {
    color: rgba(255,255,255,0.85);
    text-decoration: none;
    margin: 0 12px;
    font-weight: 500;
    transition: color 0.2s;
  }
  .lococlic-footer nav a:hover { color: #10b981; }
  .lococlic-footer .copyright { margin-top: 10px; opacity: 0.7; font-size: 12px; }
  @media print {
    .lococlic-footer { display: none; }
  }
  @media (max-width: 640px) {
    .lococlic-footer { padding: 16px; }
    .lococlic-footer nav a { display: inline-block; margin: 4px 8px; font-size: 12px; }
  }
</style>
<footer class="lococlic-footer">
  <nav>
    <a href="/">Accueil</a>
    <a href="/mentions-legales.html">Mentions légales</a>
    <a href="/confidentialite.html">Confidentialité</a>
    <a href="/cgu.html">CGU</a>
    <a href="mailto:contact@lococlic.com">Contact</a>
  </nav>
  <div class="copyright">© 2026 LocoClic™ — Tous droits réservés. Marque déposée à l'INPI.</div>
</footer>
"""

# Pages à ignorer (déjà conformes ou cas spéciaux)
SKIP_FILES = {
    "mentions-legales.html",
    "confidentialite.html",
    "cgu.html",
}


def inject(file_path: Path, content_to_inject: str) -> str:
    """Injecte content_to_inject juste avant </body>. Idempotent.
    Retourne 'injected', 'already_injected', ou 'no_body_tag'."""
    text = file_path.read_text(encoding="utf-8")
    
    # Idempotence : si déjà injecté, on ignore
    if MARKER in text:
        return "already_injected"
    
    # Chercher </body> (avec ou sans espaces autour)
    pattern = re.compile(r"</body>", re.IGNORECASE)
    if not pattern.search(text):
        return "no_body_tag"
    
    new_text = pattern.sub(content_to_inject + "\n</body>", text, count=1)
    file_path.write_text(new_text, encoding="utf-8")
    return "injected"


def main():
    root = Path(__file__).parent.resolve()
    
    stats = {
        "injected_full": 0,
        "injected_footer": 0,
        "already_done": 0,
        "page_legale": 0,
        "no_body": 0,
    }
    no_body_files = []
    
    # 1. Pages racine (index, login, modules lococlic_*_v5)
    print("\n=== Pages racine ===")
    for html_file in sorted(root.glob("*.html")):
        if html_file.name in SKIP_FILES:
            print(f"  ⏭️  {html_file.name} (page légale)")
            stats["page_legale"] += 1
            continue
        result = inject(html_file, DISCLAIMER_FULL)
        if result == "injected":
            print(f"  ✅ {html_file.name}")
            stats["injected_full"] += 1
        elif result == "already_injected":
            print(f"  ⏭️  {html_file.name} (déjà fait)")
            stats["already_done"] += 1
        else:
            print(f"  ⚠️  {html_file.name} (pas de </body>)")
            stats["no_body"] += 1
            no_body_files.append(str(html_file.relative_to(root)))
    
    # 2. Fiches pathologies → footer seul
    fiches_path = root / "fiches_pathologies"
    if fiches_path.exists():
        total = len(list(fiches_path.glob("*.html")))
        print(f"\n=== Fiches pathologies ({total} fichiers) ===")
        new_count = 0
        for html_file in fiches_path.glob("*.html"):
            result = inject(html_file, FOOTER_ONLY)
            if result == "injected":
                stats["injected_footer"] += 1
                new_count += 1
            elif result == "already_injected":
                stats["already_done"] += 1
            else:
                stats["no_body"] += 1
                no_body_files.append(str(html_file.relative_to(root)))
        print(f"  ✅ {new_count} nouveaux fichiers traités ({total - new_count} déjà à jour)")
    
    # 3. Fiches patient → footer seul
    patient_path = root / "lococlic_fiches_patient"
    if patient_path.exists():
        total = len(list(patient_path.glob("*.html")))
        print(f"\n=== Fiches patient ({total} fichiers) ===")
        new_count = 0
        for html_file in patient_path.glob("*.html"):
            result = inject(html_file, FOOTER_ONLY)
            if result == "injected":
                stats["injected_footer"] += 1
                new_count += 1
            elif result == "already_injected":
                stats["already_done"] += 1
            else:
                stats["no_body"] += 1
                no_body_files.append(str(html_file.relative_to(root)))
        print(f"  ✅ {new_count} nouveaux fichiers traités ({total - new_count} déjà à jour)")
    
    # Récap
    total_new = stats["injected_full"] + stats["injected_footer"]
    print()
    print("=" * 56)
    print("RÉCAPITULATIF")
    print("=" * 56)
    print(f"✅ Disclaimer + footer ajoutés (cette exécution) : {stats['injected_full']:>4}")
    print(f"✅ Footer seul ajouté (cette exécution)         : {stats['injected_footer']:>4}")
    print(f"⏭️  Déjà à jour (rien fait)                      : {stats['already_done']:>4}")
    print(f"⏭️  Pages légales (ignorées)                     : {stats['page_legale']:>4}")
    if stats["no_body"]:
        print(f"⚠️  Fichiers sans </body> (signaler à Claude)    : {stats['no_body']:>4}")
        for f in no_body_files:
            print(f"     - {f}")
    print()
    if total_new > 0:
        print(f"🎉 {total_new} fichiers modifiés. Pense à commit + push sur GitHub Desktop.")
    else:
        print("ℹ️  Aucune modification nécessaire. Tout est déjà à jour.")
    print()


if __name__ == "__main__":
    main()
