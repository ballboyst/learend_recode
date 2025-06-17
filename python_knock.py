
class SimpleClass():
    count = 0  # class変数
    def __init__(self,name):
        self.name = name
        SimpleClass.count += 1  # class.valueでclass変数にアクセスする
    def print_count(self):
        print(f'{SimpleClass.count}回目のクラスが作成されました')
    def print_name(self):
        print(f'名前が{self.name}のオブジェクトを作成しました')

Tom = SimpleClass('tom')
Tom.print_count()
Alice = SimpleClass('Alice')
Alice.print_count()
# 上記でも同じ出力は得られるが、以下のコードが模範解答

class SimpleClass():
    count = 0  # class変数
    def __init__(self,name):
        self.name = name
        SimpleClass.count += 1  # class.valueでclass変数にアクセスする
    @classmethod
    def print_count(cls):
        print(cls.count)

SimpleClass.print_count()
Sample = SimpleClass("aa")
SimpleClass.print_count()

# 問題67まで終了
# セットは集合を意味する。表現は{x,y}
# タプルは組を意味する。複数の要素が決まった順番に並ぶ。表現は(x,y)
# リストは配列を意味する。表現は[x,y]　例えばlist=[1,2,3]ならlist[1]で２番目の要素を取得できる
# 辞書はキーと値から構成される。キーがあるため要素を一意に特定可能。表現は{key:value}
# リスト内包表記は既存のリストから新しいリストを簡単に作成するもの。[式 for x in rnge(1,10) if x % 2 == 0]のように書く
# リスト内の文字を分割したいときはsplit,結合したい時はjoinを使う。lst.split(',')や"&".join(lst)"
# 辞書内容表記というものもある。
# itemsメソッドは辞書のkeyとvalueを取得し、タプルとして返す。タプルはイミュータブルで(1,2)のように表す