#!/usr/bin/env python3
"""
Script de corrections LocoClic — 3 modifications :

1. Inversion bird-dog / bracing dans lombaire_08_lumbago_aigu.html
   → Le bracing étant plus simple que le bird-dog, l'encart "essayez plus simple"
     est en réalité une PROGRESSION → on change le titre de l'encart.

2. Remplacement "DEXA" → "DMO" (Densitométrie Minérale Osseuse)
   → Plus à jour terminologiquement et plus français.

3. Ajout d'un encart "🚩 Drapeaux rouges" sur les fiches pathologies du rachis
   (cervical, dorsal, lombaire) qui n'en ont pas encore.

Idempotent : peut être relancé sans casser.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
FICHES_PATHO = ROOT / "fiches_pathologies"
FICHES_PATIENT = ROOT / "lococlic_fiches_patient"

# ============================================================
# CORRECTION 1 : Bird-dog / Bracing
# ============================================================

def fix_birddog_bracing():
    """Dans lombaire_08_lumbago_aigu.html, le bracing est l'exo principal et le
    bird-dog est dans l'encart 'essayez plus simple' — alors que c'est l'inverse.
    On corrige le titre de l'encart en 'progression'."""
    
    file = FICHES_PATIENT / "lombaire_08_lumbago_aigu.html"
    if not file.exists():
        return "(fichier non trouvé)"
    
    text = file.read_text(encoding="utf-8")
    
    # Le pattern problématique
    old_title = '<div class="alternative-title">💡 Vous n\'y arrivez pas ? Essayez plus simple :</div>\n          <div class="alternative-name">Stabilisation lombaire (Bird-dog) — quand vous allez mieux</div>'
    
    new_title = '<div class="alternative-title">📈 Quand vous allez mieux, progressez vers :</div>\n          <div class="alternative-name">Stabilisation lombaire (Bird-dog)</div>'
    
    if old_title in text:
        text = text.replace(old_title, new_title)
        file.write_text(text, encoding="utf-8")
        return "✅ corrigé"
    elif new_title in text:
        return "⏭️  déjà corrigé"
    else:
        # Tentative de match plus souple
        pattern_bracing_bird = re.search(
            r'<div class="alternative-title">[^<]*Vous n\'y arrivez pas[^<]*</div>\s*<div class="alternative-name">Stabilisation lombaire \(Bird-dog\)[^<]*</div>',
            text, re.DOTALL
        )
        if pattern_bracing_bird:
            old = pattern_bracing_bird.group(0)
            new = '<div class="alternative-title">📈 Quand vous allez mieux, progressez vers :</div>\n          <div class="alternative-name">Stabilisation lombaire (Bird-dog)</div>'
            text = text.replace(old, new)
            file.write_text(text, encoding="utf-8")
            return "✅ corrigé (match souple)"
        return "⚠️  pattern introuvable"


# ============================================================
# CORRECTION 2 : DEXA → DMO
# ============================================================

def fix_dexa_to_dmo():
    """Remplace 'DEXA' par 'DMO' dans tout le site.
    Conserve uniquement la mention parenthétique 'Densitométrie Minérale Osseuse'
    là où le contexte le permet."""
    
    files_modified = []
    
    # Toutes les pages HTML du site
    all_html = (
        list(ROOT.glob("*.html"))
        + list(FICHES_PATHO.glob("*.html"))
        + list(FICHES_PATIENT.glob("*.html"))
    )
    
    for file in all_html:
        text = file.read_text(encoding="utf-8")
        original = text
        
        # Cas 1 : "DEXA (densitométrie osseuse)" → "DMO (densitométrie minérale osseuse)"
        text = text.replace(
            "DEXA (densitométrie osseuse)",
            "DMO (densitométrie minérale osseuse)"
        )
        # Cas 2 : "DEXA, calcémie" → "DMO, calcémie" (contexte bilan)
        text = text.replace("DEXA, calcémie", "DMO, calcémie")
        text = text.replace("DEXA, vitamine D", "DMO, vitamine D")
        
        # Cas 3 : "DEXA" tout court (mot entier, pas dans un mot)
        # Attention : DEXA en majuscules → DMO, pas dexa en minuscules
        text = re.sub(r'\bDEXA\b', 'DMO', text)
        text = re.sub(r'\bDexa\b', 'DMO', text)
        # Pas de remplacement de "dexa" minuscule (peut être dans un code, etc.)
        
        if text != original:
            file.write_text(text, encoding="utf-8")
            files_modified.append(file.name)
    
    return files_modified


