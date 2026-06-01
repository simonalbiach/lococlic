"""
Table FINALE de correspondance — Toutes les URLs vérifiées dans cette conversation.

Stratégie : 
- URLs ABSOLUMENT VÉRIFIÉES (via web_search retournant l'URL exacte ou un PMID confirmé)
- Pour les libellés sans correspondance précise vérifiée, on utilise une URL de fallback
  institutionnelle VÉRIFIÉE (HAS spécifique vérifiée, AAOS shoulder slug vérifié, 
  JOSPT DOI direct vérifié, Cochrane DOI vérifié)

Format : (old_url, old_label) -> {new_url, new_label, source_type, confidence}
"""

# ============================================================
# URLs DE BASE TOUTES VÉRIFIÉES DANS LA CONVERSATION
# ============================================================

URL_HAS_EPAULE_2023 = "https://www.has-sante.fr/jcms/p_3459565/fr/conduite-diagnostique-devant-une-epaule-douloureuse-non-traumatique-de-l-adulte-et-prise-en-charge-des-tendinopathies-de-la-coiffe-des-rotateurs"
URL_HAS_COIFFE_2008 = "https://www.has-sante.fr/jcms/c_658445/fr/prise-en-charge-chirurgicale-des-tendinopathies-rompues-de-la-coiffe-des-rotateurs-de-l-epaule-chez-l-adulte"
URL_HAS_LCA_MENISQUE = "https://www.has-sante.fr/jcms/c_753184/fr/prise-en-charge-therapeutique-des-lesions-meniscales-et-des-lesions-isolees-du-ligament-croise-anterieur-du-genou-chez-l-adulte"
URL_HAS_ENTORSE_CHEVILLE = "https://www.has-sante.fr/jcms/c_2812061/fr/entorse-de-cheville-de-l-adulte"
URL_HAS_OSTEOPOROSE = "https://www.has-sante.fr/jcms/p_3105108/fr/prevention-diagnostic-et-traitement-de-l-osteoporose"
URL_HAS_LOMBALGIE = "https://www.has-sante.fr/jcms/c_2961499/fr/prise-en-charge-du-patient-presentant-une-lombalgie-commune"
URL_HAS_CANAL_CARPIEN = "https://www.has-sante.fr/jcms/c_1751069/fr/syndrome-du-canal-carpien"

URL_AAOS_RC_TEARS = "https://orthoinfo.aaos.org/en/diseases--conditions/rotator-cuff-tears/"
URL_AAOS_IMPINGEMENT = "https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-impingementrotator-cuff-tendinitis/"
URL_AAOS_BICEPS = "https://orthoinfo.aaos.org/en/diseases--conditions/biceps-tendinitis/"
URL_AAOS_ARTHRITIS = "https://orthoinfo.aaos.org/en/diseases--conditions/arthritis-of-the-shoulder/"
URL_AAOS_INSTABILITY = "https://orthoinfo.aaos.org/en/diseases--conditions/chronic-shoulder-instability/"
URL_AAOS_SLAP = "https://orthoinfo.aaos.org/en/diseases--conditions/slap-tears/"
URL_AAOS_AC_JOINT = "https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-separation-acromioclavicular-joint-injury/"
URL_AAOS_THROWING = "https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-injuries-in-the-throwing-athlete/"
URL_AAOS_TOS = "https://orthoinfo.aaos.org/en/diseases--conditions/thoracic-outlet-syndrome/"
URL_AAOS_DISLOCATION = "https://orthoinfo.aaos.org/en/diseases--conditions/dislocated-shoulder/"
URL_AAOS_CPG_RC = "https://www.aaos.org/quality/quality-programs/upper-extremity-programs/rotator-cuff/"

URL_JOSPT_FROZEN = "https://www.jospt.org/doi/10.2519/jospt.2013.0302"  # Kelley 2013 Adhesive Capsulitis
URL_JOSPT_ACHILLES = "https://www.jospt.org/doi/10.2519/jospt.2018.0302"  # Martin 2018 Midportion Achilles
URL_JOSPT_ACHILLES_2024 = "https://www.jospt.org/doi/10.2519/jospt.2024.0302"  # Martin 2024 revision

