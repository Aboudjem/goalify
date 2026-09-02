<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-light.svg">
    <img src="../assets/hero-dark.svg" alt="goalify: 自律実行の下ごしらえ。戻ってきたときに待っているのは約束ではなく証拠。" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="検証"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=8E7BFF" alt="MIT ライセンス"></a>
  <a href="https://github.com/Aboudjem/goalify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/goalify?color=8E7BFF" alt="GitHub スター"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <b>日本語</b> · <a href="es.md">Español</a> · <a href="fr.md">Français</a>
</p>

<p align="center">
  <strong>大きな仕事を Claude に渡す。戻ってきたら、終わったという約束ではなく、終わった証拠が待っている。</strong>
</p>

<p align="center">
  <a href="#何をするか">何をするか</a> · <a href="#インストール">インストール</a> · <a href="#使い方">使い方</a> · <a href="#得られるもの">得られるもの</a> · <a href="#お使いのエディタで動く">お使いのエディタで動く</a> · <a href="#知っておくこと">知っておくこと</a>
</p>

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

## 何をするか

そばに座って見ていられないほど大きな仕事があります。ひとつの名前を数百のファイルにわたって変える。古いプロジェクトを、その土台となるコードの新しいバージョンへ載せ替える。散らかったプロジェクトを通しで見て、ある一種類の問題だけを片づける。Claude がまだあなたの文脈を持っているうちに、あなたは仕事を説明します。goalify は、その実行が何をしなければならないか、そして完了とはどういう状態かを書き留めます。そして貼り付ける一行を渡してきます。

- **ブリーフ**はファイルです。あなたの決定、正確なパス、作業の順序など、実行に必要なものがすべて入っています。
- **条件**は `/goal` に貼り付ける一行です。`/goal` は Claude Code に組み込まれた停止判定で、セッションを走らせ続け、毎ターンその一行に照らして判定します。

建築現場を思い浮かべてください。ブリーフは施工者が見ながら作業する図面です。条件は検査者が承認に使うチェックリストで、その検査者は図面を読まず、現場にも来ません。施工者が示した証拠だけを見て判断します。

## インストール

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

ほかのエージェントなら、一行で済みます。

```bash
npx skills add Aboudjem/goalify
```

<details>
<summary>手動でコピーして入れる</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

実行時にリポジトリのほかの部分は一切必要ありません。Claude Code 2.1.139 以降を使ってください。`/goal` が入ったのはそのリリースだからです。残りは[クイックスタート](../docs/quickstart.md)にあります。
</details>

## 使い方

**1. 仕事を説明する。** Claude Code で `/goalify` に続けてタスクを書きます。goalify はプロジェクトを読み、本当に決めるべき数点だけを尋ね、ブリーフを書いて条件を表示します。

```text
/goalify migrate our API to async/await
    Brief:     ~/acme/.goal/api-migration.md
    Condition: 149 chars, under the 4,000 limit
```

**2. チャットを消す。** `/clear` で会話が消えるので、実行はまっさらな状態から、集中力を保ったまま始まります。

**3. 条件を貼り付ける。** 一行まるごとです。画面上では折り返されるので、全部つかんでください。

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it - done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

ブリーフのパスはその一行の中に同乗しています。`/goal` の背後にいる評価者はツールを持たず、ファイルを開けないからです。評価者が読むのは、貼り付けた一行と、実行の切り詰められたトランスクリプトだけで、ブリーフそのものは見えません。パスだけを渡してもエラーにはならず、何も証明されません。だからこそ、いちばんやりがちな失敗です。

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

貼り付ける前に一行が心配なら、
`python3 skills/goalify/scripts/condition_lint.py "<your condition>"` が六つの機械的なルールに照らして確認し、通らなかったものを挙げます。判断が要るところはあなたに残ります。

<p align="center">
  <img src="../assets/hero.svg" alt="4 ステップ: 仕事を説明する、ブリーフと条件を受け取る、条件を貼り付ける、証拠が待っている。" width="72%">
</p>

## 得られるもの