# ============================================================
# CORRECTION 3 : Encart drapeaux rouges sur fiches rachis
# ============================================================

RED_FLAGS_CERVICAL = """
    <div class="red-flags-banner">
      <div class="rf-title">🚩 Drapeaux rouges — Recherche systématique</div>
      <div class="rf-content">
        <div class="rf-section">
          <strong>Néoplasiques / Infectieux</strong>
          <ul>
            <li>Antécédent de cancer (sein, poumon, prostate, rein, thyroïde)</li>
            <li>Altération de l'état général, perte de poids inexpliquée</li>
            <li>Fièvre, immunodépression, toxicomanie IV</li>
            <li>Douleur nocturne non mécanique, non soulagée par le repos</li>
          </ul>
        </div>
        <div class="rf-section">
          <strong>Neurologiques (urgents)</strong>
          <ul>
            <li>Déficit moteur des membres supérieurs ou inférieurs</li>
            <li>Signes médullaires (syndrome pyramidal, Hoffmann, Babinski)</li>
            <li>Troubles sphinctériens, anesthésie en selle</li>
            <li>Névralgie cervico-brachiale déficitaire (parésie)</li>
          </ul>
        </div>
        <div class="rf-section">
          <strong>Traumatiques / Vasculaires</strong>
          <ul>
            <li>Traumatisme cervical à haute énergie</li>
            <li>Céphalée brutale + cervicalgie (dissection vertébrale, HSA)</li>
            <li>Vertiges, troubles visuels, dysarthrie (vertébro-basilaire)</li>
          </ul>
        </div>
        <div class="rf-section">
          <strong>Rhumatologiques</strong>
          <ul>
            <li>Raideur matinale > 60 min, réveil nocturne 2<sup>e</sup> partie de nuit (spondylarthrite)</li>
            <li>Polyarthrite rhumatoïde connue (instabilité C1-C2)</li>
          </ul>
        </div>
      </div>
      <div class="rf-footer">⚠️ La présence d'un seul de ces signes impose une exploration urgente.</div>
    </div>
"""

RED_FLAGS_DORSAL = """
    <div class="red-flags-banner">
      <div class="rf-title">🚩 Drapeaux rouges — Recherche systématique</div>
      <div class="rf-content">
        <div class="rf-section">
          <strong>Néoplasiques / Infectieux</strong>
          <ul>
            <li>Antécédent de cancer (rachis dorsal = site métastatique fréquent)</li>
            <li>Altération de l'état général, perte de poids, fièvre</li>
            <li>Douleur nocturne, non mécanique, non soulagée par repos</li>
            <li>Immunodépression, toxicomanie IV, sepsis</li>
          </ul>
        </div>
        <div class="rf-section">
          <strong>Fracture vertébrale</strong>
          <ul>
            <li>Femme ménopausée, homme > 70 ans</li>
            <li>Corticothérapie au long cours, antécédent de fracture de fragilité</li>
            <li>Perte de taille > 3 cm, cyphose progressive</li>
            <li>Douleur brutale après effort minime (vertèbre tassée)</li>
          </ul>
        </div>
        <div class="rf-section">
          <strong>Neurologiques (urgents)</strong>
          <ul>
            <li>Déficit moteur ou sensitif des membres inférieurs</li>
            <li>Syndrome médullaire, niveau sensitif</li>
            <li>Troubles sphinctériens, anesthésie en selle</li>
          </ul>
        </div>
        <div class="rf-section">
          <strong>Viscérales (douleur projetée)</strong>
          <ul>
            <li>Douleur thoracique d'allure cardiaque (SCA, dissection aortique)</li>
            <li>Pancréatite, ulcère perforé, cholécystite</li>
            <li>Embolie pulmonaire, pleurésie</li>
            <li>Dissection aortique : douleur transfixiante, asymétrie tensionnelle</li>
          </ul>
        </div>
      </div>
      <div class="rf-footer">⚠️ La présence d'un seul de ces signes impose une exploration urgente.</div>
    </div>
"""

