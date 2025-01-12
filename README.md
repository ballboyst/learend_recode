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