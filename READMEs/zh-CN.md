<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-light.svg">
    <img src="../assets/hero-dark.svg" alt="goalify：把大活交给你的 AI，拿回证据。" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="校验"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=9b6bff" alt="MIT 许可证"></a>
  <a href="https://github.com/Aboudjem/goalify/releases"><img src="https://img.shields.io/github/v/release/Aboudjem/goalify?color=2ee6ff" alt="最新版本"></a>
  <a href="https://github.com/Aboudjem/goalify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/goalify?color=ff3d9a" alt="GitHub 星标"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <b>简体中文</b> · <a href="ja.md">日本語</a> · <a href="es.md">Español</a> · <a href="fr.md">Français</a>
</p>

<p align="center">
  <strong>把一件大活交给你的 AI。拿回证据。</strong>
</p>

<p align="center">
  <a href="https://goalify-kappa.vercel.app">网站</a> · <a href="#安装">安装</a> · <a href="#它是怎么工作的">它是怎么工作的</a> · <a href="#30-新特性">3.0 新特性</a> · <a href="#和同类工具比">和同类工具比</a> · <a href="#需要知道的事">需要知道的事</a>
</p>

goalify 把你的请求变成一个**目标**。目标就是一条清楚的终点线。AI 会一直干下去，直到目标完成并且被证明，或者到了你设的上限。

goalify 先动脑。它先确认计划行得通，读文档，找出你项目里真正的测试。它把所有问题在一开始一次问完。然后 AI 自己干，干几个小时，甚至几天，不需要任何人回答。最后，它给你看证据。

它在 **Claude Code** 和 **Codex** 里效果最好。两者都内置了 `/goal` 命令，能让工作一直继续。在 Claude Code 里，第二个检查员会在每一步之后读一遍工作成果。Codex 则对照同一条终点线，自己检查自己的工作。goalify 也能装进另外 70 多个 AI 工具。在那里你得到同样的计划和终点线，工作由你自己来启动。

## 安装

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

其他任何能读技能的 AI 工具，一行搞定：

```bash
npx skills add Aboudjem/goalify
```

然后输入 `/goalify`，描述这件活。你需要 Claude Code 2.1.139 或更新的版本。那个版本加入了 `/goal`。

<p align="center">
  <a href="https://goalify-kappa.vercel.app"><img src="../assets/goalify-demo.gif" alt="循环中的 goalify：你的请求变成目标，所有问题先问完，AI 自己干活，最后你拿到证据。" width="88%"></a>
  <br><sub><a href="../assets/goalify-promo.mp4">观看完整视频</a> · <a href="../assets/goalify-promo-vertical.mp4">竖屏视频</a> · <a href="../assets/goalify-promo-30s.mp4">30 秒视频</a> · <a href="../assets/goalify-promo-15s.mp4">15 秒视频</a></sub>
</p>

## 没有 goalify，有了 goalify

| 没有 goalify | 有了 goalify |
|:--|:--|
| AI 凌晨 3 点停下来问你问题 | 所有问题先问，只问一次 |
| 清空聊天，计划就丢了 | 计划存在一个文件里。AI 会一遍遍重读 |
| AI 用了你的项目里根本没有的测试 | 测试来自你真正的项目 |
| 「搞定了！」只是 AI 自己这么说 | 「搞定」的意思是最后一步显示测试通过 |
| 第二天早上你才发现问题 | `/goalify verify` 重新跑测试，并给你一份回执 |

## 它是怎么工作的

goalify 只负责准备。真正干活的是 `/goal` 命令。goalify 要保证 AI 没有任何需要再问的事。

