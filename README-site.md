# Pages à ajouter à `ulcan19.github.io`

## Ce qui va dans le repo

```
notes/
├── index.html                                     # l'index des notes
└── guardrails-retrieved-by-similarity/
    └── index.html                                 # l'article
build.py                                           # régénère les deux, calcule les hashes CSP
_shared.css   _article.css   _lang.js              # sources assemblées par build.py
_article_en.html   _article_fr.html                # corps de l'article, par langue
```

Les fichiers `_*` et `build.py` peuvent rester dans le repo : GitHub Pages
sert `notes/**/index.html` et ignore le reste. Les garder versionnés est ce
qui rend la page suivante éditable.

## Pourquoi un build.py sur un site sans build

Parce que ta CSP est appliquée par hash. Un octet modifié dans le `<style>`
ou le `<script>` inline et la page cesse de les exécuter. Éditer les hashes à
la main marche une fois, puis on oublie, et le symptôme est une page qui
s'affiche sans style sans qu'aucune erreur ne remonte — le même mode de
défaillance silencieux que décrit l'article.

```bash
python3 build.py           # régénère les pages
python3 build.py --check   # échoue si une page ne correspond plus à ses sources
```

`--check` en pre-commit ou en CI évite de pousser une page dont le hash a
divergé.

## Ce qui a été respecté du site existant

- Mêmes variables CSS, même typographie, même barre EN/FR.
- Même clé `localStorage` (`yu-lang`) : la langue choisie sur l'accueil suit
  sur les notes, et inversement.
- Aucune police, aucun script, aucune ressource tierce.
- Pas d'analytics.

## Ce qui diffère, et pourquoi

L'accueil traduit via `data-en` / `data-fr` sur chaque nœud. Pour un article
long, ça rendrait le HTML illisible. Les notes basculent donc **deux blocs
entiers** (`[data-lang-block="en"|"fr"]`), et gardent l'approche par attribut
pour les titres et la navigation.

Conséquence à connaître : sans JavaScript, aucun des deux blocs ne s'affiche.
Si ça te gêne, la correction est d'ajouter `class="on"` au bloc EN dans le
HTML généré — mais ça change le hash CSS, donc passe par `build.py`.

## Vérifications avant de pousser

1. Ouvrir `notes/guardrails-retrieved-by-similarity/index.html` en local, sans
   serveur : la CSP est déclarée en `<meta>`, elle s'applique aussi sur
   `file://`. Si la page est stylée et que la bascule EN/FR marche, les hashes
   sont bons.
2. Console ouverte : aucune violation CSP.
3. Le lien vers `github.com/Karibusan/scoped-memory` doit exister avant de
   publier le post LinkedIn.
