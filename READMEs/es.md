<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-light.svg">
    <img src="../assets/hero-dark.svg" alt="goalify: dale un trabajo grande a tu IA y recibe una prueba." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="validación"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=9b6bff" alt="licencia MIT"></a>
  <a href="https://github.com/Aboudjem/goalify/releases"><img src="https://img.shields.io/github/v/release/Aboudjem/goalify?color=2ee6ff" alt="última versión"></a>
  <a href="https://github.com/Aboudjem/goalify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/goalify?color=ff3d9a" alt="estrellas en GitHub"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <a href="ja.md">日本語</a> · <b>Español</b> · <a href="fr.md">Français</a>
</p>

<p align="center">
  <strong>Dale un trabajo grande a tu IA. Recibe una prueba.</strong>
</p>

<p align="center">
  <a href="https://goalify-kappa.vercel.app">Sitio web</a> · <a href="#instalación">Instalación</a> · <a href="#cómo-funciona">Cómo funciona</a> · <a href="#novedades-de-la-30">Novedades de la 3.0</a> · <a href="#cómo-se-compara">Cómo se compara</a> · <a href="#conviene-saber">Conviene saber</a>
</p>

goalify convierte tu petición en un **objetivo**. Un objetivo es una meta clara. La IA sigue
trabajando hasta que el objetivo está hecho y probado, o hasta que llega al límite que tú pusiste.

goalify piensa primero. Comprueba que el plan puede funcionar. Lee la documentación. Encuentra los
tests reales de tu proyecto. Te hace todas sus preguntas al principio, una sola vez. Después la IA
trabaja sola, durante horas o incluso días, y nadie tiene que responder nada. Al final, te
enseña una prueba.

Funciona mejor en **Claude Code** y **Codex**. Los dos tienen un comando `/goal` integrado que
mantiene el trabajo en marcha. En Claude Code, un segundo revisor lee el trabajo después de cada
paso. Codex revisa su propio trabajo frente a la misma meta. goalify también se instala en más de
70 otras herramientas de IA. Ahí obtienes el mismo plan y la misma meta, y empiezas el trabajo tú.

## Instalación

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

Cualquier otra herramienta de IA que lea skills, en una línea:

```bash
npx skills add Aboudjem/goalify
```

Después escribe `/goalify` y describe el trabajo. Necesitas Claude Code 2.1.139 o más nuevo. Esa
versión añadió `/goal`.

<p align="center">
  <a href="https://goalify-kappa.vercel.app"><img src="../assets/goalify-demo.gif" alt="goalify en bucle: tu petición se convierte en un objetivo, primero van todas las preguntas, la IA trabaja sola y al final recibes una prueba." width="88%"></a>
  <br><sub><a href="../assets/goalify-promo.mp4">Ver el vídeo completo</a> · <a href="../assets/goalify-promo-vertical.mp4">vídeo vertical</a> · <a href="../assets/goalify-promo-30s.mp4">vídeo de 30 segundos</a> · <a href="../assets/goalify-promo-15s.mp4">vídeo de 15 segundos</a></sub>
</p>

## Sin goalify, con goalify

| Sin goalify | Con goalify |
|:--|:--|
| La IA para a las 3 de la mañana para hacerte una pregunta | Todas las preguntas van primero, una sola vez |
| El plan se pierde cuando borras el chat | El plan se guarda en un archivo. La IA lo lee una y otra vez |
| La IA usa un test que tu proyecto no tiene | Los tests salen de tu proyecto real |
| «¡Hecho!» solo significa que la IA lo dijo | «Hecho» significa que el último paso muestra los tests pasando |
| Encuentras los problemas a la mañana siguiente | `/goalify verify` repite los tests y te da un recibo |

## Cómo funciona

goalify solo prepara el trabajo. El comando `/goal` hace el trabajo. goalify se asegura de que la IA
no tenga nada más que preguntar.

1. **Los deberes.** ¿Puede funcionar? goalify lee tu proyecto, la documentación y tus tests.
   Encuentra los comandos que muestran que el trabajo está de verdad terminado.
2. **Preguntas, una vez.** Te hace juntas las pocas decisiones reales. Después no vuelve a
   preguntar.