RED_FLAGS_LOMBAIRE = """
    <div class="red-flags-banner">
      <div class="rf-title">🚩 Drapeaux rouges — Recherche systématique</div>
      <div class="rf-content">
        <div class="rf-section">
          <strong>Néoplasiques / Infectieux</strong>
          <ul>
            <li>Antécédent de cancer (sein, prostate, poumon, rein, thyroïde, myélome)</li>
            <li>Altération de l'état général, perte de poids inexpliquée</li>
            <li>Fièvre, immunodépression, toxicomanie IV, sepsis</li>
            <li>Douleur nocturne non mécanique, non soulagée par le repos</li>
          </ul>
        </div>
        <div class="rf-section">
          <strong>Neurologiques (urgents)</strong>
          <ul>
            <li>Syndrome de la queue de cheval : anesthésie en selle, troubles sphinctériens, déficit bilatéral</li>
            <li>Déficit moteur installé ou progressif (cotation MRC < 3)</li>
            <li>Sciatique hyperalgique résistante</li>
          </ul>
        </div>
        <div class="rf-section">
          <strong>Fracture vertébrale</strong>
          <ul>
            <li>Femme ménopausée, homme > 70 ans, corticothérapie au long cours</li>
            <li>Antécédent de fracture de fragilité, perte de taille > 3 cm</li>
            <li>Traumatisme même mineur sur terrain ostéoporotique</li>
          </ul>
        </div>
        <div class="rf-section">
          <strong>Rhumatologiques / Vasculaires</strong>
          <ul>
            <li>Spondylarthrite : âge < 45 ans, raideur matinale > 30 min, réveil 2<sup>e</sup> partie de nuit, amélioration à l'effort</li>
            <li>Anévrisme aorte abdominale : douleur lombaire pulsatile, masse battante</li>
            <li>Colique néphrétique, pyélonéphrite, pathologie pelvienne</li>
          </ul>
        </div>
      </div>
      <div class="rf-footer">⚠️ La présence d'un seul de ces signes impose une exploration urgente.</div>
    </div>
"""

# CSS dédié — sera injecté dans le <head> de chaque fiche
RED_FLAGS_CSS = """
<style>
  .red-flags-banner {
    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    border-left: 6px solid #dc2626;
    border-radius: 0 14px 14px 0;
    padding: 22px 26px;
    margin: 24px 0 28px 0;
    box-shadow: 0 4px 14px rgba(220, 38, 38, 0.12);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
  .red-flags-banner .rf-title {
    color: #991b1b;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 14px;
    letter-spacing: -0.2px;
  }
  .red-flags-banner .rf-content {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px 24px;
  }
  .red-flags-banner .rf-section strong {
    display: block;
    color: #7f1d1d;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  .red-flags-banner .rf-section ul {
    margin: 0;
    padding-left: 18px;
    color: #7f1d1d;
    font-size: 13px;
    line-height: 1.55;
  }
  .red-flags-banner .rf-section li {
    margin-bottom: 3px;
  }
  .red-flags-banner .rf-footer {
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px dashed rgba(220, 38, 38, 0.3);
    color: #991b1b;
    font-size: 12px;
    font-weight: 600;
    font-style: italic;
  }
  @media (max-width: 700px) {
    .red-flags-banner { padding: 18px 18px; margin: 18px 0 22px 0; }
    .red-flags-banner .rf-content { grid-template-columns: 1fr; gap: 12px; }
    .red-flags-banner .rf-section ul { font-size: 12px; }
  }
  @media print {
    .red-flags-banner { 
      page-break-inside: avoid; 
      background: #fef2f2 !important;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
  }
</style>
"""

RED_FLAGS_MARKER = "<!-- LOCOCLIC-REDFLAGS-INJECTED -->"

# Classification des fiches rachis
CERVICAL_FILES = [
    "arthrose_cerv_cervicarthrose_uncarthrose_discarthrose.html",
    "cerv_chronique_cervicalgie_chronique.html",
    "cerv_commune_cervicalgie_commune_aigue.html",
    "myelopathie_cerv_myelopathie_cervicarthrosique_a_depister.html",
    "ncb_nevralgie_cervico_brachiale_ncb.html",
    "spondylarthrite_c_atteinte_cervicale_d_une_spondylarthrite_a_depister.html",
    "synd_facettaire_c_syndrome_facettaire_cervical.html",
    "torticolis_aigu_torticolis_aigu_contracture.html",
    "whiplash_whiplash_coup_du_lapin_cervicalgie_post_traumatique.html",
]

