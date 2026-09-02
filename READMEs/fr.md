<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-light.svg">
    <img src="../assets/hero-dark.svg" alt="goalify : préparation d'une exécution autonome. Revenez à une preuve, pas à une promesse." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validation"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=8E7BFF" alt="licence MIT"></a>
  <a href="https://github.com/Aboudjem/goalify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/goalify?color=8E7BFF" alt="étoiles GitHub"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <a href="ja.md">日本語</a> · <a href="es.md">Español</a> · <b>Français</b>
</p>

<p align="center">
  <strong>Confiez une tâche énorme à Claude. Revenez à la preuve qu'elle est faite, pas à la promesse qu'elle l'est.</strong>
</p>

<p align="center">
  <a href="#ce-que-ça-fait">Ce que ça fait</a> · <a href="#installation">Installation</a> · <a href="#utilisation">Utilisation</a> · <a href="#ce-que-vous-obtenez">Ce que vous obtenez</a> · <a href="#fonctionne-dans-votre-éditeur">Fonctionne dans votre éditeur</a> · <a href="#bon-à-savoir">Bon à savoir</a>
</p>

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

## Ce que ça fait

Certains chantiers sont trop gros pour rester à les regarder. Renommer une chose dans des centaines
de fichiers. Faire passer un vieux projet sur une version plus récente du code sur lequel il repose.
Traverser un projet en désordre pour nettoyer un seul type de problème. Vous décrivez le travail
pendant que Claude a encore votre contexte, et goalify écrit ce que l'exécution doit faire et à quoi
ressemble le fait d'avoir terminé. Puis il vous tend une ligne à coller.

- **Le brief** est un fichier qui contient tout ce dont l'exécution a besoin : vos décisions, les
  chemins exacts, l'ordre du travail.
- **La condition** est la ligne que vous collez dans `/goal`, le contrôle d'arrêt intégré à Claude
  Code, qui garde la session au travail et juge chaque tour au regard de cette ligne.

Imaginez un chantier. Le brief, ce sont les plans sur lesquels travaille celui qui construit. La
condition, c'est la liste de contrôle que signe celui qui inspecte, et cette personne ne lit jamais les plans et
ne vient jamais sur le chantier. Elle ne juge que les preuves qu'on lui montre.

## Installation

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

N'importe quel autre agent, en une ligne :

```bash
npx skills add Aboudjem/goalify
```

<details>
<summary>Le copier à la main</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

Rien d'autre dans le dépôt n'est nécessaire à l'exécution. Vous voudrez Claude Code 2.1.139 ou plus
récent, car c'est la version dans laquelle `/goal` est arrivé. Le reste est dans le
[démarrage rapide](../docs/quickstart.md).
</details>

## Utilisation

**1. Décrivez le travail.** Lancez `/goalify` suivi de votre tâche dans Claude Code. goalify lit
votre projet, vous interroge sur les quelques vraies décisions, écrit le brief et affiche la
condition.

```text
/goalify migrate our API to async/await
    Brief:     ~/acme/.goal/api-migration.md
    Condition: 149 chars, under the 4,000 limit
```

**2. Videz la conversation.** `/clear` efface l'échange, l'exécution repart donc à neuf, pleinement
attentive.

**3. Collez la condition.** La ligne entière. Elle se replie à l'écran, alors prenez-la en entier.

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it - done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

Le chemin du brief voyage à l'intérieur de cette ligne, car l'évaluateur derrière `/goal` n'a aucun
outil et ne peut pas ouvrir de fichier. Il lit la ligne que vous collez et une transcription tronquée de l'exécution, jamais le brief
lui-même. Lui donner le
chemin tout seul ne provoque aucune erreur et ne prouve rien, ce qui en fait l'erreur la plus facile
à commettre :

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

Un doute sur une ligne avant de la coller ?
`python3 skills/goalify/scripts/condition_lint.py "<your condition>"` la vérifie au regard de six
règles mécaniques et nomme celles qu'elle rate. Les appréciations restent les vôtres.

<p align="center">
  <img src="../assets/hero.svg" alt="Quatre étapes : décrire le travail, recevoir un brief et une condition, coller la condition, revenir à la preuve." width="72%">
</p>

## Ce que vous obtenez

- **Une seule ligne à transmettre.** Videz la conversation, collez une ligne, partez.
- **Votre contexte survit à la remise à zéro.** Le brief porte vos décisions dans la nouvelle session.
- **Une progression visible d'un coup d'œil.** L'exécution coche une liste de contrôle à l'intérieur du brief au
  fur et à mesure.
