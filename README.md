# LocoClic — Site web

Site statique d'aide au diagnostic des pathologies musculo-squelettiques.

## 📁 Contenu

- `index.html` — Page d'accueil avec logo, hero, grille des 11 modules
- `lococlic_*_v5.html` — Les 11 modules d'aide diagnostique
- Bouton "← Accueil" intégré en haut à gauche de chaque module

## 🚀 Déploiement

Le site est 100% statique. Aucun serveur, aucune base de données, aucune dépendance externe.

### Option 1 — Test en local
Double-cliquer sur `index.html` ou ouvrir avec navigateur.

### Option 2 — Hébergement gratuit
- **GitHub Pages** : créer un repo, uploader le dossier, activer Pages
- **Netlify** : drag & drop du dossier sur netlify.com
- **Vercel** : importer le dossier sur vercel.com
- **Cloudflare Pages** : connecter un repo

### Option 3 — Hébergement propre
Uploader le dossier sur n'importe quel hébergeur web classique (OVH, Infomaniak, etc.).

## 📐 Structure des modules

Chaque module suit le même schéma v5 :
1. **Mécanisme** — Comment la douleur est apparue
2. **Profil** — Tranche d'âge et activité
3. **Tableau clinique** — Vignettes localisations et présentations
4. **Horaire** — Profil temporel de la douleur
5. **Tests cliniques** — 5 tests adaptatifs avec scoring probabiliste
6. **Résultat** — Fiche diagnostique avec imagerie / traitement / orientation / sources

## 🎨 Design

- Palette : bleu marine (#1e3a5f) + accent turquoise (#10b981)
- Logo SVG intégré (anatomie + "click" turquoise)
- Responsive mobile-first
- Aucune dépendance JS externe

## ⚠️ Avertissement

Outil d'aide à la décision clinique. Ne remplace pas l'examen clinique et le jugement médical du praticien.