- **渡すのは一行だけ。** チャットを消し、一行貼り付け、あとは離れる。
- **文脈がリセットを越える。** ブリーフがあなたの決定を新しいセッションへ運びます。
- **進捗はひと目でわかる。** 実行はブリーフの中のチェックリストを進めながら消し込みます。
- **約束ではなく証拠。** 最後のターンは、検査が通った出力を引用し、上の `ASYNC-OK` のような作り物の語を印字しなければなりません。作業を飛ばした実行は、あからさまに嘘をつくしかなくなります。
- **上限でもきれいに終わる。** ターン上限が近づくと、実行は新しい作業を始めるのをやめ、途中のものを仕上げるか戻し、最終報告で早く止まったと伝えます。
- **止まっても進捗は残る。** ブリーフはチェックリストごとその場に残ります。同じ一行を貼り直せば再開でき、やり直しにはなりません。
- **成功したときだけ片づける。** 締めのターンで全部の検査を再実行し、出力を引用し、ブリーフを `.goal/done/` へ移します。どのファイルブラウザでも見える移動です。

## お使いのエディタで動く

`npx skills add` を通じて、Claude Code、Cursor、Codex、Copilot、Gemini CLI、ほか 70 以上のエージェントで動きます。スキルはただの Markdown なので、特定のモデルに縛られる部分はどこにもありません。

| エージェント | 一行インストール |
|:--|:--|
| Claude Code | `claude plugin install goalify@10x` |
| 70 以上のエージェントのいずれか | `npx skills add Aboudjem/goalify` |
| Cursor、Codex、Copilot、Gemini CLI、OpenCode | `npx skills add Aboudjem/goalify -a <agent>` |
| そのほかすべて | [docs/editors.md](../docs/editors.md) にあるエージェントのコードと配置先 |

`/clear` と `/goal` は Claude Code のコマンドです。ほかの環境では、`/clear` の代わりに新しいセッションを始め、そこへ条件を常設の目標として渡してください。Codex には独自の `/goal` があり、[Codex で動かす](../docs/codex.md)に何が引き継がれ何が引き継がれないかを書いてあります。

## 知っておくこと

> [!IMPORTANT]
> 実行が止まったことは、終わった証拠ではありません。評価者は自分で判断し、ゴールに届かないと結論して実行を終わらせることもあります。緑の結果を信じる前に、締めの証拠、つまり最後の返信で引用された検査の出力と `.goal/done/` へ移されたブリーフを読み直すか、自分で検査を走らせ直してください。

- **goalify は書くだけで、実行はしません。** このセッションで二つの成果物を書いて止まります。実行を始めるのはあなたです。
- **裏で動くものはありません。** Markdown のスキルが一つ。サーバーなし、入れる依存なし、それ自身のネットワーク通信もなし。
- **約束しないことのすべて**は[正直な限界](../docs/limits.md)に書いてあります。

## もっと知る

- [クイックスタート](../docs/quickstart.md)、最初の実行を最後まで、それに別のインストール方法。
- [条件の実例](../examples/conditions.md)、出荷に値するもの 8 本と避けるべきもの 8 本。悪いほうが何を失っているかを 1 行で書いてあります。
- [実例のブリーフ](../examples/sample-brief.md)、本物のブリーフと、そこから導いた条件。
- [エディタへのインストール](../docs/editors.md) · [FAQ](../docs/faq.md) · [Codex で動かす](../docs/codex.md)
- [正直な限界](../docs/limits.md) · [変更履歴](../CHANGELOG.md) · [スキル本体](../skills/goalify/SKILL.md) · [ライセンス](../LICENSE)

<p align="center"><sub><a href="../assets/goalify-teaser.mp4">28 秒のティザーを見る</a> · <a href="../assets/goalify-teaser.gif">GIF</a></sub></p>

---

<sub><a href="https://github.com/Aboudjem">Adam Boudjemaa</a> 作。MIT ライセンス。`/goal` の挙動は 2026 年に、配布された Claude Code 2.1.223 のバイナリから再導出したものです。<a href="https://github.com/Aboudjem/goalify/issues">気になる点は？</a></sub>

<sub>この翻訳は機械支援によるものです。正典は英語版の <a href="../README.md">README.md</a> です。</sub>
