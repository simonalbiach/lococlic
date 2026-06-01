# 📦 LocoClic — Pack complet (RGPD + corrections)

Salut Simon,

Ce dossier contient **TON SITE COMPLET** mis à jour avec :

### 🛡️ Conformité juridique
- ✅ **3 nouvelles pages** : `mentions-legales.html`, `confidentialite.html`, `cgu.html`
- ✅ **Bandeau disclaimer médico-légal** sur les 13 pages racine
- ✅ **Footer légal** sur les 284 pages HTML du site
- ✅ Marque INPI mentionnée partout

### 🩺 Corrections médicales que tu as demandées
- ✅ **Bird-dog / Bracing** : encart corrigé dans `lombaire_08_lumbago_aigu.html`. L'encart présentait le bird-dog comme "plus simple" que le bracing, ce qui est l'inverse de la réalité (le bracing est plus simple, le bird-dog est une PROGRESSION). Le titre est maintenant "📈 Quand vous allez mieux, progressez vers..."
- ✅ **DEXA → DMO** : remplacé dans `lococlic_dorsal_v5.html` et `fract_vertebre_osteop_*.html`
- ✅ **Encart drapeaux rouges** ajouté sur les 29 fiches pathologies du rachis :
  - 9 fiches cervicales
  - 11 fiches dorsales
  - 9 fiches lombaires
  - Chaque encart est adapté au segment concerné

---

## 🚀 Marche à suivre (5 minutes)

### Étape 1 : Décompresse avec **The Unarchiver**
⚠️ PAS l'utilitaire natif macOS (il rajoute des accents).

### Étape 2 : Remplace ton dossier local
1. **GitHub Desktop** → Repository → **Show in Finder**
2. Sélectionne tout dans `lococlic-new/` (Cmd+A) → corbeille
   - Le `.git` caché reste intact, c'est normal
3. Entre dans le dossier décompressé `lococlic_site_final/`
4. Cmd+A → glisse-dépose dans `lococlic-new/` vide

### Étape 3 : GitHub Desktop
- Summary : `RGPD + corrections rachis (bird-dog, DMO, drapeaux rouges)`
- Commit to main → Push origin
- ⏳ Cloudflare redéploie en 2-5 min

### Étape 4 : Test
- `https://lococlic.com/cgu.html` → page CGU
- `https://lococlic.com/mentions-legales.html` → mentions
- `https://lococlic.com/confidentialite.html` → RGPD
- N'importe quelle fiche du rachis → encart drapeaux rouges en haut
- N'importe quelle page outil → bande jaune + footer bleu en bas

---

## 📧 Dernière action : adresses email pro

2 emails à activer (mentionnés dans les pages légales) :
- `contact@lococlic.com`
- `confidentialite@lococlic.com`

### Méthode GRATUITE : Cloudflare Email Routing

1. dash.cloudflare.com → domaine `lococlic.com`
2. Email → Email Routing → Get started
3. Crée 2 redirections vers ton email personnel
4. Confirme via le mail de vérif

**5 min, gratuit, illimité.**

---

## 🩺 Contenu des encarts drapeaux rouges

### CERVICAL (9 fiches)
- **Néo / Infectieux** : ATCD cancer, AEG, fièvre, douleur nocturne
- **Neurologiques** : déficit moteur, signes médullaires (Hoffmann, Babinski), troubles sphinctériens
- **Traumatiques / Vasculaires** : trauma haute énergie, dissection vertébrale, vertébro-basilaire
- **Rhumato** : spondylarthrite, PR (instabilité C1-C2)

### DORSAL (11 fiches)
- **Néo / Infectieux** : site métastatique fréquent, douleur nocturne
- **Fracture vertébrale** : ménopause, > 70 ans, corticothérapie, perte taille
- **Neurologiques** : déficit MI, syndrome médullaire
- **Viscérales (projection)** : SCA, dissection aortique, EP, ulcère

### LOMBAIRE (9 fiches)
- **Néo / Infectieux** : myélome inclus, douleur nocturne non mécanique
- **Neurologiques** : syndrome queue de cheval, sciatique déficitaire/hyperalgique
- **Fracture vertébrale** : facteurs ostéoporose
- **Rhumato / Vasculaires** : spondylarthrite, AAA, colique néphrétique

Tous : rouges (alerte forte), responsive mobile, print-friendly.

---

## 🔧 Scripts Python inclus (maintenance future)

### `inject_legal.py`
Réinjecte disclaimer + footer si tu ajoutes des pages.

### `apply_corrections.py`
Applique les 3 corrections (bird-dog, DMO, red flags rachis).

**Tu n'as PAS besoin de les lancer maintenant**, j'ai déjà tout fait. Ils sont là pour la maintenance future.

Pour les utiliser : `python3 inject_legal.py` dans Terminal au sein du dossier `lococlic-new`.

---

## 🎯 Récap final

| Élément | Quantité |
|---|---|
| Pages racine HTML | 13 + 3 pages légales |
| Fiches pathologies | 137 (29 avec drapeaux rouges) |
| Fiches patient | 134 |
| Disclaimer + footer | 284 pages |
| Encarts drapeaux rouges | 29 fiches rachis |
| Corrections DMO | 2 fichiers |
| Correction logique exercice | 1 fiche |

Tu es prêt pour :
- ✅ Distribuer LocoClic à tes 4 beta-testeurs
- ✅ Communiquer publiquement
- ✅ Préparer la landing page
- ✅ Démarcher des médecins sans risque

---

Bonne mise en ligne ! 💪

— Claude

P.S. Quand tu veux reprendre les illustrations Gemini (9 restantes pour finir l'épaule), je suis là 🎨
