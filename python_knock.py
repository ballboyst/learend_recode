# target = "hello"
# for num in target:
#     print(num)
# lst = "hello"
# dict = {}
# for char in lst:
#     if char in dict:
#         dict[char] += 1
#     else:
#         dict[char] = 1
# print(dict)
target_list = [1, 2, 3, None, 5]
for num in target_list:
    try:
        print(num * 2)
    except TypeError as e:
        print(e)
# 問題59まで終了
# タプルは組を意味する。複数の要素が決まった順番に並ぶ。表現は(x,y)
# リストは配列を意味する。表現は[x,y]　例えばlist=[1,2,3]ならlist[1]で２番目の要素を取得できる
# 辞書はキーと値から構成される。キーがあるため要素を一意に特定可能。表現は{key:value}
# リスト内包表記は既存のリストから新しいリストを簡単に作成するもの。[式 for x in rnge(1,10) if x % 2 == 0]のように書く
# リスト内の文字を分割したいときはsplit,結合したい時はjoinを使う。lst.split(',')や"&".join(lst)"
# 辞書内容表記というものもある。
# itemsメソッドは辞書のkeyとvalueを取得し、タプルとして返す。タプルはイミュータブルで(1,2)のように表す