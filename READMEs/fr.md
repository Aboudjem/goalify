<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-light.svg">
    <img src="../assets/hero-dark.svg" alt="goalify : donnez un gros travail à votre IA, recevez une preuve en retour." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validation"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=9b6bff" alt="licence MIT"></a>
  <a href="https://github.com/Aboudjem/goalify/releases"><img src="https://img.shields.io/github/v/release/Aboudjem/goalify?color=2ee6ff" alt="dernière version"></a>
  <a href="https://github.com/Aboudjem/goalify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/goalify?color=ff3d9a" alt="étoiles GitHub"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <a href="ja.md">日本語</a> · <a href="es.md">Español</a> · <b>Français</b>
</p>

<p align="center">
  <strong>Donnez un gros travail à votre IA. Recevez une preuve en retour.</strong>
</p>

<p align="center">
  <a href="https://goalify-kappa.vercel.app">Site web</a> · <a href="#installation">Installation</a> · <a href="#comment-ça-marche">Comment ça marche</a> · <a href="#nouveautés-de-la-30">Nouveautés de la 3.0</a> · <a href="#comparaison">Comparaison</a> · <a href="#bon-à-savoir">Bon à savoir</a>
</p>

goalify transforme votre demande en **objectif**. Un objectif est une ligne d'arrivée claire. L'IA
continue de travailler jusqu'à ce que l'objectif soit atteint et prouvé, ou jusqu'à la limite que
vous avez fixée.

goalify réfléchit d'abord. Il vérifie que le plan peut marcher. Il lit la doc. Il trouve les vrais
tests de votre projet. Il vous pose toutes ses questions au début, une seule fois. Ensuite l'IA
travaille seule, pendant des heures ou même des jours, sans que personne ait à répondre. À la fin,
elle vous montre une preuve.

Il marche mieux dans **Claude Code** et **Codex**. Les deux ont une commande `/goal` intégrée qui
fait continuer le travail. Dans Claude Code, un second vérificateur relit le travail après chaque
étape. Codex vérifie son propre travail par rapport à la même ligne d'arrivée. goalify s'installe
aussi dans plus de 70 autres outils d'IA. Là, vous obtenez le même plan et la même ligne d'arrivée,
et vous lancez le travail vous-même.

## Installation

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

N'importe quel autre outil d'IA qui lit les skills, en une ligne :

```bash
npx skills add Aboudjem/goalify
```

Tapez ensuite `/goalify` et décrivez le travail. Il vous faut Claude Code 2.1.139 ou plus récent.
Cette version a ajouté `/goal`.

<p align="center">
  <a href="https://goalify-kappa.vercel.app"><img src="../assets/goalify-demo.gif" alt="goalify en boucle : votre demande devient un objectif, toutes les questions viennent d'abord, l'IA travaille seule, et à la fin vous recevez une preuve." width="88%"></a>
  <br><sub><a href="../assets/goalify-promo.mp4">Voir la vidéo complète</a> · <a href="../assets/goalify-promo-vertical.mp4">vidéo verticale</a> · <a href="../assets/goalify-promo-15s.mp4">vidéo de 15 secondes</a></sub>
</p>

## Sans goalify, avec goalify

| Sans goalify | Avec goalify |
|:--|:--|
| L'IA s'arrête à 3 h du matin pour vous poser une question | Toutes les questions viennent d'abord, une seule fois |
| Le plan est perdu quand vous videz le chat | Le plan est gardé dans un fichier. L'IA le relit encore et encore |
| L'IA utilise un test que votre projet n'a pas | Les tests viennent de votre vrai projet |
| « Terminé ! » veut seulement dire que l'IA l'a dit | « Terminé » veut dire que la dernière étape montre les tests qui passent |
| Vous trouvez les problèmes le lendemain matin | `/goalify verify` relance les tests et vous donne un reçu |

## Comment ça marche

goalify prépare seulement le travail. C'est la commande `/goal` qui fait le travail. goalify s'assure
que l'IA n'a plus rien à demander.

1. **Les devoirs.** Est-ce que ça peut marcher ? goalify lit votre projet, la doc et vos tests. Il
   trouve les commandes qui montrent que le travail est vraiment fini.
2. **Des questions, une fois.** Il vous pose ensemble les quelques vrais choix. Après, il ne
   demande plus.
3. **Deux choses en sortent.** Le **brief** est un fichier avec le plan complet : vos choix, les
   fichiers exacts, l'ordre du travail. La **condition** est une ligne pour `/goal`. Elle dit à
   quoi ressemble la preuve. Une **page d'aperçu** s'ouvre aussi, pour que vous voyiez d'abord tout
   le plan.
