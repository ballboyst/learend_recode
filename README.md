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
### 2025.1.5
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
- JSのイベントリスナーでchangeイベントが発火するタイミングは要素によって異なる。具体的にはinput要素の場合は値を変更し、フォーカスが外れたタイミングで、select要素やチェックボタン・ラジオボタンの場合は状態が変化したタイミングとなる。
JSで今回書いたコードに出てきたものをまとめたものが以下
```JavaScript
    // イベントリスナーの設定
要素.addEventListener("イベント", function{
    処理
});
// 自分はよくfunctionをfuncとしてしまいエラーが出るので注意


    // HTMlに要素を追加
let 要素名 = 親要素.createElement("要素");
/* だいたいはdocument.createElementになる！
*/ ちなみにボタンを作る時はこんな感じ
let button = document.createElement("updateButton")
button.textContent = "編集";


    // 要素に属性を設定する
要素名.setAttribute("属性", "値");
// input要素の属性ならtype属性、値をcheckboxとしたり、id属性で値をID名にしたりといったことが可能


    // 要素を書き換える
親要素.replaceChild(変更前の要素, 変更後の要素);
// ただし要素を指定するためにgetElementやquerySelectorで要素を事前に取得しておく必要があることに注意


    // 配列にオブジェクトを格納する（Todoリストとかで使う）
let list = [];  // まず配列を作る
const obj ={  // オブジェクトを作る
    プロパティ:"名前",
    プロパティ:"名前",
};
list.push(obj);  // 作ったオブジェクトを配列にプッシュする


    // 要素の取得（IDを使う場合）
let 名前 = document.getElementById("ID名")
```
- forEachとfor ofとの違いは繰り返し処理を制御するかどうか。forEachは配列を単純に繰り返し処理する。for ofは配列を細かく制御できるという点で異なる。ちなみにfor inはオブジェクトに対する繰り返し処理となる。

