dict = {'id': '0001', 'name': 'guest'}
for key, value in dict.items():
    print(f'key:{key},value:{value}')

lst = [n for n in range(1,10) if n%2 == 0]
print(lst)

x = "1,2,3"
lst = x.split(",")
print(lst)
lst2 = '&'.join(x)
print(lst2)
# 問題43まで終了
# タプルは組を意味する。複数の要素が決まった順番に並ぶ。表現は(x,y)
# リストは配列を意味する。表現は[x,y]　例えばlist=[1,2,3]ならlist[1]で２番目の要素を取得できる
# 辞書はキーと値から構成される。キーがあるため要素を一意に特定可能。表現は{key:value}
# リスト内包表記は既存のリストから新しいリストを簡単に作成するもの。[式 for x in rnge(1,10) if x % 2 == 0]のように書く
# リスト内の文字を分割したいときはsplit,結合したい時はjoinを使う。lst.split(',')や"&".join(lst)"