DORSAL_FILES = [
    "discopathie_d_discopathie_dorsale.html",
    "dors_chronique_dorsalgie_chronique_incluant_posture_sedentaire.html",
    "dors_commune_dorsalgie_commune_mecanique.html",
    "douleur_costovertebrale_douleur_costo_vertebrale_blocage_costal.html",
    "fract_vertebre_osteop_fracture_vertebrale_osteoporotique.html",
    "scheuermann_maladie_de_scheuermann_cyphose_juvenile.html",
    "spondylarthrite_d_atteinte_dorsale_d_une_spondylarthrite_a_depister.html",
    "synd_charniere_dl_syndrome_de_la_charniere_dorso_lombaire_maigne.html",
    "synd_cyriax_syndrome_de_cyriax_slipping_rib_syndrome.html",
    "synd_facettaire_d_syndrome_articulaire_posterieur_dorsal.html",
    "tietze_syndrome_de_tietze.html",
]

LOMBAIRE_FILES = [
    "canal_lombaire_canal_lombaire_etroit.html",
    "cruralgie_cruralgie_radiculalgie_l3_ou_l4.html",
    "lomb_chronique_lombalgie_chronique.html",
    "lomb_commune_lombalgie_commune_aigue.html",
    "lumbago_aigu_lumbago_aigu_contracture.html",
    "sacro_iliaque_dysfonction_sacro_iliaque.html",
    "sacro_iliaque_sacro_iliaque_mecanique.html",
    "sciatique_lombo_sciatique_radiculalgie_l5_ou_s1.html",
    "spondylolisthesis_spondylolisthesis.html",
]


def inject_red_flags(filename: str, banner_html: str) -> str:
    """Injecte l'encart drapeaux rouges en haut du <main> de la fiche."""
    file = FICHES_PATHO / filename
    if not file.exists():
        return "❌ fichier introuvable"
    
    text = file.read_text(encoding="utf-8")
    
    # Idempotence
    if RED_FLAGS_MARKER in text:
        return "⏭️  déjà injecté"
    
    # 1. Injecter le CSS dans le <head>
    if "</head>" in text:
        text = text.replace("</head>", RED_FLAGS_CSS + "\n</head>", 1)
    
    # 2. Injecter le banner après l'ouverture de <main class="main-content">
    main_pattern = re.compile(r'(<main class="main-content">)', re.IGNORECASE)
    if main_pattern.search(text):
        full_banner = f"\n{RED_FLAGS_MARKER}\n{banner_html}\n"
        text = main_pattern.sub(r'\1' + full_banner, text, count=1)
    else:
        return "⚠️  pas de <main class=\"main-content\"> trouvé"
    
    file.write_text(text, encoding="utf-8")
    return "✅ injecté"


# ============================================================
# MAIN
# ============================================================

def main():
    print()
    print("=" * 60)
    print("  Corrections LocoClic")
    print("=" * 60)
    
    # Correction 1
    print("\n[1] Correction Bird-dog / Bracing (lumbago aigu)")
    print(f"    → {fix_birddog_bracing()}")
    
    # Correction 2
    print("\n[2] Remplacement DEXA → DMO")
    modified = fix_dexa_to_dmo()
    if modified:
        for f in modified:
            print(f"    ✅ {f}")
    else:
        print("    ⏭️  aucune occurrence trouvée (déjà remplacé ?)")
    
    # Correction 3
    print("\n[3] Encart drapeaux rouges — fiches CERVICAL")
    for f in CERVICAL_FILES:
        status = inject_red_flags(f, RED_FLAGS_CERVICAL)
        print(f"    {status:30s} {f}")
    
    print("\n[3] Encart drapeaux rouges — fiches DORSAL")
    for f in DORSAL_FILES:
        status = inject_red_flags(f, RED_FLAGS_DORSAL)
        print(f"    {status:30s} {f}")
    
    print("\n[3] Encart drapeaux rouges — fiches LOMBAIRE")
    for f in LOMBAIRE_FILES:
        status = inject_red_flags(f, RED_FLAGS_LOMBAIRE)
        print(f"    {status:30s} {f}")
    
    print()
    print("=" * 60)
    print("  ✅ Toutes les corrections appliquées")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
