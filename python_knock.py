import csv
lst = [
    {'id': '0001', 'name': 'admin'},
    {'id': '0002', 'name': 'guest'},
    {'id': '0003', 'name': 'test'},
]

with open('test.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file,fieldnames=('id','name'))
    writer.writeheader()
    writer.writerows(lst)



with open('test.csv','r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)

# 問題84まで終了
# セットは集合を意味する。表現は{x,y}
# タプルは組を意味する。複数の要素が決まった順番に並ぶ。表現は(x,y)
# リストは配列を意味する。表現は[x,y]　例えばlist=[1,2,3]ならlist[1]で２番目の要素を取得できる
# 辞書はキーと値から構成される。キーがあるため要素を一意に特定可能。表現は{key:value}
# リスト内包表記は既存のリストから新しいリストを簡単に作成するもの。[式 for x in rnge(1,10) if x % 2 == 0]のように書く
# リスト内の文字を分割したいときはsplit,結合したい時はjoinを使う。lst.split(',')や"&".join(lst)"
# 辞書内容表記というものもある。
# itemsメソッドは辞書のkeyとvalueを取得し、タプルとして返す。タプルはイミュータブルで(1,2)のように表す:w