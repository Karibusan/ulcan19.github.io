# Deux modifications à faire à la main dans `index.html`

Je ne touche pas à ton fichier existant — voici les deux endroits à éditer.
Aucune des deux ne modifie le `<style>` ni le `<script>` inline, donc **les
hashes CSP de la page d'accueil restent valides**.

## 1 — Lien vers les notes, dans la nav du hero

Cherche le bloc `<nav class="cta">` et ajoute une entrée :

```html
<nav class="cta">
  <a href="/notes/" data-en="Notes" data-fr="Notes"></a>
  <a href="https://uk.linkedin.com/in/yanurquiza" rel="me">LinkedIn</a>
  <a href="https://github.com/gensecaihq/Wazuh-MCP-Server" rel="noopener">Wazuh-MCP-Server</a>
  <a href="mailto:ulcan19@pm.me" data-en="Email" data-fr="Écrire"></a>
</nav>
```

## 2 — `scoped-memory` dans la carte « Writing & open source »

Dans le `<ul class="clean">` de cette carte, en première position :

```html
<li data-en="Author, scoped-memory — a two-layer memory store for agents: rules are scrolled by scope, knowledge is searched by similarity"
    data-fr="Auteur de scoped-memory — mémoire d'agent à deux couches : les règles se scrollent par portée, les connaissances se cherchent par similarité"></li>
```

---

# Une troisième, pour octobre

Le pied de page dit actuellement :

> Based in the UK — full right to work.
> Basé au Royaume-Uni — plein droit de travail.

À changer au moment du déménagement, par exemple :

```html
<p class="foot-langs" data-en="French (native) · English (fluent) · Japanese (elementary). Based in France — EU and UK right to work."
   data-fr="Français (langue maternelle) · Anglais (courant) · Japonais (notions). Basé en France — droit de travail UE et Royaume-Uni."></p>
```

Vérifie la formulation UK selon ton statut réel après le départ — je ne sais
pas ce que tu conserves comme droit de travail là-bas.