4. **`/clear`, collez, partez.** Le travail démarre dans un chat propre, avec toute sa mémoire
   libre pour votre travail. Dans Claude Code, un second vérificateur relit le travail après chaque
   étape. Il laisse le travail s'arrêter seulement quand la preuve est là, ou quand il atteint
   votre limite d'étapes.
5. **Vérifiez plus tard.** `/goalify verify` relance les vérifications et écrit un reçu.

La ligne à coller ressemble à ceci. Elle est longue, alors copiez-la en entier :

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it, done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

Le chemin du brief est dans cette ligne. C'est important : le vérificateur derrière `/goal` ne peut
pas ouvrir de fichiers. Il lit seulement la ligne que vous collez et le chat. Alors ne donnez pas
à `/goal` seulement un chemin de fichier. Rien ne plante, mais rien n'est vérifié non plus. C'est
l'erreur la plus facile à faire :

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

<p align="center">
  <img src="../assets/hero.svg" alt="Quatre étapes : décrire le travail, recevoir un brief et une condition, coller la condition, revenir à la preuve." width="72%">
</p>

### Pourquoi ça peut travailler des jours

Un long travail d'IA échoue en général de deux façons. L'IA s'arrête pour vous demander quelque
chose. Ou elle dit « terminé » alors que quelque chose est encore cassé. goalify règle le premier
problème : il pose tout au début et écrit les réponses dans le brief. Il règle le second problème
avec la condition : à la fin, l'IA doit relancer chaque vérification, montrer le résultat et écrire
un mot spécial comme `ASYNC-OK`. Si l'IA a sauté le travail, elle devrait mentir. Près de sa limite
d'étapes, l'IA termine proprement et dit ce qu'il reste. Si elle s'arrête trop tôt, le brief garde
sa liste de contrôle. Collez la même ligne encore une fois pour continuer.

## Nouveautés de la 3.0

<p align="center">
  <img src="../assets/preview-and-receipt.svg" alt="La boucle 3.0 : un aperçu du plan avant, l'IA qui travaille seule, puis un reçu qui dit VERIFIED." width="88%">
</p>

- **Aperçu du plan.** Après chaque `/goalify`, une page s'ouvre dans votre navigateur. Elle montre
  les étapes, chaque vérification avec la commande qui la prouve, les limites, vos choix, et un
  bouton pour copier la ligne `/goal`. Elle vérifie aussi le brief et refuse d'afficher un brief
  cassé. La ligne `/goal` dans le chat reste l'étape principale. La page est un plus.
- **Reçus de preuve.** `/goalify verify` vous montre les vérifications, demande une fois, les lance
  et écrit un reçu : **VERIFIED**, **NOT VERIFIED** ou **UNVERIFIABLE**. Il peut dire « not
  verified » même quand l'IA a dit « terminé ». Il ne lance pas de commandes dangereuses, sauf si
  vous autorisez chacune.
- **De vrais tests, trouvés pour vous.** goalify lit `package.json`, `pyproject.toml`,
  `Cargo.toml`, `go.mod`, les Makefiles et vos fichiers de CI. Il ignore le faux test « no test
  specified » de npm. Ainsi la ligne d'arrivée n'utilise jamais un test qui ne peut pas passer. Il
  peut aussi lancer les tests une fois au départ.
- **Statut.** `/goalify status` liste chaque brief de `.goal/` : ouvert, bloqué ou terminé. Pour
  chaque brief ouvert, il montre la ligne `/goal` complète pour continuer.
- **Mode rapide.** `/goalify --quick <task>` est pour les travaux moyens. Il saute la recherche web
  et les questions, mais garde toutes les vérifications de sécurité. Si le travail peut vouloir dire
  deux choses différentes, il s'arrête et vous demande d'utiliser le mode complet.
- **Doctor.** `/goalify doctor` liste chaque copie de goalify sur votre ordinateur. Il vous prévient
  quand une ancienne copie est chargée à côté de la nouvelle.