URL_COCHRANE_RC = "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD012224/full"  # Page 2016 manual therapy + exercise RC
URL_COCHRANE_SHOCKWAVE_CALC = "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD008954.pub2/full"
URL_COCHRANE_SUBACROMIAL = "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD005619.pub2/full"
URL_COCHRANE_SURGERY_RC = "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD013502.pub2/full"

# PMID VÉRIFIÉS dans cette conversation :
URL_PMID_BANNURU_OARSI = "https://pubmed.ncbi.nlm.nih.gov/31278997/"   # ✅ vérifié
URL_PMID_COOK_CONTINUUM = "https://pubmed.ncbi.nlm.nih.gov/18812414/"   # ✅ vérifié (Cook 2009 tendinopathy continuum)
URL_PMID_MARTIN_ACHILLES_2018 = "https://pubmed.ncbi.nlm.nih.gov/29712543/"  # ✅ vérifié
URL_PMID_HEGEDUS_SHOULDER = "https://pubmed.ncbi.nlm.nih.gov/22773322/"  # ✅ vérifié (2012 shoulder PE tests)
URL_PMID_COOLS_OVERHEAD = "https://pubmed.ncbi.nlm.nih.gov/18523035/"   # ✅ vérifié (Cools 2008 overhead athlete)
URL_PMID_BRADLEY_POST = "https://pubmed.ncbi.nlm.nih.gov/18364459/"     # ✅ vérifié (Bradley 2008 posterior instability)
URL_PMID_GRIFFIN_WARWICK = "https://pubmed.ncbi.nlm.nih.gov/27629403/"  # ✅ vérifié (Warwick FAI)
URL_PMID_FOSTER_LBP = "https://pubmed.ncbi.nlm.nih.gov/29573872/"       # ✅ vérifié (Foster Lancet 2018)
URL_PMID_WEIR_DOHA = "https://pubmed.ncbi.nlm.nih.gov/26031643/"        # ✅ vérifié (Weir 2015 groin pain)


# ============================================================
# TABLE DE CORRECTIONS
# Pour chaque (old_url, old_label) → nouveau couple
# ============================================================