3. **Salen dos cosas.** El **informe** es un archivo con el plan completo: tus decisiones, los
   archivos exactos, el orden del trabajo. La **condición** es una línea para `/goal`. Dice cómo es
   la prueba. También se abre una **página de vista previa**, para que veas antes todo el plan.
4. **`/clear`, pega y márchate.** El trabajo empieza en un chat limpio, con toda su memoria libre
   para tu trabajo. En Claude Code, un segundo revisor lee el trabajo después de cada paso. Solo
   deja que el trabajo pare cuando la prueba está ahí, o cuando llega a tu límite de pasos.
5. **Compruébalo después.** `/goalify verify` repite las comprobaciones y escribe un recibo.

La línea que pegas se ve así. Es larga, así que cópiala entera:

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it, done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

La ruta del informe está dentro de esa línea. Esto es importante: el revisor que hay detrás de
`/goal` no puede abrir archivos. Solo lee la línea que pegas y el chat. Así que no le des a `/goal`
solo la ruta de un archivo. No se rompe nada, pero tampoco se comprueba nada. Es el error más fácil
de cometer:

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

<p align="center">
  <img src="../assets/hero.svg" alt="Cuatro pasos: describe el trabajo, recibe un informe y una condición, pega la condición, vuelve a la prueba." width="72%">
</p>

### Por qué puede trabajar durante días

Un trabajo largo de IA suele fallar de dos maneras. La IA para para preguntarte algo. O dice
«hecho» cuando algo sigue roto. goalify arregla el primer problema: lo pregunta todo al principio y
escribe las respuestas en el informe. Arregla el segundo problema con la condición: al final, la IA
tiene que repetir cada comprobación, enseñar el resultado y escribir una palabra especial como
`ASYNC-OK`. Si la IA se saltó el trabajo, tendría que mentir. Cerca de su límite de pasos, la IA
termina con orden y dice lo que queda. Si para antes de tiempo, el informe guarda su lista. Pega la
misma línea otra vez para continuar.

## Novedades de la 3.0

<p align="center">
  <img src="../assets/preview-and-receipt.svg" alt="El bucle 3.0: una vista previa del plan antes, la IA trabajando sola y después un recibo que dice VERIFIED." width="88%">
</p>

- **Vista previa del plan.** Después de cada `/goalify`, se abre una página en tu navegador. Muestra
  los pasos, cada comprobación con el comando que la prueba, los límites, tus decisiones y un botón
  para copiar la línea `/goal`. También revisa el informe y se niega a mostrar uno roto. La línea
  `/goal` del chat sigue siendo el paso principal. La página es un extra.
- **Recibos de prueba.** `/goalify verify` te muestra las comprobaciones, pregunta una vez, las
  ejecuta y escribe un recibo: **VERIFIED**, **NOT VERIFIED** o **UNVERIFIABLE**. Puede decir «not
  verified» aunque la IA haya dicho «hecho». No ejecuta comandos peligrosos si no permites cada uno.
- **Tests reales, encontrados por ti.** goalify lee `package.json`, `pyproject.toml`, `Cargo.toml`,
  `go.mod`, los Makefiles y tus archivos de CI. Se salta el test vacío «no test specified» de npm.
  Así la meta nunca usa un test que no puede pasar. También puede ejecutar los tests una vez al
  principio.
- **Estado.** `/goalify status` lista cada informe de `.goal/`: abierto, bloqueado o terminado. Para
  cada informe abierto, muestra la línea `/goal` completa para continuar.
- **Modo rápido.** `/goalify --quick <task>` es para trabajos medianos. Se salta la búsqueda web y
  las preguntas, pero mantiene todas las comprobaciones de seguridad. Si el trabajo puede significar
  dos cosas distintas, se detiene y te pide usar el modo completo.
- **Doctor.** `/goalify doctor` lista cada copia de goalify en tu ordenador. Te avisa cuando una copia
  antigua está cargada junto a la nueva.
