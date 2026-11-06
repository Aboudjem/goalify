<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-light.svg">
    <img src="../assets/hero-dark.svg" alt="goalify: AI に大きな仕事を渡して、証拠を受け取る。" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/goalify/actions/workflows/validate.yml/badge.svg" alt="検証"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/github/license/Aboudjem/goalify?color=9b6bff" alt="MIT ライセンス"></a>
  <a href="https://github.com/Aboudjem/goalify/releases"><img src="https://img.shields.io/github/v/release/Aboudjem/goalify?color=2ee6ff" alt="最新リリース"></a>
  <a href="https://github.com/Aboudjem/goalify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/goalify?color=ff3d9a" alt="GitHub スター"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <b>日本語</b> · <a href="es.md">Español</a> · <a href="fr.md">Français</a>
</p>

<p align="center">
  <strong>AI に大きな仕事を渡す。証拠を受け取る。</strong>
</p>

<p align="center">
  <a href="https://goalify-kappa.vercel.app">Web サイト</a> · <a href="#インストール">インストール</a> · <a href="#しくみ">しくみ</a> · <a href="#30-の新機能">3.0 の新機能</a> · <a href="#ほかとの違い">ほかとの違い</a> · <a href="#知っておくこと">知っておくこと</a>
</p>

goalify は、あなたの依頼を**ゴール**に変えます。ゴールとは、はっきりしたゴールラインです。AI は、ゴールが終わって証明されるまで、またはあなたが決めた上限に着くまで、働き続けます。

goalify は先に考えます。計画がうまくいくか確かめます。ドキュメントを読みます。プロジェクトにある本物のテストを見つけます。聞きたいことは、最初に一度だけ全部尋ねます。そのあと AI はひとりで、何時間も、ときには何日も働きます。だれも答える必要はありません。最後に、AI は証拠を見せます。

**Claude Code** と **Codex** で最もよく動きます。どちらにも `/goal` コマンドが入っていて、作業を続けさせます。Claude Code では、2 つ目のチェッカーが毎ステップのあとに作業を読みます。Codex は、同じゴールラインに照らして自分の作業を自分で確認します。goalify はほかの 70 以上の AI ツールにも入ります。そこでは同じ計画とゴールラインが手に入り、作業はあなたが自分で始めます。