### 2025.1.7
- smbclientの使いかた
```bash
    # 認証不要な共有ファイル一覧を表示
smbclient -N -L 接続先ホスト
# 表示されるリストで末尾が＄のものは管理用

    # 接続100
smbclient //サーバー名/共有名 -U ユーザー名

    # ファイルのダウンロード
get ファイル名
    # ファイルのアップロード
put ローカルファイル名 リモートファイル名
```
- どうやらHTBではResponderとimpacketはセットでよく使われるみたい。特にimpacketはペネトレでは必須のよう
- 結局フロントエンドもフローチャートを作る力が重要で、そこが適切にできてれば、あとはやりたいことのメソッドを探して書いていくだけ。つまり、フローチャートが主軸として、そこに必要な要素やメソッドを集めて飾ってやるみたいなイメージ！
### 2025.1.8
- JSで配列の要素やインデックスを調べるメソッドは３つ
```JavaScript
配列.find
配列.findOf
配列.indexOf
// 違いは改めて調査する
```
要素の削除は次の通り。indexメソッドと組み合わせて使ったりする
```JavaScript
let index = 配列.findIndex(task => task.todo === currentText)
配列.splice(index, 1)
```
`次回、findIndexの挙動とindexOfとの違いを調査`
### 2025.1.9
- AWSのSGについて。1つのSGには0.0.0.0/0を設定できるのは１つのみ。つまり、HTTPで0.0.0.0/0からのアクセスとカスタムTCPの8000番ポートを0.0.0.0/0で許可したい場合、SGを２種類作ってインスタンスに紐づける必要がある。
- JSの変数。変数に格納している値は実はメモリ空間。変数を更新した時は、参照するメモリ空間を変更しているだけ。じゃあ元々のメモリ空間に入っている値はというと、必要なければ削除される。
- オブジェクトの操作にはドット記法とブラケット記法がある。
```JavaScript
const obj = {
    name : "taro",
    age : 18,
    };

// ドット記法はobj.propのように対象を指定する
console.log(obj.age);
// >18

// ブラケット記法はobj[prop]のように対象を指定する
console.log(obj["age"]);
// >18
// ブラケット記法は変数による指定が可能
let key = name;
console.log(obj[key]);
// >18
```
- JSのfindIndexメソッドの使い方
```JavaScript
// findIndexはテスト関数に合格した最初の要素のインデックス番号を返す
let array ={
    key1:orange1,
    key2:grape2,
    key3:great3,
};

console.log(array.findIndex((element) => element === "great3"));
> 2 
// これだと最初に完全一致したものを抽出する。指定文字を含むものを抽出したい場合は以下
console.log(array.findIndex((element) => element.includes("2")));
> 1

// findメソッドとfindIndexメソッドの違いは返り値！findは要素の値を返し、findIndexは要素のインデックス番号を返す
```
- JSのindexOfメソッド
```JavaScript
// indexOfメソッドは指定した文字列の添字番号を返す。つまり、配列なら要素番号を返し、文字列なら何文字目かを返す
let array = {
    key1:orange,
    key2:grape,
    key3:great,
}
console.log(indexOf("grape"));
> 1
console.log(indexOf(g));
> -1

let string= "I love dog!";
string.indexOf("dog"); 
> 7
string.indexOf("I");
> 0
```
### 2025.1.10
- todoListの作成でfindIndexメソッドを使ったが、値が取れない...と悩んだものの、結局値は取れていて、取得した値を変数に格納していなかったから表示していないだけだった。使い方にまだ慣れてないってこと！
```javascript
// ダメな例
todoList.findIndex(task => task.todo === anchor.textContent);
console.log(task.todo); // ここでtask.todoを指定してもtaskは上記findIndex中でのみ有効なので値は取得できない。
> undefined
// OKな例
let task = todoList.findIndex(task => task.todo === anchor.textContent);
console.lgo(task);
> 1
```
- 最初はaddTodoにリスト追加と画面表示を書いていたが、処理を分割すべきと気づいてリスト制御のaddTodoと画面表示のreladにメソッドを分けた。この流れは前回と全く一緒。以前より早く気づけたのは良いが、最初にフローチャートを作らない弊害が大きい！
- 画面に表示されているul要素を削除しリフレッシュするコード
```javascript
const ul = document.querySelectorAll('ul');
ul.forEach(ul => ul.remove());
```
- for inとfor ofの違いにたいする理解が浅かった。
```javascript
let list =[
    {key1:"check1",key2:"todo1"},
    {key1:"check2",key2:"todo2"}
]
// この場合listは配列なので使うのはfor ofになる。オブジェクトを操作したいからといってfor inを使うのはNG
for (todo in list){console.log(todo)};
> 0
> 1
// リストの要素が返される
for (todo of list){console.log(todo)};
> {key1: 'check1', key2: 'todo1'}
> {key1: 'check2', key2: 'todo2'}
// リストのオブジェクトが返される
for (todo of list){console.log(todo.key2)};
> todo1
> todo2
```
### 2025.1.11
- 質問ダイアログを表示したい時はwindow.prompt(question, default_massage)を使う。
todoListのUpdate機能を実装する際、最初は以下のコードにしたがキャンセルボタンを押すとtodoキーの値がnullになる問題が発生。
```javascript
updateButton.addEventListener('click', function(){
    let update = window.prompt("修正内容を入力してください");
    let index = todoList.findIndex(
        (task) => task.todo === anchor.textContent
    );
    todoList[index]["todo"] = update; //ブラケット表記なのは変数で指定するため
})
```
具体的な解決策
1. 現在の文字列を初期値として修正させる。(これだけではダメで条件分岐が必要だった..)
```javascript
updateButton.addEventListener('click', function(){
    let index = todoList.findIndex(
        (task) => task.todo === anchor.textContent
    );
    let update = window.prompt("内容を修正してください", anchor.textContent);
    todoList[index]["todo"] = update; //ブラケット表記なのは変数で指定するため
})
// この方法では結局「キャンセル」を押すとtodoの値がnullになるのでNG
```
2. 条件分岐で制御
```javascript
updateButton.addEventListener('click', function(){
    let update = window.prompt("修正内容を入力してください");
    if (update !== null) {
        let index = todoList.findIndex(
            (task) => task.todo === anchor.textContent
        );
    todoList[index]["todo"] = update; //ブラケット表記なのは変数で指定するため
    };
});
```
- JSで配列の要素を取り出すメソッドは３つ！取り出す場所が
先頭 => shift()
末尾 => pop()
途中 => splice(start, deleteCount)
となる。
### 2025.1.12
- htmlファイルにCSSを直接記述するには以下のように指定する。
```html
<body>
    <h2>title</h2>
    <p></p>
    <a href="source path">hoge</a>
    <a style="color:red;">文字を赤色にする</a>
</body>
```
- htdocsディレクトリはApacheのデフォルトのドキュメントルートとして使用される。
ここに配置したファイルはWebからアクセス可能となるためWebコンテンツが格納される。一方、誰でもアクセスできるので、公開したくないファイルはドキュメントルート外のディレクトリに置くことが重要である。
- JSのincludesは指定した文字が含まれているか調べるもの。includesとfilterメソッドの組み合わせが便利
```javascript
let array = [
    {"key":"apple"},
    {"key":"grape"},
    {"key":"lemon"},
];
let filter = array.filter(
    (name) => name.key.includes("a")
);
console.log(filter);
> (2) [{…}, {…}]
  0: {key: 'apple'}
  1: {key: 'grape'}
  length: 2[[Prototype]]: Array(0)
/* 文字"a"を含む配列を取り出すことができた。
filterメソッドはコールバック関数の条件式を判定するので、
includesを使わないと(name) => name.key === "apple"
のように完全一致または完全不一致が考えられる
```
### 2025.1.13
- 連想配列について。
通常、配列は配列名によって特定され、配列内の要素はインデックスで特定される。インデックスは非負整数が割り当てられる。連想配列は配列内の要素特定にkeyを使えるようにしたもの！。つまり、文字列が使え、より直感的に要素を扱えるということ。イメージはJSのオブジェクト（JSのオブジェクトは連想配列の１種という扱いらしい。byIT用語辞典）。
- PHPの連想配列
```php
$array = [
    'key1' => 'taro',
    'key2' => 'jiro',
    'key3' => 'saburo',
];
foreach($array as $key => $name){
    print($key . 'の値は' . $name . "\n");
}
/* 以下は出力結果
key1の値はtaro
key2の値はjiro
key3の値はsaburo

*/
```
- PHPのsprintfはフォーマット変換を行うメソッド。%sや%dに引数で指定したデータを埋める。
```php
$format = '%s君は%sを%d個食べました。' . "\n";
echo sprintf($format,"太郎","りんご",7);
echo sprintf($format,"次郎","みかん",10);
/* 以下、出力結果
太郎君はりんごを7個食べました。
次郎君はみかんを10個食べました。
*/
```
- PHPのechoとprintの違いは引数が１つか１つ以上か。
echoは文で、printは式。基本的にechoを使うようにしておけば問題ない。
### 2025.1.14
- JSのsymbolはバージョンアップにより既存の機能を壊さないためのもの
- OT機器のネットワークプロテクション製品にedgeIPS,edgeFireというものがあり、それらを一元的に集中監視できるedgeOneというものがある。
### 2025.1.15
- 統計に関して。
推測統計は一部のデータから全体の性質を推測するもの
連続確率変数＝とりうる値が連続的な確率変数
ベイズ統計学ではベータ分析がよく使われる
期待値は確率分布をやじろべえと見なした場合の重心にあたる
- 技術屋は技術力があるのが当たり前。ハードスキルの無い人が技術屋を名乗るのは名前負け
- ハードスキル✖️ソフトスキル＝アウトプットの質
- MITRE ATT&CKのAzure版のようなAzure Threat Research Matrixというものがある
### 2025.1.16
- Splunkを学習。取得したログを効果的に扱うためにはindexとfieldの設定が必要みたい。
- ubuntuでchromeが最新版でないと表示されたのでをアップデートしようとしたが、なぜかうまくアップデートできなかった。
実行履歴
```bash
sudo apt update
sudo apt upgrade
sudo apt install google-chrome-stable # upgradeで全て更新されているはずだが念の為chromeを指定してインストール
sudo apt autoremove # chromeのインストールで不要なものがあると言われたので削除
sudo apt install google-chrome-stable
google-chrome # chromeがアップデートされないのでターミナルで開いてみる→変化なし
# ubuntuソフトウェアでchromeをアンインストール
sudo apt install google-chrome-stable
# アップデート成功
```
結局再インストールでOKとなったが、なぜアップデートできなかったのかは不明
chromeのインストールはダウンロードした.debファイルを右クリックし「別のアプリケーションで開く」を選択。その後「ソフトウェアのインストール」を選択することで行える。
- gitに関して
```bash
git reset -- hard Head^
```
このコマンドでステージングの追加を含めて取り消しが行える。
ということは次のようなケースで考えると...
1. ファイルを編集
2. ファイルをステージングに追加
3. git add . としてしまったため不要なファイルまで追加される
4. ミスに気づかずコミットする
5. コミット後ターミナルを見て気づく
6. git reset -- hard Head^ する
7. 改めて対象のファイルのみステージングに追加しコミットする