- **Copiar y pegar más seguro.** La condición ya no puede llevar acentos graves ni comillas dobles.
  Así la línea `claude -p "/goal ..."` no puede ejecutar un comando oculto cuando la pegas. Gracias
  a [@Hug0x0](https://github.com/Hug0x0) por este arreglo.

## Cómo se compara

Diferencias simples, comprobadas con el README de cada proyecto en noviembre de 2026.

| Herramienta | Qué es | En qué se diferencia de goalify |
|:--|:--|:--|
| [supergoal](https://github.com/robzilla1738/supergoal) | Un plugin de Claude Code. Explora, pregunta, planifica por fases y le da un comando a `/goal`. Al final comprueba el resultado frente al plan | La herramienta más cercana. goalify escribe un informe completo y una condición revisada, muestra una página de vista previa antes del trabajo y escribe un recibo de prueba después |
| Bucles Ralph ([snarktank/ralph](https://github.com/snarktank/ralph) y otros) | Un bucle que le da a la IA el mismo prompt una y otra vez | Suele parar con una palabra que escribe la IA, o después de cierto número de vueltas. Con el `/goal` de Claude Code, un segundo revisor lee el trabajo en cada paso |
| [Spec Kit](https://github.com/github/spec-kit) | El kit de GitHub para escribir una especificación, un plan y tareas | Genial para escribir la especificación. goalify es para el trabajo largo sin nadie mirando, y para probar que está terminado |

## Funciona en tu herramienta de IA

| Herramienta | Instalación en una línea |
|:--|:--|
| Claude Code | `claude plugin install goalify@10x` |
| Cualquiera de las más de 70 herramientas de IA | `npx skills add Aboudjem/goalify` |
| Cursor, Codex, Copilot, Gemini CLI, OpenCode | `npx skills add Aboudjem/goalify -a <agent>` |
| Todo lo demás | los códigos y las carpetas en [docs/editors.md](../docs/editors.md) |

`/clear` y `/goal` son comandos de Claude Code. En otras herramientas, empieza un chat nuevo en lugar
de `/clear`, y dale a la IA la condición como tarea principal. Codex tiene su propio `/goal`. Mira
[goalify en Codex](../docs/codex.md) para saber qué funciona igual y qué no.

<details>
<summary>Instalar a mano</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

Solo necesitas esa carpeta. La [guía rápida](../docs/quickstart.md) explica el resto. Si tenías una
copia antigua, ejecuta `/goalify doctor` para asegurarte de que solo hay una copia cargada.

</details>

## Conviene saber

> [!IMPORTANT]
> Cuando un trabajo para, no siempre está terminado. El revisor decide por su cuenta. También puede
> parar el trabajo si cree que la meta no se puede alcanzar. Antes de fiarte de un resultado en
> verde, ejecuta `/goalify verify` sobre el informe, o ejecuta tú mismo sus comprobaciones.

- **goalify nunca hace el trabajo él mismo.** Escribe el informe y la condición. Ejecuta tus
  comprobaciones solo cuando se lo pides.
- **No se envía nada a ningún sitio.** Sin servidor, sin paquetes extra, sin llamadas de red. Los
  scripts de ayuda usan solo Python estándar, y la página de vista previa no carga nada de internet.
- **Sin adivinar precios.** goalify nunca adivina un coste en dinero o en tokens. Tu límite de pasos
  es tu control.
- **Todo lo que no promete** está en la lista de [límites honestos](../docs/limits.md).

## Más información

- [Sitio web](https://goalify-kappa.vercel.app) · [Guía rápida](../docs/quickstart.md) · [Preguntas frecuentes](../docs/faq.md)
- [Condiciones de ejemplo](../examples/conditions.md): buenas y malas, y lo que pierde cada mala.
- [Un ejemplo completo](../examples/sample-brief.md): un informe real y su condición, más
  [su página de vista previa](../examples/sample-brief.html) (descárgala y ábrela en un navegador).
- [Instalar en tu herramienta de IA](../docs/editors.md) · [goalify en Codex](../docs/codex.md) · [Límites honestos](../docs/limits.md)
- [Registro de cambios](../CHANGELOG.md) · [El skill en sí](../skills/goalify/SKILL.md) · [Licencia](../LICENSE)

---

<sub>Hecho por <a href="https://github.com/Aboudjem">Adam Boudjemaa</a>. Licencia MIT. Los datos sobre `/goal`
están comprobados con Claude Code 2.1.317 y su documentación, noviembre de 2026.
<a href="https://github.com/Aboudjem/goalify/issues">¿Ves un problema?</a></sub>

<sub>Traducción asistida por máquina. La versión de referencia es el <a href="../README.md">README.md</a> en inglés.</sub>
