# learend_recode
## what I learned
### 2025.1.3
- URLにIPアドレスを直打ちしてリダイレクトされる場合はetc/hostsにIPアドレスとホスト名を書き込むことでアクセスが可能になる
- gobusterのdirモードは-xでファイルタイプの指定ができる
- URLパラメータのpageはサーバーサイドではページネーションの役割をもち、クライアントサイドでは言語の変更が可能となる
- ハイジャック攻撃ツールとしてResponderというものがある
### 2025.1.4
- find ./ -name hoge* とするとzshではno matches foundとなり、bashでは検索される。これはzshがワイルドカードをシェルで展開しないためである。つまりzshではhoge\*が文字列として扱われる。これを展開してワイルドカードを認識させるためにはfind ./ -name "hoge*"とする。bashでは"があってもなくても展開されるので問題ない。つまり、""込みで覚えておくのがベター
- find . hoge.txtのようにオプションがないケースでカレントディレクトリを指定すると、.がファイル名として扱われてしまうことがある。よって、findコマンドはオプションをつけることを基本と考えた方が良い。
- サブドメイン探索ツールとしてffufというものがある。gobusterと同じように辞書を使用して探索が可能で、こちらはresponsecodeの指定もできる。
- パスワードリストが無い場合は、crunchというツールで作成することができる。crunch 1 3 01234 -o <path>で1文字以上3文字以下、使う文字は01234で指定されたパスにファイルを作成するというコマンドになる。
### 2024.1.5
- awscliを使ってAmazon S3にアクセスすることができる
- ParrotOSやkali Linuxにはリバースシェルなどを行うためのファイルが/usr/share/webshells/に入っている。使う時はファイルをコピーしてsedコマンドなどで自分の情報に書き換えて使う。つまり、S3バケットにスクリプトをアップロードしてリバースシェルを実現することができる
- JavaScriptでは変数を定義（constやlet）した後はプログラムが自動的に変数を判断してくれるが、phpでは変数であることを明示しなければならない。
つまり、以下のような違いがある
```JavaScript
// JavaScriptの場合
const num = 12;
console.log(num);
// 12が出力される。
```
```php
// PHPの場合
$num =12;
print(num);
// errorが出る
print($num);
// 12が出力される
```
- JavaScriptの文字列連結は+だが、PHPでは.である。
### 2025.1.6
- ハイジャック攻撃ツールのResponderは通信を記録できるのでリモートファイルインクルードの脆弱性を持つサイトがあれば、自分のIPにアクセスさせることでパスワードハッシュなどを入手できる。そのハッシュをJohnで解析することによりパスワードを割り出すことができる。ということはWireSharkでもOK？**用深掘り**
- 技術的なことではないけども、次の言葉にどきっとした。
# 「強い意志で決めた目標が願望になりさがる」
## 目標がすこしずつただの願望になっていませんか？
- 間違ったgit commitを消す手順。タイトルだけを消したい時は
```bash
# コミットだけを消したい場合
git reset --soft HEAD^

# コミットだけでなくステージングへの追加も消したい場合
git reset --hard Head^
```