この場合git resetでステージングへの追加も取り消されているため、変更したファイルが変更前の状態（最終コミット）に戻ってしまうためgit addしても無意味で最初にステージングに追加したファイルの内容は失われてしまう。
検証により確認済み。
つまり、addする範囲を間違えた時はgit reset --soft Head^　の後にステージングからファイルを対象外にする操作が必要ということ。
そもそもignoreで除外しておけばいい話ではあるが..
### 2025.1.17
- ターミナルのコマンドにslやcmatrixなど遊び心の塊のようなものがあることを知ったｗ
- MAMPで構築した環境の注意点
vscodeで記述したhtmlをオプション＋Bで開くとURLはfile//hogeとなっている。そのためhtmlからphpファイルにリンクさせても正常に動作しない。（コードが表示されるだけ）
挙動を確認するためにはhttp://localhost:8888のようにhttpを使う必要がある。
- PHPに対するXSSはインプットフォームに次のように入力する
```
<script>{alert('hello');}</script>
```
- PHPのhtmlspecialcharsファンクションはHTMLタグの効果をうちけしてくれるのでXSS対策になる。
- PHPは次の構文でHTTPのメソッドを扱える
```php
print($_GET['hoge']);
// hogeはHTML内の要素（nameやvalue）
// 当然POSTメソッドも使える。
// REQUESTはGETもPOSTも扱えるが、基本的に使わない方がいい
```
### 2025.1.18
- vimの操作。１行目に移動はggで、最下行に移動はG。10gなら１０行目に移動する
- vimの操作。fhでカーソルをｈに移動。thでカーソルをｈの一つ前に移動。
- vimの操作。cwとかよく使う。カーソルがある場所の単語をカットする。
- PHPで指定したURLに遷移させるにはheaderファンクションを使う。
```php
header('Location:https://hoge');
```
### 2025.1.19
- DB設計に関して。datetime型とtimestamp型はどちらも日付時刻を扱えるが明確な違いがある。