1. **先做功课。** 行得通吗？goalify 读你的项目、文档和测试，找出真正能说明这件活做完了的命令。
2. **问题只问一次。** 它把那几个真正要你选的问题放在一起问。之后不再问。
3. **产出两样东西。** **简报**是一个文件，装着完整的计划：你的选择、准确的文件、做事的顺序。**条件**是给 `/goal` 的一行，说明证据长什么样。还会打开一个**预览页面**，让你先看到整个计划。
4. **`/clear`，粘贴，走开。** 工作在一个干净的聊天里开始，所有记忆都留给你的活。在 Claude Code 里，第二个检查员会在每一步之后读一遍工作成果。只有证据到位，或者到了你设的步数上限，它才允许工作停下。
5. **之后再核对。** `/goalify verify` 重新跑一遍检查，并写出一份回执。

你要粘贴的那一行长这样。它很长，所以要全部复制：

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it, done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

简报的路径就在这一行里面。这一点很重要：`/goal` 背后的检查员打不开文件。它只读你粘贴的那一行和聊天内容。所以不要只给 `/goal` 一个文件路径。什么都不会坏，但什么也不会被检查。这是最容易犯的错：

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

<p align="center">
  <img src="../assets/hero.svg" alt="四步：描述这件活，拿到简报和条件，粘贴条件，回来看到证据。" width="72%">
</p>

### 为什么它能干上好几天

AI 的长时间工作通常以两种方式失败。一种是 AI 停下来问你问题。另一种是东西还坏着，它却说「做完了」。goalify 解决第一个问题的办法是：一开始就把所有问题问完，并把答案写进简报。它解决第二个问题的办法是条件：最后 AI 必须把每一项检查再跑一遍，给出结果，并写出一个特别的词，比如 `ASYNC-OK`。如果 AI 跳过了工作，它就只能撒谎。接近步数上限时，AI 会干净地收尾，并说明还剩什么。如果它提前停了，简报里还留着清单。再粘贴同一行，就能接着干。

## 3.0 新特性

<p align="center">
  <img src="../assets/preview-and-receipt.svg" alt="3.0 的循环：先看计划预览，AI 自己干活，然后是写着 VERIFIED 的回执。" width="88%">
</p>