- **Copier-coller plus sûr.** La condition ne peut plus contenir d'accents graves ni de guillemets
  doubles. Ainsi la ligne `claude -p "/goal ..."` ne peut pas lancer une commande cachée quand vous
  la collez. Merci à [@Hug0x0](https://github.com/Hug0x0) pour ce correctif.

## Comparaison

Des différences simples, vérifiées dans le README de chaque projet en novembre 2026.

| Outil | Ce que c'est | En quoi il est différent de goalify |
|:--|:--|:--|
| [supergoal](https://github.com/robzilla1738/supergoal) | Un plugin Claude Code. Il explore, pose des questions, planifie par phases et donne une commande à `/goal`. À la fin, il vérifie le résultat par rapport au plan | L'outil le plus proche. goalify écrit un brief complet et une condition vérifiée, montre une page d'aperçu avant le travail, et écrit un reçu de preuve après |
| Boucles Ralph ([snarktank/ralph](https://github.com/snarktank/ralph) et d'autres) | Une boucle qui donne à l'IA le même prompt encore et encore | Elle s'arrête en général sur un mot que l'IA écrit, ou après un certain nombre de tours. Avec le `/goal` de Claude Code, un second vérificateur relit le travail à chaque étape |
| [Spec Kit](https://github.com/github/spec-kit) | La boîte à outils de GitHub pour écrire une spec, un plan et des tâches | Très bien pour écrire la spec. goalify sert pour le long travail sans personne devant l'écran, et pour prouver qu'il est fini |

## Fonctionne dans votre outil d'IA

| Outil | Installation en une ligne |
|:--|:--|
| Claude Code | `claude plugin install goalify@10x` |
| N'importe lequel des 70 outils d'IA et plus | `npx skills add Aboudjem/goalify` |
| Cursor, Codex, Copilot, Gemini CLI, OpenCode | `npx skills add Aboudjem/goalify -a <agent>` |
| Tout le reste | les codes et les dossiers dans [docs/editors.md](../docs/editors.md) |

`/clear` et `/goal` sont des commandes de Claude Code. Dans les autres outils, ouvrez un nouveau chat
à la place de `/clear`, et donnez à l'IA la condition comme tâche principale. Codex a son propre
`/goal`. Voyez [goalify dans Codex](../docs/codex.md) pour ce qui marche pareil et ce qui ne marche
pas pareil.

<details>
<summary>Installer à la main</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

Il vous faut seulement ce dossier. Le [démarrage rapide](../docs/quickstart.md) explique le
reste. Si vous aviez une ancienne copie, lancez `/goalify doctor` pour vérifier qu'une seule copie
est chargée.

</details>

## Bon à savoir

> [!IMPORTANT]
> Quand un travail s'arrête, il n'est pas toujours fini. Le vérificateur décide tout seul. Il peut
> aussi arrêter le travail s'il pense que l'objectif est impossible à atteindre. Avant de croire un
> résultat vert, lancez `/goalify verify` sur le brief, ou lancez vous-même ses vérifications.

- **goalify ne fait jamais le travail lui-même.** Il écrit le brief et la condition. Il lance vos
  vérifications seulement si vous le demandez.
- **Rien n'est envoyé nulle part.** Pas de serveur, pas de paquets en plus, pas d'appels réseau. Les
  scripts d'aide utilisent seulement le Python standard, et la page d'aperçu ne charge rien depuis
  internet.
- **Pas de devinette de prix.** goalify ne devine jamais un coût en argent ou en tokens. Votre
  limite d'étapes est votre contrôle.
- **Tout ce qu'il ne promet pas** est listé dans [les limites honnêtes](../docs/limits.md).

## En savoir plus

- [Site web](https://goalify-kappa.vercel.app) · [Démarrage rapide](../docs/quickstart.md) · [FAQ](../docs/faq.md)
- [Exemples de conditions](../examples/conditions.md) : des bonnes et des mauvaises, et ce que perd chaque mauvaise.
- [Un exemple complet](../examples/sample-brief.md) : un vrai brief et sa condition, plus
  [sa page d'aperçu](../examples/sample-brief.html) (téléchargez-la et ouvrez-la dans un navigateur).
- [Installer dans votre outil d'IA](../docs/editors.md) · [goalify dans Codex](../docs/codex.md) · [Limites honnêtes](../docs/limits.md)
- [Journal des modifications](../CHANGELOG.md) · [Le skill lui-même](../skills/goalify/SKILL.md) · [Licence](../LICENSE)

---

<sub>Fait par <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. Licence MIT. Les faits sur `/goal`
sont vérifiés avec Claude Code 2.1.317 et sa doc, novembre 2026.
<a href="https://github.com/Aboudjem/goalify/issues">Un problème ?</a></sub>

<sub>Traduction assistée par machine. La version de référence est le <a href="../README.md">README.md</a> en anglais.</sub>
