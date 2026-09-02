<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-light.svg">
    <img src="../assets/hero-dark.svg" alt="goalify：自主运行的准备工作。回来看到的是证据，不是承诺。" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="校验"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=8E7BFF" alt="MIT 许可证"></a>
  <a href="https://github.com/Aboudjem/goalify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/goalify?color=8E7BFF" alt="GitHub 星标"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <b>简体中文</b> · <a href="ja.md">日本語</a> · <a href="es.md">Español</a> · <a href="fr.md">Français</a>
</p>

<p align="center">
  <strong>把一件大活交给 Claude。回来时看到的是它做完了的证据，而不是一句做完了的承诺。</strong>
</p>

<p align="center">
  <a href="#它做什么">它做什么</a> · <a href="#安装">安装</a> · <a href="#怎么用">怎么用</a> · <a href="#你会得到什么">你会得到什么</a> · <a href="#在你的编辑器里可用">在你的编辑器里可用</a> · <a href="#需要知道的事">需要知道的事</a>
</p>

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

## 它做什么

有些活太大，你没法坐在旁边一直盯着。把一个名字改遍几百个文件。把一个旧项目迁到它所依赖的代码的新版本上。把一个乱糟糟的项目里某一类问题清理干净。趁 Claude 还带着你的上下文，你把这件活描述一遍，goalify 就把这次运行要做什么、做到什么样才算完成写下来。然后它给你一行字，让你粘贴。

- **简报**是一个文件，里面装着这次运行需要的一切：你的决定、准确的路径、做事的顺序。
- **条件**是你粘贴到 `/goal` 里的那一行。`/goal` 是 Claude Code 内置的停止检查，它让会话一直干下去，并且每一轮都对照这一行来判断。

想象一个建筑工地。简报是施工方照着干活的图纸。条件是验收方签字用的清单，而这位验收方从不看图纸，也从不去工地。他们只判断施工方拿出来的证据。

## 安装

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

其他任何智能体，一行搞定：

```bash
npx skills add Aboudjem/goalify
```

<details>
<summary>手动复制安装</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

运行时不需要仓库里的其他任何东西。请用 Claude Code 2.1.139 或更新的版本，因为 `/goal` 是在那个版本里发布的。其余内容见[快速上手](../docs/quickstart.md)。
</details>

## 怎么用

**1. 描述这件活。** 在 Claude Code 里运行 `/goalify` 加上你的任务。goalify 会读你的项目，就那几个真正需要你拍板的问题问你，然后写出简报并打印出条件。

```text
/goalify migrate our API to async/await
    Brief:     ~/acme/.goal/api-migration.md
    Condition: 149 chars, under the 4,000 limit
```

**2. 清空对话。** `/clear` 会清掉这段对话，这样运行从头开始，注意力全部集中。

**3. 粘贴条件。** 整整一行。它在屏幕上会折行，所以要全部选中。

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it - done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

简报的路径就写在这一行里面，因为 `/goal` 背后的评估器没有工具，打不开文件。它读到的是你粘贴的那一行，以及这次运行被截短后的对话记录，从来看不到简报本身。只把路径丢给它不会报任何错，也证明不了任何事，所以这是最容易犯的错：

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

粘贴前拿不准这一行？
`python3 skills/goalify/scripts/condition_lint.py "<your condition>"` 会对照六条机械规则检查它，并指出没通过的是哪几条。需要拿主意的部分仍然归你。

<p align="center">
  <img src="../assets/hero.svg" alt="四步：描述这件活，拿到简报和条件，粘贴条件，回来看到证据。" width="72%">
</p>

## 你会得到什么

- **只需交出一行。** 清空对话，粘贴一行，然后走开。
- **你的上下文能挺过这次重置。** 简报把你的决定带进新的会话。
- **进度一眼就能看到。** 运行会在简报里的清单上边做边打勾。
- **要的是证据，不是承诺。** 最后一轮必须引用检查通过的输出，并打印一个自造的词，也就是上面的 `ASYNC-OK`，所以一次跳过了工作的运行只能靠彻底撒谎才能蒙混过关。
- **到了上限也收得干净。** 快到轮次上限时，运行会停止开新的工作，把做了一半的收尾或还原，并在最终报告里说明它提前停了。
- **停下也保住进度。** 简报留在原处，清单完好。你粘贴同一行就能接着做，而不是从头再来。
- **只有成功才归档。** 收尾那一轮会把每一项检查重跑一遍、引用输出，并把简报移进 `.goal/done/`，这个文件移动在任何文件管理器里都看得见。

## 在你的编辑器里可用

通过 `npx skills add`，它可以在 Claude Code、Cursor、Codex、Copilot、Gemini CLI 以及另外 70 多个智能体里使用。这个技能就是纯 Markdown，里面没有任何东西被绑死在某一个模型上。

| 智能体 | 一行安装 |
|:--|:--|
| Claude Code | `claude plugin install goalify@10x` |
| 70 多个智能体中的任意一个 | `npx skills add Aboudjem/goalify` |
| Cursor、Codex、Copilot、Gemini CLI、OpenCode | `npx skills add Aboudjem/goalify -a <agent>` |
| 其他所有 | [docs/editors.md](../docs/editors.md) 里的智能体代码和安装路径 |

`/clear` 和 `/goal` 是 Claude Code 的命令。在别处，用新开一个会话来代替 `/clear`，并把条件作为长期目标交给它。Codex 有它自己的 `/goal`，[在 Codex 下运行](../docs/codex.md)讲清楚了哪些能带过去、哪些不能。

## 需要知道的事

> [!IMPORTANT]
> 运行停下来了，并不等于它做完了。评估器自己做判断，也可能因为认定终点已经够不着而结束一次运行。在你相信一个绿色结果之前，请重读收尾时的证据，也就是最后一条回复里引用的检查输出以及被移进 `.goal/done/` 的简报，或者自己把这些检查重跑一遍。

- **goalify 只负责写，从不执行。** 它在当前会话里写出这两份产物就停下。运行由你来启动。
- **没有任何东西在后台跑。** 一个 Markdown 技能，没有服务端，没有要装的依赖，它自己也不发网络请求。
- **它不承诺的每一件事**都写在[诚实的边界](../docs/limits.md)里。

## 了解更多

- [快速上手](../docs/quickstart.md)，一次完整的运行，外加其他几种安装方式。
- [条件写法示例](../examples/conditions.md)，八条值得照着写的和八条别那么写的，每一条都说明了差的那条丢了什么。
- [一个完整示例](../examples/sample-brief.md)，一份真实的简报以及由它推导出的条件。
- [在你的编辑器里安装](../docs/editors.md) · [常见问题](../docs/faq.md) · [在 Codex 下运行](../docs/codex.md)
- [诚实的边界](../docs/limits.md) · [更新日志](../CHANGELOG.md) · [技能本身](../skills/goalify/SKILL.md) · [许可证](../LICENSE)

<p align="center"><sub><a href="../assets/goalify-teaser.mp4">观看 28 秒预告</a> · <a href="../assets/goalify-teaser.gif">GIF</a></sub></p>

---

<sub>由 <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> 制作。MIT 许可证。`/goal` 的行为是 2026 年从发布的 Claude Code 2.1.223 二进制文件中重新推导出来的。<a href="https://github.com/Aboudjem/goalify/issues">发现遗漏？</a></sub>

<sub>本译文由机器辅助翻译，以英文版 <a href="../README.md">README.md</a> 为准。</sub>