## インストール

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install goalify@10x
```

スキルを読めるほかの AI ツールなら、一行で済みます。

```bash
npx skills add Aboudjem/goalify
```

そのあと `/goalify` と打って、仕事を説明してください。Claude Code 2.1.139 以降が必要です。そのバージョンで `/goal` が加わりました。

<p align="center">
  <a href="https://goalify-kappa.vercel.app"><img src="../assets/goalify-demo.gif" alt="ループで動く goalify。依頼がゴールになり、質問が全部先に来て、AI がひとりで働き、最後に証拠が届く。" width="88%"></a>
  <br><sub><a href="../assets/goalify-promo.mp4">フル動画を見る</a> · <a href="../assets/goalify-promo-vertical.mp4">縦型動画</a> · <a href="../assets/goalify-promo-30s.mp4">30 秒動画</a> · <a href="../assets/goalify-promo-15s.mp4">15 秒動画</a></sub>
</p>

## goalify なしと、goalify あり

| goalify なし | goalify あり |
|:--|:--|
| 午前 3 時に AI が止まって質問してくる | 質問は全部先に、一度だけ |
| チャットを消すと計画も消える | 計画はファイルに残る。AI は何度でも読み直す |
| プロジェクトにないテストを AI が使う | テストはあなたの本物のプロジェクトから来る |
| 「終わった！」は AI がそう言っただけ | 「終わった」は、最後のステップでテストが通っているという意味 |
| 問題は翌朝に見つかる | `/goalify verify` がテストをもう一度走らせて、レシートを渡す |

## しくみ

goalify がするのは準備だけです。作業をするのは `/goal` コマンドです。goalify は、AI がもう何も聞かなくていいようにします。

1. **下調べ。** うまくいくか。goalify はプロジェクト、ドキュメント、テストを読みます。仕事が本当に終わったことを示すコマンドを見つけます。
2. **質問は一度だけ。** 本当に選ぶべき数点を、まとめて尋ねます。そのあとは尋ねません。
3. **2 つのものができる。** **ブリーフ**は、計画の全部が入ったファイルです。あなたの選択、正確なファイル、作業の順番。**条件**は `/goal` に渡す一行で、証拠がどんな形かを書いてあります。**プレビューページ**も開くので、先に計画の全体を見られます。
4. **`/clear`、貼り付け、あとは離れる。** 作業はきれいなチャットで始まり、メモリはすべてあなたの仕事のために空いています。Claude Code では、2 つ目のチェッカーが毎ステップのあとに作業を読みます。証拠がそろったとき、またはステップ数の上限に着いたときだけ、作業が止まることを許します。
5. **あとで確かめる。** `/goalify verify` が検査をもう一度走らせて、レシートを書きます。

貼り付ける一行はこんな形です。長いので、全部コピーしてください。

```text
/goal Do everything in ~/acme/.goal/api-migration.md and prove it, done when the last turn quotes npm test passing and says ASYNC-OK. Stop after 40 turns.
```

ブリーフへのパスは、その一行の中にあります。ここが大事です。`/goal` の裏にいるチェッカーは、ファイルを開けません。読めるのは、貼り付けた一行とチャットだけです。だから `/goal` にファイルのパスだけを渡さないでください。何も壊れませんが、何も確認されません。いちばんやりがちな間違いです。

```text v1-antipattern
/goal ~/acme/.goal/api-migration.md
```

<p align="center">
  <img src="../assets/hero.svg" alt="4 ステップ: 仕事を説明する、ブリーフと条件を受け取る、条件を貼り付ける、証拠が待っている。" width="72%">
</p>

### なぜ何日も働けるのか

長い AI の作業は、たいてい 2 つの形で失敗します。AI が止まって何かを聞いてくる。または、まだ壊れているのに「終わった」と言う。goalify は 1 つ目を、最初に全部尋ねて答えをブリーフに書くことで防ぎます。2 つ目は条件で防ぎます。最後に、AI はすべての検査をもう一度走らせ、結果を見せ、`ASYNC-OK` のような特別な語を書かなければなりません。AI が作業を飛ばしていたら、嘘をつくしかありません。ステップ数の上限が近づくと、AI はきれいに終わらせて、残りを伝えます。早く止まった場合も、ブリーフにはチェックリストが残ります。同じ一行をもう一度貼れば、続きから始まります。

## 3.0 の新機能

<p align="center">
  <img src="../assets/preview-and-receipt.svg" alt="3.0 のループ。先に計画のプレビュー、AI がひとりで作業、そして VERIFIED と書かれたレシート。" width="88%">
</p>

- **計画のプレビュー。** `/goalify` のあとに毎回、ブラウザでページが開きます。ステップ、各検査とそれを証明するコマンド、上限、あなたの選択、`/goal` の一行をコピーするボタンが見えます。ブリーフも確認して、壊れたブリーフは表示しません。チャットに出る `/goal` の一行が、いまも主な手順です。ページはおまけです。
- **証拠のレシート。** `/goalify verify` は検査を見せて、一度だけ確認し、走らせて、レシートを書きます。**VERIFIED**、**NOT VERIFIED**、**UNVERIFIABLE** のどれかです。AI が「終わった」と言ったときでも、「確認できていない」と言えます。危険なコマンドは、ひとつずつ許可しない限り走らせません。
- **本物のテストを、自動で見つける。** goalify は `package.json`、`pyproject.toml`、`Cargo.toml`、`go.mod`、Makefile、CI のファイルを読みます。npm の空の「no test specified」テストは飛ばします。だから、通るはずのないテストがゴールラインに載ることはありません。最初にテストを一度走らせることもできます。
- **ステータス。** `/goalify status` は `.goal/` にあるすべてのブリーフを、進行中、ブロック、完了で一覧にします。進行中のものには、続けるための `/goal` の一行を全部出します。
- **クイックモード。** `/goalify --quick <task>` は中くらいの仕事向けです。Web 調査と質問は省きますが、安全のための確認はすべて残します。仕事が 2 通りに読めるときは、止まって、フルモードを使うよう伝えます。
- **Doctor。** `/goalify doctor` は、コンピュータにあるすべての goalify のコピーを一覧にします。古いコピーが新しいコピーと並んで読み込まれていたら、知らせます。
- **より安全なコピー＆ペースト。** 条件にバッククォートや二重引用符を入れられなくなりました。だから `claude -p "/goal ..."` の一行を貼り付けても、隠れたコマンドは動きません。修正してくれた [@Hug0x0](https://github.com/Hug0x0) に感謝します。

## ほかとの違い

わかりやすい違いだけを挙げます。2026 年 11 月に各プロジェクトの README で確認しました。

| ツール | 何か | goalify との違い |
|:--|:--|:--|
| [supergoal](https://github.com/robzilla1738/supergoal) | Claude Code のプラグイン。下見をして、質問し、フェーズに分けて計画し、`/goal` に一つのコマンドを渡す。最後に結果を計画と照らして確認する | いちばん近いツール。goalify は完全なブリーフと確認済みの条件を一つ書き、作業の前にプレビューページを見せ、作業のあとに証拠のレシートを書きます |
| Ralph ループ（[snarktank/ralph](https://github.com/snarktank/ralph) など） | 同じプロンプトを AI に何度も与え続けるループ | たいてい、AI が書いた語か、回数の上限で止まります。Claude Code の `/goal` では、2 つ目のチェッカーが毎ステップ作業を読みます |
| [Spec Kit](https://github.com/github/spec-kit) | GitHub の、仕様、計画、タスクを書くためのツールキット | 仕様を書くのに最適。goalify は、だれも見ていない長い作業と、それが終わったことの証明のためのものです |

## お使いの AI ツールで動く

| ツール | 一行インストール |
|:--|:--|
| Claude Code | `claude plugin install goalify@10x` |
| 70 以上の AI ツールのいずれか | `npx skills add Aboudjem/goalify` |
| Cursor, Codex, Copilot, Gemini CLI, OpenCode | `npx skills add Aboudjem/goalify -a <agent>` |
| そのほかすべて | [docs/editors.md](../docs/editors.md) にあるコードとフォルダ |

`/clear` と `/goal` は Claude Code のコマンドです。ほかのツールでは、`/clear` の代わりに新しいチャットを始め、AI に条件を主なタスクとして渡してください。Codex には独自の `/goal` があります。同じように動くこと、動かないことは、[Codex での goalify](../docs/codex.md) を見てください。

<details>
<summary>手動でインストールする</summary>

```bash
git clone https://github.com/Aboudjem/goalify
cp -R goalify/skills/goalify ~/.claude/skills/
```

必要なのはそのフォルダだけです。残りは[クイックスタート](../docs/quickstart.md)で説明しています。以前のコピーがあるときは、`/goalify doctor` を実行して、読み込まれているのが一つだけか確かめてください。

</details>

## 知っておくこと

> [!IMPORTANT]
> 作業が止まっても、終わったとは限りません。チェッカーは自分で判断します。ゴールに届かないと考えたときも、作業を止めることがあります。緑の結果を信じる前に、ブリーフに対して `/goalify verify` を走らせるか、自分で検査を走らせてください。

- **goalify は仕事そのものはしません。** ブリーフと条件を書きます。検査を走らせるのは、頼まれたときだけです。
- **どこにも何も送りません。** サーバーなし、追加パッケージなし、ネットワーク通信なし。補助スクリプトは標準の Python だけを使い、プレビューページはインターネットから何も読み込みません。
- **お金の推測はしません。** goalify は、お金やトークンの費用を推測しません。ステップ数の上限があなたの手綱です。
- **約束しないことのすべて**は[正直な限界](../docs/limits.md)に書いてあります。

## もっと知る

- [Web サイト](https://goalify-kappa.vercel.app) · [クイックスタート](../docs/quickstart.md) · [FAQ](../docs/faq.md)
- [条件の例](../examples/conditions.md): 良い例と悪い例、そして悪い例ごとに何を失うか。
- [完全な例](../examples/sample-brief.md): 本物のブリーフとその条件。さらに[プレビューページ](../examples/sample-brief.html)（ダウンロードしてブラウザで開いてください）。
- [AI ツールへのインストール](../docs/editors.md) · [Codex での goalify](../docs/codex.md) · [正直な限界](../docs/limits.md)
- [変更履歴](../CHANGELOG.md) · [スキル本体](../skills/goalify/SKILL.md) · [ライセンス](../LICENSE)

---

<sub><a href="https://github.com/Aboudjem">Adam Boudjemaa</a> 作。MIT ライセンス。`/goal` に関する事実は、Claude Code 2.1.317 とそのドキュメントで 2026 年 11 月に確認しました。<a href="https://github.com/Aboudjem/goalify/issues">問題を見つけたら？</a></sub>

<sub>この翻訳は機械支援によるものです。正典は英語版の <a href="../README.md">README.md</a> です。</sub>