|内容|datetime|timestamp|
|----|----|----|
|扱える日付範囲|1000/1/1~9999/12/31|1970/1/1~2038/1/19|
|タイムゾーン|基準なし|UTC基準|
|ストレージサイズ|8byte|4byte|
|自動更新|なし|設定可能|

よって、将来的なデータを扱う場合やタイムゾーンを考慮しない場合はdatetime
ログインやアクティビティログを管理するアプリやタイムゾーンを考慮するようなグローバルユーザーの場合はtimestampとなる。

- ストレージの使用量はstr型が固定長でvarchar型は可変長。実際に扱うデータはほぼ可変長なのでstr型を扱うのは例外パターンである。
- PHPはAPIとして動作できるだけでなく、コード内にHTMLやJSを含めることができ、レンダリングしたHTMLソースを返すことができる。つまりなんでもできるオールインワンのプログラミング言語！だからこそよく使われているのだろう。
### 2025.1.20
- MAMPでMySQLを使用する手順。
1. MAMPアプリを開き、右上のSTARTを押して起動する
2. 右上に並んでいる３つのボタンのうち、中央のボタンを押し、webページを表示させる。
3. webページの左上のtoolを選択し、phpMyAdminをクリックする。
4. MySQLの管理画面が表示されるので操作する
### 2025.1.21
- 初めてモデムとルーターを使いwi-fi環境を構築した。
ルーターの方はRTモードではなくBR（ブリッジ）モードかAPモードを使用する。知識としては知っていたが全く自分の中で使える状態ではなく、取説の手順書を読んで初めてそうだよねってなった。また、モデムに接続し各種設定を行わないとインターネット通信できないことを初めて知った。
### 2025.1.22
Dockerマスター編パート①
- Dockerは仮想化技術の一つ。
- 仮想化とは１人で複数人いるように見せる技術
- Dockerを使うことで異なるハードウェアに同じ環境を構築できるので開発効率がUP
- ハイパーバイザー
1. ベアメタルハイパーバイザー
ホストOSを必要としない
VMwareESXi,Microsoft Hyper-V(ベアメタル版),Xen（EC2の裏側はこいつ）
EC2はゲストOS
2. ホスト型ハイパーバイザー
ホストOS上で動作する
VirtualBoxとか
- 仮想マシン＝仮想化された上で動いているマシン
- コンテナ型仮想化は圧倒的に速い
- コンテナはdockerだけじゃない
- Dockerはコンテナの作成、デプロイ、管理を簡単にするためのプラットフォーム
- デーモン＝常駐プログラム
- Dockerの特徴はポータビリティ（ソースコードのようにインフラ環境まで持ち運べる）
- 冪等性は同じことが起きること
- コンピューティングリソース＝CPUとRAM（メモリ）
- Dockerイメージはカップ麺のようなもの！
pull=購入、runなどのクライアントコマンド=お湯を注ぐ、起動完了=ラーメン完成
- cat /etc/os-releaseは覚えておくこと！
- イメージの選定で見るポイント！
どれだけ更新されているか？
どこが出しているか？
- curl ifconfig.me は自分のグローバルIPがわかる
### 2025.1.23
securityイベント（LT）に参加
- IT業界の資格は2000以上！全ての資格はオンリーワン
- CompTIAは実業務に沿った内容となっている。
- Security+はセキュリティに関する基盤。そのためどんな方向性でも必要。そこからどんな業務に携わるかで方向が決まる。
- サッカーで例えると、Security+がスタメンに入る能力。Pentest+とかはポジション別の能力。CEHはそのポジションの特定の人物の特化能力。Cyspはキャプテンなどのプレイヤーの中のリーダー。CISSPや情報確保支援士はフィールド外にいる監督やコーチという分類になる。
- クラウドサービスにはOracleが提供しているOICというものがある。どうやらOICはIPアドレスを無料で使えるらしい。
### 2025.1.25
- NDAは「秘密保持契約」のこと
- MSAは「マスターサービス契約書」で取引全般に適用されるルールを示した契約書のこと
- ALEは「年間損失予測」、SLEは「単一損失予測」で１回のリスク発生における損失予測のこと
- RPOは「目標復旧時点」、RTOは「目標復旧時間」
- 偵察にはアクティブとパッシブがあり、ポートスキャンなど実際に対象へアクションするものはアクティブ、公開情報を探すなど直接的関与を伴わないのがパッシブに分類される。
- CIAの保護に関して責任を負うのがデータカストディアン
- ゼロトラストアーキテクチャではコントロールプレーンとデータプレーンがあり、コントロールプレーンの中にアクセス許可の最終決定を行うポリシーエンジンがある。
- パスワードを２通のメールに分けて送信することをPPAPと言うらしい。やるメリットは皆無。そもそもメールが流出する場合に考えられるのは次の３パターン
1. アカウントが乗っ取られている
2. 中間者攻撃(１通目と２通目の時間が空いてれば効果はありそう)
3. メールサーバーが乗っ取られている
上記から愚策であることがわかる。パスワードを別で伝えるなら伝達媒体を別にする必要有り！
### 2025.1.26
- NCAとはネットワーク・アクセス・コントロールのことで端末を識別、認証し一定のセキュリティ基準を満たす場合のみアクセスを許可する
- メンテナンスウインドウは計画的なダウンタイムのこと
- 要塞ホストは一種のフィルタリングとも言える
- データ主権は国家が領土内で生成されたデータに対して持つ法的な権利や管理権のこと。各国でデータ主権について厳格化の動きが強まっている。
- NGFWは次世代ファイアウォールのこと。
- EDRはエンドポイントを監視及び保護する機能を持つ。よってマルウェアの横展開からホストを保護する
- 目的達成のためにリスクを進んで受け入れるのがリスクアペタイト
- スクリーンサブネットはDMZのこと
- PHPのif文の短縮構文
```php
<!-- 通常のif文 -->
if (条件式) {
    trueの処理
} else {
    falseの処理
}
<!-- 短縮構文 -->
<?php if (条件式): ?>
    処理
<?php else : ?>
    処理
<?php endif; ?>
```
### 2025.1.27
- PHPの入力フォームでバリデーションする時のサンプルコード
```php
if (!empty($_POST)) {
    // エラー項目の確認
    if ($_POST['name'] == '') {
        $error['name'] = 'blank';
    }
}
    <p>次のフォームに必要事項を記入ください</p>
    <form action="" method="POST" enctype="multipart/form-data">
    <dl>
        <dt>ニックネーム<span>必須</span></dt>
        <dd>
            <input type="text" name="name" size="35" maxlength="255">
            // isset関数により変数の存在確認を実施。<?php if $error['name'] == 'blank'>としてしまうとエラーが出るので注意！
            <?php if (isset($error['name']) && $error['name'] == 'blank'): ?>
            <p class="error">* ニックネームを入力してください</p>
            <?php endif; ?>
        </dd>
    </dl>
    </form>
```
- PHPでファイル名から拡張子を抜き出すにはsubstr()関数を使う.
```PHP
$name = hoge.jpg;
$ext = substr($name,-3);
echo $ext;
// jpg
```
### 2025.1.28
- JavaScriptのインクリメントとデクリメントは前置と後置で挙動が異なるため注意が必要！
- WordPressの有名な脆弱性としてauthorにidをポストするとアカウント名が分かるというものがある。
例えばURLにhoge?author=1とするとユーザーIDが１のアカウント名が表示されてしまうということ。
### 2025.1.29
- 相関副問い合わせとは、サブクエリでメインクエリを参照するもの！
つまり、通常の副問い合わせでは、サブクエリでSQL文が完結するが、相関副問い合わせでは外側のクエリの表を参照する。
よって、サブクエリの中に外側の表があるかないかで判断する。相関副問い合わせの場合の処理は以下のようになる。
1. 外側のクエリを実行（１行分だけ）
2. 結果を参照して内側のクエリを実行
3. 内側のクエリを参照して外側クエリを評価
### 2025.1.30
- Nutanixについて調査。
WebGUIツールPrismによるシステムの一画面管理が可能になる。
AHVというベアメタルハイパーバイザーを使用
各ホストにCVMとAHVを有しており、HAクラスタリングを実現
### 2025.2.1
|やったこと|わかったこと|備考|
|-----|-----|-----|
|UTMにMetasploitable2を入れた|ISOからQEMUに変換する手順|qemu-image convert -O qcow2 -c <vmdkファイル> <作成ファイル.qcow2>|
### 2025.2.2
|やったこと|わかったこと|備考|
|-----|-----|-----|
|UTMにvulnhubのイメージ（OVA）を入れた|OVAからQEMUに変換する手順|tar -xvf <ダウンロードしたファイル.ova> この後はISOの場合と同じコマンド。UTMでのインポートはqita記事参照|
|UTMに入れたMr-Robotを攻略|スクリーンショット取得ツールの存在||
||SUIDについて||
||nmapのinteractiveモードでシェルが実行できること||
### 2025.2.3
- mysql hoge@fuga -p で接続できないって昨日１日つぶしたが、今日はmysql -u hoge -h fuga -p で接続できた。よくよく考えるとSSHとMySQLでコマンドを混同してしまっていた....
### 2025.2.4
- kaliでmetasploitable2を攻撃。Udemyは現行Burpとバージョンが違うのでBurpは公式サイトを見た方が良い
### 2025.2.5
- vsftpd2.3.4にはハッピーフェイス（:)）を入力するとバックドアを仕掛けられる脆弱性が存在する
- metasploitの使い方は次の手順による
1. search hoge
2. show options
3. set hoge fuga
4. exploit
- NWについて
OSPFのコスト計算
1. 拠点〜拠点までの最小コストを算出する。
2. 不明なルートのコストをｘ、ｙとして連立方程式を立てる
3. 連立方程式を解く
### 2025.2.6
- シェルスクリプトによる繰り返しは以下
```bash
for ip in {1..10};do ping 192.168.1.$ip -c 1 2> /dev/null. &;done
```
2> /dev/nullで標準エラー出力を表示しないようにし、&でバックグラウンド処理としている。
バックグラウンド処理にすることで並列処理となり高速化が実現できる。
### 2025.2.7
- vimのコマンドで"命令*i|a+範囲"で一気に指定できる！
aだと範囲内でiだと指定文字を含んだ範囲
### 2025.2.8
- responderはWindowsの認証情報を取得できるセッションハイジャックツール
インターフェースを指定することで通信情報を取得できるため、そのハッシュをjohnすれば認証情報を解析できる。
- クエリストリングのpage=は特定のページやリソースを指定する。
- //<IPアドレス>とすることでリモートファイルを指定できる。/<IPアドレス>だとローカルファイルとして認識される。//はプロトコルを省略した形式でリモートファイルを読み込む。よってRFIの脆弱性があるサイトでは?page=//<自分のIPアドレス>とすることで自分にインターフェースにアクセスさせて情報を取得する。
- evil-winrmはwindowsに対する侵入テストが行える。
### 2025.2.12
##### CISSP学習
- CISSPは人命を最優先に考える。セキュリティ策が人命を上回ることはなく、人命のためには法律に一時的に背くこともある
- CISSPは適切に拘る。過剰でも過小でもダメ。適切が組織の目標達成に貢献する
- CISSPではポリシー、スタンダード、プロシージャが肝。組織の目的・目標を実現するためポリシーが策定される。ポリシーを実現するためスタンダードが策定される。スタンダードを実現するためプロシージャで手順や方法を決める。そしてプロシージャが行われることでスタンダードが実現され、スタンダードが実現されることでポリシーが実現され、組織の目的・目標が実現される。
- CISSPは経営者または経営者を補佐するためのスキルセット
- CISSPの考え方はあくまでも一例
- データオーナー、データコントローラ、データカスケディアン、あと何だったっけ？