- **Une preuve, pas une promesse.** Le dernier tour doit citer les vérifications qui passent et
  afficher un mot inventé, `ASYNC-OK` ci-dessus, si bien qu'une exécution qui aurait sauté le travail
  devrait mentir ouvertement.
- **Une fin propre au plafond.** À l'approche de sa limite de tours, l'exécution arrête d'ouvrir de
  nouveaux chantiers, termine ou annule ce qui est à moitié fait, et dit dans son rapport final
  qu'elle s'est arrêtée en avance.
- **Un arrêt garde votre progression.** Le brief reste en place, sa liste de contrôle intacte. Vous reprenez en
  collant la même ligne, vous ne recommencez pas.
- **Un classement seulement en cas de succès.** Le tour de clôture rejoue toutes les vérifications,
  cite la sortie et déplace le brief dans `.goal/done/`, un déplacement de fichier visible dans
  n'importe quel navigateur de fichiers.

## Fonctionne dans votre éditeur

Fonctionne dans Claude Code, Cursor, Codex, Copilot, Gemini CLI et plus de 70 autres agents via
`npx skills add`. La compétence est du Markdown pur, rien en elle n'est lié à un modèle donné.

| Agent | Installation en une ligne |
|:--|:--|
| Claude Code | `claude plugin install goalify@10x` |
| N'importe lequel des 70 agents et plus | `npx skills add Aboudjem/goalify` |
| Cursor, Codex, Copilot, Gemini CLI, OpenCode | `npx skills add Aboudjem/goalify -a <agent>` |
| Tout le reste | les codes d'agent et les chemins dans [docs/editors.md](../docs/editors.md) |

`/clear` et `/goal` sont des commandes de Claude Code. Ailleurs, ouvrez une nouvelle session à la
place de `/clear` et donnez-lui la condition comme objectif constant. Codex a son propre `/goal`, et
[l'utiliser sous Codex](../docs/codex.md) dit ce qui se transporte et ce qui ne se transporte pas.

## Bon à savoir

> [!IMPORTANT]
> Une exécution qui s'arrête ne prouve pas qu'elle a fini. L'évaluateur juge par lui-même et peut
> mettre fin à une exécution en décidant que la ligne d'arrivée est hors d'atteinte. Avant de croire
> un résultat au vert, relisez les preuves de clôture, les vérifications citées dans la dernière
> réponse et le brief déplacé dans `.goal/done/`, ou rejouez les vérifications vous-même.

- **goalify rédige, il n'exécute jamais.** Il écrit les deux artefacts dans cette session puis
  s'arrête. C'est vous qui lancez l'exécution.
- **Rien ne tourne en arrière-plan.** Une compétence Markdown, sans serveur, sans dépendance à
  installer, sans appel réseau qui lui soit propre.
- **Tout ce qu'il ne promet pas** est écrit dans [les limites honnêtes](../docs/limits.md).

## En savoir plus

- [Démarrage rapide](../docs/quickstart.md), une première exécution de bout en bout, et les autres
  façons d'installer.
- [Conditions travaillées](../examples/conditions.md), huit qui méritent d'être livrées et huit à
  éviter, chacune avec une ligne qui dit ce que la mauvaise perd.
- [Un exemple complet](../examples/sample-brief.md), un vrai brief et la condition qui en découle.
- [Installer dans votre éditeur](../docs/editors.md) · [FAQ](../docs/faq.md) · [Sous Codex](../docs/codex.md)
- [Limites honnêtes](../docs/limits.md) · [Journal des modifications](../CHANGELOG.md) · [La compétence elle-même](../skills/goalify/SKILL.md) · [Licence](../LICENSE)

<p align="center"><sub><a href="../assets/goalify-teaser.mp4">Voir la bande-annonce de 28 secondes</a> · <a href="../assets/goalify-teaser.gif">GIF</a></sub></p>

---

<sub>Réalisé par <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. Licence MIT. Le
comportement de `/goal` a été redérivé du binaire Claude Code 2.1.223 distribué, en 2026.
<a href="https://github.com/Aboudjem/goalify/issues">Vous voyez un manque ?</a></sub>

<sub>Traduction assistée par machine. La version de référence est le <a href="../README.md">README.md</a> en anglais.</sub>
