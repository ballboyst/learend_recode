# クラス定義
class Sample:
    count = 0  # 関数外のクラス内で定義されている変数はクラス変数といいクラスで共通の変数

    def __init__(self, name):
        self.name = name
        Sample.count += 1
        print('hello')
	
    def print_name(self):
        print(f'{self.name}を登録しました。')

# クラスの使用
Sample('PY').print_name()
x = Sample('AA')
print(x.count)

# 問題84まで終了
# セットは集合を意味する。表現は{x,y}
# タプルは組を意味する。複数の要素が決まった順番に並ぶ。表現は(x,y)
# リストは配列を意味する。表現は[x,y]　例えばlist=[1,2,3]ならlist[1]で２番目の要素を取得できる
# 辞書はキーと値から構成される。キーがあるため要素を一意に特定可能。表現は{key:value}
# リスト内包表記は既存のリストから新しいリストを簡単に作成するもの。[式 for x in rnge(1,10) if x % 2 == 0]のように書く
# リスト内の文字を分割したいときはsplit,結合したい時はjoinを使う。lst.split(',')や"&".join(lst)"
# 辞書内容表記というものもある。
# itemsメソッドは辞書のkeyとvalueを取得し、タプルとして返す。タプルはイミュータブルで(1,2)のように表す