- **计划预览。** 每次 `/goalify` 之后，浏览器里会打开一个页面。它显示各个步骤、每项检查和证明它的命令、上限、你的选择，还有一个复制 `/goal` 那一行的按钮。它还会检查简报，并拒绝显示有问题的简报。聊天里的那行 `/goal` 仍然是主要的一步。这个页面只是额外的。
- **证据回执。** `/goalify verify` 会给你看这些检查，问你一次，然后运行它们，并写出一份回执：**VERIFIED**、**NOT VERIFIED** 或 **UNVERIFIABLE**。即使 AI 说了「做完了」，它也可以说「没有验证通过」。除非你逐条允许，否则它不会运行危险的命令。
- **真正的测试，替你找出来。** goalify 会读 `package.json`、`pyproject.toml`、`Cargo.toml`、`go.mod`、Makefile 和你的 CI 文件。它会跳过 npm 那个空的「no test specified」测试。所以终点线上绝不会出现一个根本通不过的测试。它也可以在一开始先把测试跑一遍。
- **状态。** `/goalify status` 列出 `.goal/` 里的每一份简报：进行中、被阻塞或已完成。对每个进行中的简报，它会显示完整的 `/goal` 那一行，方便接着做。
- **快速模式。** `/goalify --quick <task>` 适合中等规模的活。它跳过网络调研和提问，但保留所有安全检查。如果这件活可能有两种不同的理解，它会停下来，请你改用完整模式。
- **Doctor。** `/goalify doctor` 列出你电脑上每一份 goalify 副本。如果旧副本和新副本同时被加载，它会提醒你。
- **更安全的复制粘贴。** 条件里不能再带反引号或双引号。所以你粘贴 `claude -p "/goal ..."` 那一行时，不会运行任何隐藏的命令。感谢 [@Hug0x0](https://github.com/Hug0x0) 的修复。

## 和同类工具比

只讲明白的差别，2026 年 11 月对照各项目的 README 核对过。

| 工具 | 它是什么 | 和 goalify 有什么不同 |
|:--|:--|:--|
| [supergoal](https://github.com/robzilla1738/supergoal) | 一个 Claude Code 插件。它先探查，再提问，分阶段做计划，给 `/goal` 一条命令。最后它对照计划检查结果 | 最接近的工具。goalify 写出一份完整的简报和一条经过检查的条件，干活前给你看预览页面，干活后写一份证据回执 |
| Ralph 循环（[snarktank/ralph](https://github.com/snarktank/ralph) 等） | 一个把同一个提示词一遍又一遍交给 AI 的循环 | 通常靠 AI 写出的某个词，或者靠轮数上限来停。用 Claude Code 的 `/goal` 时，由第二个检查员每一步读一遍工作成果 |
| [Spec Kit](https://github.com/github/spec-kit) | GitHub 的工具包，用来写规范、计划和任务 | 很适合用来写规范。goalify 管的是没人盯着的长时间工作，以及证明它真的做完了 |

## 在你的 AI 工具里可用

| 工具 | 一行安装 |
|:--|:--|
| Claude Code | `claude plugin install goalify@10x` |
| 70 多个 AI 工具中的任意一个 | `npx skills add Aboudjem/goalify` |
| Cursor, Codex, Copilot, Gemini CLI, OpenCode | `npx skills add Aboudjem/goalify -a <agent>` |
| 其他所有 | [docs/editors.md](../docs/editors.md) 里的代码和文件夹 |

`/clear` 和 `/goal` 是 Claude Code 的命令。在其他工具里，用新开一个聊天来代替 `/clear`，并把条件作为主要任务交给 AI。Codex 有它自己的 `/goal`。哪些做法一样、哪些不一样，请看 [Codex 里的 goalify](../docs/codex.md)。

<details>
<summary>手动安装</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

你只需要那一个文件夹。其余内容见[快速上手](../docs/quickstart.md)。如果你以前装过旧版本，运行 `/goalify doctor`，确认只加载了一份。

</details>

## 需要知道的事

> [!IMPORTANT]
> 工作停下来了，不一定就做完了。检查员自己做判断。如果它认为目标够不着，也可能让工作停下。在你相信一个绿色结果之前，请对简报运行 `/goalify verify`，或者自己把它的检查跑一遍。

- **goalify 从不自己做这件活。** 它写简报和条件。只有你要求时，它才运行你的检查。
- **不会往任何地方发送东西。** 没有服务端，没有额外的包，没有网络请求。辅助脚本只用标准的 Python，预览页面也不从互联网加载任何东西。
- **不瞎猜价格。** goalify 从不猜测要花多少钱或多少 token。步数上限由你来掌控。
- **它不承诺的每一件事**都列在[诚实的边界](../docs/limits.md)里。

## 了解更多

- [网站](https://goalify-kappa.vercel.app) · [快速上手](../docs/quickstart.md) · [常见问题](../docs/faq.md)
- [条件示例](../examples/conditions.md)：有好的也有差的，每一条差的都说明了它丢了什么。
- [一个完整示例](../examples/sample-brief.md)：一份真实的简报和它的条件，外加[它的预览页面](../examples/sample-brief.html)（下载后用浏览器打开）。
- [在你的 AI 工具里安装](../docs/editors.md) · [Codex 里的 goalify](../docs/codex.md) · [诚实的边界](../docs/limits.md)
- [更新日志](../CHANGELOG.md) · [技能本身](../skills/goalify/SKILL.md) · [许可证](../LICENSE)

---

<sub>由 <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> 制作。MIT 许可证。关于 `/goal` 的事实已对照 Claude Code 2.1.317 及其文档核对，2026 年 11 月。<a href="https://github.com/Aboudjem/goalify/issues">发现问题？</a></sub>

<sub>本译文由机器辅助翻译，以英文版 <a href="../README.md">README.md</a> 为准。</sub>