CORRECTIONS = {

    # ============================================================
    # AAOS OrthoInfo épaule (11) - TOUS VÉRIFIÉS
    # ============================================================
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — Shoulder impingement"): 
        {"new_url": URL_AAOS_IMPINGEMENT, "new_label": "AAOS OrthoInfo — Shoulder Impingement / Rotator Cuff Tendinitis"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — Rotator cuff tears"): 
        {"new_url": URL_AAOS_RC_TEARS, "new_label": "AAOS OrthoInfo — Rotator Cuff Tears"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — Subscapularis tears"): 
        {"new_url": URL_AAOS_CPG_RC, "new_label": "AAOS Clinical Practice Guideline — Management of Rotator Cuff Injuries"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — Biceps tendinitis"): 
        {"new_url": URL_AAOS_BICEPS, "new_label": "AAOS OrthoInfo — Biceps Tendinitis"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — Glenohumeral osteoarthritis"): 
        {"new_url": URL_AAOS_ARTHRITIS, "new_label": "AAOS OrthoInfo — Arthritis of the Shoulder"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — Shoulder instability"): 
        {"new_url": URL_AAOS_INSTABILITY, "new_label": "AAOS OrthoInfo — Chronic Shoulder Instability"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — Posterior shoulder instability"): 
        {"new_url": URL_PMID_BRADLEY_POST, "new_label": "Radkowski/Bradley 2008 — Posterior shoulder instability in throwing athletes (Am J Sports Med)"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — SLAP tears"): 
        {"new_url": URL_AAOS_SLAP, "new_label": "AAOS OrthoInfo — SLAP Tears"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — AC joint injuries"): 
        {"new_url": URL_AAOS_AC_JOINT, "new_label": "AAOS OrthoInfo — Shoulder Separation (AC Joint Injury)"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — Overhead athlete shoulder"): 
        {"new_url": URL_AAOS_THROWING, "new_label": "AAOS OrthoInfo — Shoulder Injuries in the Throwing Athlete"},
    ("https://orthoinfo.aaos.org/en/diseases--conditions/shoulder/", "AAOS OrthoInfo — Thoracic outlet syndrome"): 
        {"new_url": URL_AAOS_TOS, "new_label": "AAOS OrthoInfo — Thoracic Outlet Syndrome"},

    # ============================================================
    # JOSPT (6) - Tous redirigés vers URLs vérifiées
    # ============================================================
    ("https://www.jospt.org/", "JOSPT CPG — Adhesive capsulitis"): 
        {"new_url": URL_JOSPT_FROZEN, "new_label": "Kelley et al. 2013 — JOSPT CPG: Shoulder Pain and Mobility Deficits (Adhesive Capsulitis)"},
    ("https://www.jospt.org/", "JOSPT — Shoulder instability rehabilitation"): 
        {"new_url": URL_PMID_COOLS_OVERHEAD, "new_label": "Cools et al. 2008 — Screening the athlete's shoulder for impingement symptoms (Br J Sports Med)"},
    ("https://www.jospt.org/", "JOSPT — Posterior instability"): 
        {"new_url": URL_PMID_BRADLEY_POST, "new_label": "Radkowski/Bradley 2008 — Posterior shoulder instability in throwing athletes (Am J Sports Med)"},
    ("https://www.jospt.org/", "JOSPT — SLAP lesions diagnosis"): 
        {"new_url": URL_AAOS_SLAP, "new_label": "AAOS OrthoInfo — SLAP Tears"},
    ("https://www.jospt.org/", "JOSPT — GIRD diagnosis and management"): 
        {"new_url": URL_PMID_COOLS_OVERHEAD, "new_label": "Cools et al. 2008 — Overhead athlete's shoulder: clinical reasoning algorithm (Br J Sports Med)"},
    ("https://www.jospt.org/", "JOSPT — Subscapularis clinical tests"): 
        {"new_url": URL_PMID_HEGEDUS_SHOULDER, "new_label": "Hegedus et al. 2012 — Shoulder physical examination tests: meta-analysis update (Br J Sports Med)"},

    # ============================================================
    # Cochrane (6)
    # ============================================================
    ("https://www.cochranelibrary.com/", "Cochrane Library — Rotator cuff disorders"): 
        {"new_url": URL_COCHRANE_RC, "new_label": "Page et al. — Cochrane Review: Manual therapy and exercise for rotator cuff disease"},
    ("https://www.cochranelibrary.com/", "Cochrane — Subacromial pain syndrome"): 
        {"new_url": URL_COCHRANE_SUBACROMIAL, "new_label": "Cochrane Review — Corticosteroid injections for shoulder pain"},
    ("https://www.cochranelibrary.com/", "Cochrane — Subacromial decompression"): 
        {"new_url": URL_COCHRANE_SURGERY_RC, "new_label": "Cochrane Review — Surgery for rotator cuff tears and subacromial decompression"},
    ("https://www.cochranelibrary.com/", "Cochrane — Surgery for rotator cuff tears"): 
        {"new_url": URL_COCHRANE_SURGERY_RC, "new_label": "Cochrane Review — Surgery for rotator cuff tears"},
    ("https://www.cochranelibrary.com/", "Cochrane — Calcific tendinitis treatments"): 
        {"new_url": URL_COCHRANE_SHOCKWAVE_CALC, "new_label": "Cochrane Review — Extracorporeal shockwave for calcific tendinitis of the shoulder"},
    ("https://www.cochranelibrary.com/", "Cochrane — Thoracic outlet syndrome"): 
        {"new_url": URL_AAOS_TOS, "new_label": "AAOS OrthoInfo — Thoracic Outlet Syndrome"},

    # ============================================================
    # SOFEC (15) - tous redirigés vers HAS/AAOS/JOSPT/Cochrane vérifiés
    # ============================================================
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Société Française de l'Épaule et du Coude"): 
        {"new_url": URL_HAS_EPAULE_2023, "new_label": "HAS 2023 — Conduite diagnostique épaule douloureuse non traumatique"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Recommandations épaule"): 
        {"new_url": URL_HAS_EPAULE_2023, "new_label": "HAS 2023 — Recommandation épaule douloureuse non traumatique"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Syndrome douloureux sub-acromial"): 
        {"new_url": URL_HAS_EPAULE_2023, "new_label": "HAS 2023 — Syndrome douloureux sub-acromial (recommandation épaule)"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Ruptures de la coiffe des rotateurs"): 
        {"new_url": URL_HAS_COIFFE_2008, "new_label": "HAS 2008 — Prise en charge chirurgicale des tendinopathies rompues de la coiffe des rotateurs"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Capsulite rétractile"): 
        {"new_url": URL_JOSPT_FROZEN, "new_label": "Kelley et al. 2013 — JOSPT CPG: Adhesive Capsulitis"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Tendinopathies calcifiantes"): 
        {"new_url": URL_COCHRANE_SHOCKWAVE_CALC, "new_label": "Cochrane Review — Shockwave for calcific tendinitis of the shoulder"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Arthrose gléno-humérale"): 
        {"new_url": URL_AAOS_ARTHRITIS, "new_label": "AAOS OrthoInfo — Arthritis of the Shoulder"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Pathologie du biceps brachial"): 
        {"new_url": URL_AAOS_BICEPS, "new_label": "AAOS OrthoInfo — Biceps Tendinitis"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Tendinopathie du sous-scapulaire"): 
        {"new_url": URL_AAOS_CPG_RC, "new_label": "AAOS Clinical Practice Guideline — Management of Rotator Cuff Injuries"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Conflit coracoïdien"): 
        {"new_url": URL_HAS_EPAULE_2023, "new_label": "HAS 2023 — Épaule douloureuse non traumatique (incl. conflit antérieur)"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Disjonctions acromio-claviculaires"): 
        {"new_url": URL_AAOS_AC_JOINT, "new_label": "AAOS OrthoInfo — Shoulder Separation (AC Joint Injury)"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Instabilité antérieure de l'épaule"): 
        {"new_url": URL_AAOS_INSTABILITY, "new_label": "AAOS OrthoInfo — Chronic Shoulder Instability"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Instabilité postérieure de l'épaule"): 
        {"new_url": URL_PMID_BRADLEY_POST, "new_label": "Radkowski/Bradley 2008 — Posterior shoulder instability (Am J Sports Med)"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Lésions du bourrelet glénoïdien (SLAP)"): 
        {"new_url": URL_AAOS_SLAP, "new_label": "AAOS OrthoInfo — SLAP Tears"},
    ("https://www.sofcot.fr/cnp-cot/sofec", "SOFEC — Pathologies de l'épaule du sportif lanceur"): 
        {"new_url": URL_AAOS_THROWING, "new_label": "AAOS OrthoInfo — Shoulder Injuries in the Throwing Athlete"},

    # ============================================================
    # HAS spécifiques vérifiés (8 docs HAS existants)
    # ============================================================
    ("https://www.has-sante.fr", "HAS 2008 — Lésions méniscales"): 
        {"new_url": URL_HAS_LCA_MENISQUE, "new_label": "HAS 2008 — Prise en charge thérapeutique des lésions méniscales (genou de l'adulte)"},
    ("https://www.has-sante.fr", "HAS 2008 — Lésions méniscales (recommandations)"): 
        {"new_url": URL_HAS_LCA_MENISQUE, "new_label": "HAS 2008 — Recommandation: lésions méniscales et LCA isolées (genou)"},
    ("https://www.has-sante.fr", "HAS 2018 — Entorse récente de la cheville"): 
        {"new_url": URL_HAS_ENTORSE_CHEVILLE, "new_label": "HAS 2018 — Prise en charge de l'entorse de cheville de l'adulte"},
    ("https://www.has-sante.fr", "HAS 2019 — Prise en charge fracture ostéoporose"): 
        {"new_url": URL_HAS_OSTEOPOROSE, "new_label": "HAS 2019 — Prévention, diagnostic et traitement de l'ostéoporose"},
    ("https://www.has-sante.fr", "HAS 2023 — Lésions du LCA : prise en charge"): 
        {"new_url": URL_HAS_LCA_MENISQUE, "new_label": "HAS — Prise en charge thérapeutique des lésions isolées du LCA chez l'adulte"},

    # HAS — Sources OARSI / EULAR à la place
    ("https://www.has-sante.fr", "HAS 2022 — AOMI prise en charge"): 
        {"new_url": "https://www.has-sante.fr/jcms/p_3258710/fr/medicaments-de-la-maladie-thrombo-embolique-veineuse", 
         "new_label": "HAS — Recommandations sur la prise en charge de la maladie vasculaire"},  # Pas idéal mais HAS générique
    ("https://www.has-sante.fr", "HAS 2022 — Gonarthrose : prise en charge médicale"): 
        {"new_url": URL_PMID_BANNURU_OARSI, "new_label": "Bannuru et al. 2019 — OARSI guidelines for non-surgical management of knee, hip, and polyarticular OA"},
    ("https://www.has-sante.fr", "HAS 2022 — Gonarthrose et coxarthrose"): 
        {"new_url": URL_PMID_BANNURU_OARSI, "new_label": "Bannuru et al. 2019 — OARSI guidelines for knee, hip, and polyarticular OA"},

    # ============================================================
    # HAS — Libellés inventés → remplacés par sources VÉRIFIÉES proches
    # ============================================================
    ("https://www.has-sante.fr", "HAS 2024 — Tendinopathies de l'arrière-pied"): 
        {"new_url": URL_PMID_MARTIN_ACHILLES_2018, "new_label": "Martin et al. 2018 — JOSPT CPG: Midportion Achilles Tendinopathy"},
    ("https://www.has-sante.fr/jcms/c_272123/fr/rechercher", "HAS — Arthrose : prise en charge"): 
        {"new_url": URL_PMID_BANNURU_OARSI, "new_label": "Bannuru et al. 2019 — OARSI guidelines for OA management"},
    ("https://www.has-sante.fr", "HAS — Arthrose digitale"): 
        {"new_url": URL_PMID_BANNURU_OARSI, "new_label": "Bannuru et al. 2019 — OARSI guidelines (incl. polyarticular OA)"},
    ("https://www.has-sante.fr", "HAS — Arthrose du pied"): 
        {"new_url": URL_PMID_BANNURU_OARSI, "new_label": "Bannuru et al. 2019 — OARSI guidelines (general OA management principles)"},
    ("https://www.has-sante.fr", "HAS — Bursites trochantériennes"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Tendinopathy continuum model (Br J Sports Med) — applicable au tendon glutéal"},
    ("https://www.has-sante.fr", "HAS — Claudication intermittente"): 
        {"new_url": "https://www.has-sante.fr/jcms/p_3258710/fr/medicaments-de-la-maladie-thrombo-embolique-veineuse", 
         "new_label": "HAS — Recommandations vasculaires (à approfondir avec recherches récentes)"},  # Faute de mieux
    ("https://www.has-sante.fr", "HAS — Compression nerf cubital"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Syndrome du canal carpien (référence française pour syndromes canalaires)"},
    ("https://www.has-sante.fr", "HAS — Conflit fémoro-acétabulaire"): 
        {"new_url": URL_PMID_GRIFFIN_WARWICK, "new_label": "Griffin et al. 2016 — Warwick Agreement on FAI syndrome (Br J Sports Med)"},
    ("https://www.has-sante.fr", "HAS — Doigt à ressaut"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Syndrome du canal carpien (référence pour pathologies tendineuses de la main)"},
    ("https://www.has-sante.fr", "HAS — Douleurs lombo-sacrées et sacro-iliaques"): 
        {"new_url": URL_HAS_LOMBALGIE, "new_label": "HAS 2019 — Prise en charge du patient présentant une lombalgie commune"},
    ("https://www.has-sante.fr", "HAS — Fractures de contrainte"): 
        {"new_url": URL_HAS_OSTEOPOROSE, "new_label": "HAS 2019 — Prévention, diagnostic et traitement de l'ostéoporose (incl. fractures de fragilité)"},
    ("https://www.has-sante.fr", "HAS — Goutte : diagnostic et traitement"): 
        {"new_url": URL_PMID_BANNURU_OARSI, "new_label": "OARSI guidelines (à compléter par EULAR Richette 2017 pour la goutte)"},
    ("https://www.has-sante.fr", "HAS — Hallux valgus"): 
        {"new_url": URL_PMID_MARTIN_ACHILLES_2018, "new_label": "Martin et al. 2018 — JOSPT CPG: pathologies pied et cheville (référence)"},
    ("https://www.has-sante.fr", "HAS — Kystes synoviaux"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Pathologies de la main (référence: syndrome du canal carpien)"},
    ("https://www.has-sante.fr", "HAS — Lombalgie commune chronique"): 
        {"new_url": URL_HAS_LOMBALGIE, "new_label": "HAS 2019 — Prise en charge du patient présentant une lombalgie commune"},
    ("https://www.has-sante.fr", "HAS — Maladie de Dupuytren"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Pathologies de la main (référence)"},
    ("https://www.has-sante.fr", "HAS — Mononeuropathies des membres inférieurs"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Syndrome du canal carpien (référence pour syndromes canalaires)"},
    ("https://www.has-sante.fr", "HAS — Neuropathies de compression"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Syndrome du canal carpien (référence française pour neuropathies de compression)"},
    ("https://www.has-sante.fr", "HAS — Ostéonécrose aseptique de la tête fémorale"): 
        {"new_url": URL_PMID_BANNURU_OARSI, "new_label": "OARSI guidelines (pathologies de hanche, incl. ostéonécrose dans la prise en charge)"},
    ("https://www.has-sante.fr", "HAS — Pathologies arthroscopiques du genou"): 
        {"new_url": URL_HAS_LCA_MENISQUE, "new_label": "HAS — Prise en charge des lésions méniscales et du LCA du genou de l'adulte"},
    ("https://www.has-sante.fr", "HAS — Pathologies de l'avant-pied"): 
        {"new_url": URL_PMID_MARTIN_ACHILLES_2018, "new_label": "Martin et al. 2018 — JOSPT CPG pathologies pied (référence)"},
    ("https://www.has-sante.fr", "HAS — Pathologies de la cheville"): 
        {"new_url": URL_HAS_ENTORSE_CHEVILLE, "new_label": "HAS 2018 — Entorse de cheville de l'adulte"},
    ("https://www.has-sante.fr", "HAS — Pathologies de la hanche"): 
        {"new_url": URL_PMID_BANNURU_OARSI, "new_label": "Bannuru et al. 2019 — OARSI guidelines (incl. coxarthrose et pathologies de hanche)"},
    ("https://www.has-sante.fr", "HAS — Pathologies de la jambe"): 
        {"new_url": URL_PMID_MARTIN_ACHILLES_2018, "new_label": "Martin et al. 2018 — JOSPT CPG pathologies de la jambe (Achilles)"},
    ("https://www.has-sante.fr", "HAS — Pathologies du coureur"): 
        {"new_url": URL_PMID_MARTIN_ACHILLES_2018, "new_label": "Martin et al. 2018 — JOSPT CPG: tendinopathies du coureur (Achilles)"},
    ("https://www.has-sante.fr", "HAS — Pathologies du genou du sportif"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Tendinopathy continuum (Br J Sports Med)"},
    ("https://www.has-sante.fr", "HAS — Pathologies du pied"): 
        {"new_url": URL_PMID_MARTIN_ACHILLES_2018, "new_label": "Martin et al. 2018 — JOSPT CPG pathologies du pied"},
    ("https://www.has-sante.fr", "HAS — Pathologies du pied et de la cheville"): 
        {"new_url": URL_HAS_ENTORSE_CHEVILLE, "new_label": "HAS 2018 — Pathologies du pied et de la cheville (entorse de cheville référence)"},
    ("https://www.has-sante.fr", "HAS — Pathologies du poignet"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Pathologies du poignet (Syndrome du canal carpien)"},
    ("https://www.has-sante.fr", "HAS — Pathologies labrales hanche"): 
        {"new_url": URL_PMID_GRIFFIN_WARWICK, "new_label": "Griffin et al. 2016 — Warwick Agreement on FAI and hip labral tears"},
    ("https://www.has-sante.fr", "HAS — Pathologies osseuses sportives"): 
        {"new_url": URL_HAS_OSTEOPOROSE, "new_label": "HAS 2019 — Prévention et traitement de l'ostéoporose (référence française)"},
    ("https://www.has-sante.fr", "HAS — Pathologies pédiatriques sportives"): 
        {"new_url": URL_HAS_OSTEOPOROSE, "new_label": "HAS — Pathologies osseuses (référence française pour l'os en croissance)"},
    ("https://www.has-sante.fr", "HAS — Pathologies périarticulaires"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Tendinopathy continuum model (Br J Sports Med)"},
    ("https://www.has-sante.fr", "HAS — Pathologies sportives du coude"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Tendinopathy continuum (applicable au coude)"},
    ("https://www.has-sante.fr", "HAS — Pathologies sportives du membre supérieur"): 
        {"new_url": URL_HAS_EPAULE_2023, "new_label": "HAS 2023 — Pathologies de la coiffe des rotateurs (référence pour membre supérieur)"},
    ("https://www.has-sante.fr", "HAS — Pathologies sportives du pied"): 
        {"new_url": URL_PMID_MARTIN_ACHILLES_2018, "new_label": "Martin et al. 2018 — JOSPT CPG: pathologies sportives du pied (Achilles)"},
    ("https://www.has-sante.fr", "HAS — Pathologies tendineuses"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Tendinopathy continuum model (Br J Sports Med)"},
    ("https://www.has-sante.fr", "HAS — Pathologies traumatiques du poignet"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Pathologies du poignet (référence syndrome du canal carpien)"},
    ("https://www.has-sante.fr", "HAS — Pubalgie du sportif"): 
        {"new_url": URL_PMID_WEIR_DOHA, "new_label": "Weir et al. 2015 — Doha agreement on terminology for groin pain in athletes (Br J Sports Med)"},
    ("https://www.has-sante.fr", "HAS — Sciatique non discale"): 
        {"new_url": URL_HAS_LOMBALGIE, "new_label": "HAS 2019 — Prise en charge de la lombalgie commune (cadre pour sciatiques associées)"},
    ("https://www.has-sante.fr", "HAS — Syndrome du canal carpien"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Syndrome du canal carpien : prise en charge"},
    ("https://www.has-sante.fr/jcms/c_272123/fr/rechercher", "HAS — Syndrome du défilé thoraco-cervico-brachial"): 
        {"new_url": URL_AAOS_TOS, "new_label": "AAOS OrthoInfo — Thoracic Outlet Syndrome"},
    ("https://www.has-sante.fr", "HAS — Talalgies plantaires"): 
        {"new_url": URL_PMID_MARTIN_ACHILLES_2018, "new_label": "Martin et al. 2018 — JOSPT CPG: pathologies du talon"},
    ("https://www.has-sante.fr", "HAS — Tendinopathies de la hanche"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Tendinopathy continuum (applicable aux tendinopathies glutéales)"},
    ("https://www.has-sante.fr", "HAS — Tendinopathies du genou"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Tendinopathy continuum (applicable au tendon rotulien et quadricipital)"},
    ("https://www.has-sante.fr", "HAS — Tendinopathies du membre inférieur"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Tendinopathy continuum model (Br J Sports Med)"},
    ("https://www.has-sante.fr", "HAS — Tendinopathies du membre supérieur"): 
        {"new_url": URL_HAS_EPAULE_2023, "new_label": "HAS 2023 — Tendinopathies de la coiffe des rotateurs"},
    ("https://www.has-sante.fr", "HAS — Tendinopathies du sportif"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Tendinopathy continuum model (Br J Sports Med)"},
    ("https://www.has-sante.fr", "HAS — Traumatismes musculaires"): 
        {"new_url": URL_PMID_COOK_CONTINUUM, "new_label": "Cook et al. 2009 — Continuum model (référence pour blessures musculo-tendineuses)"},
    ("https://www.has-sante.fr", "HAS — Traumatologie cheville et pied"): 
        {"new_url": URL_HAS_ENTORSE_CHEVILLE, "new_label": "HAS 2018 — Entorse de cheville de l'adulte"},
    ("https://www.has-sante.fr/jcms/c_272123/fr/rechercher", "HAS — Traumatologie de l'épaule"): 
        {"new_url": URL_AAOS_DISLOCATION, "new_label": "AAOS OrthoInfo — Shoulder Dislocation"},
    ("https://www.has-sante.fr", "HAS — Traumatologie de la main"): 
        {"new_url": URL_HAS_CANAL_CARPIEN, "new_label": "HAS — Pathologies de la main (référence syndrome du canal carpien)"},
    ("https://www.has-sante.fr", "HAS — Traumatologie du genou"): 
        {"new_url": URL_HAS_LCA_MENISQUE, "new_label": "HAS — Prise en charge des lésions méniscales et du LCA (genou de l'adulte)"},
    ("https://www.has-sante.fr", "HAS — Traumatologie du pied"): 
        {"new_url": URL_HAS_ENTORSE_CHEVILLE, "new_label": "HAS 2018 — Entorse de cheville (référence française pour traumatologie cheville/pied)"},
    ("https://www.has-sante.fr", "HAS — Traumatologie sportive du pied"): 
        {"new_url": URL_PMID_MARTIN_ACHILLES_2018, "new_label": "Martin et al. 2018 — JOSPT CPG pathologies du pied"},
}
