# classは属性をまとめたもの
class Item:         # クラスの定義

    
    def __init__(self, name, price):
        self.name = name
        self.price = price


    def message_item(self):         # クラスメソッドの定義
        print(f'{self.name}商品の値段は{self.price}です')

item1 = Item("卵", 100)
item2 = Item("牛乳", 150)

print(item1)        # item1オブジェクトの情報を表示
print(item1.name)   # item1インスタンスのname属性の値を表示
print(item2.price)  # item2インスタンスのprice属性の値を表示

item2.message_item()


# 上記のクラス定義に型ヒントを加えると次のようになる。
class Item:

    
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price


# クラス定義にdataclassを使った場合
from datetime import date, datetime
from dataclasses import dataclass

@dataclass
class User:
    name:str
    email:str
    age:int
    address: str
    birthday: date
    phone_number: str
    is_admin: bool
    is_active: bool
    last_login: datetime
    date_joined: datetime
    

# 上記クラスをdataclassを使わず定義した場合、以下のように長くなる
from datetime import date, datetime

class User:
    def __init__(
        self,
        name:str,
        email:str,
        age:int,
        address: str,
        birthday: date,
        phone_number: str,
        is_admin: bool,
        is_active: bool,
        last_login: datetime,
        date_joined: datetime,
    ):
        self.name = name
        self.email = email
        self.age = age
        self.address = addresss
        self.birthday = birthday
        self.phone_number= phone_number 
        self.is_admin= is_admin
        self.is_active= is_active
        self.last_login= last_login
        self.date_joined= date_joined

# classにデフォルト値を設定する（今回はis_adminとdate_joinedに設定）
# 注意点として、デフォルト値を設定するものはデフォルト値が無いものより後ろに書かないとTypeErrorになる
from datetime import date, datetime
from dataclasses import dataclass

@dataclass
class User:
    name:str
    email:str
    age:int
    address: str
    birthday: date
    phone_number: str
    is_active: bool
    last_login: datetime
    is_admin: bool = False
    date_joined: datetime = datetime.now()

# カプセル化
# インスタンス変数を安全に扱うために先頭に_をつける。
class Item:
    
    def __init__(self, name, price):
        self.name = name
        self._price = price


    def set_price(self, price):
        assert price >= 0, "価格は０以上にする必要がある"
        assert isinstance(
                price, int
        ), "価格はintにする必要がある"
        self._price = price


    def get_price(self):
        return self._price


item_1 = Item("新鮮！山の卵", 250)
item_1.set_price(300)
print(item_1.get_price())

# コマンドプロンプトで指定したコマンドを実行し結果を表示するコード
import subprocess       # 従来のos.systemの代替


command = 'dir'     # 実行するコマンド
result = subprocess.run(command, shell=True, text=True, capture_output=True)
print("コマンド:", command)
print("実行結果：")
print(result.stdout)
print("エラー出力:")
print(result.stderr)


# ジャンケンプログラム
# import random
# array = ["グー","チョキ","パー"]
# cpu = random.randint(0, 2)
# int(input("あなたは何を出しますか？数字で入力してください\n0:グー\n:1:チョキ\n2:パー"))
# display = array[input]
# print(f"あなたは{array[input]}を選びました")


# def judge():
#     result = (cpu - input + 3) % 3
#     if result == 0:
#         print("あいこです")
#     elif result == 1:
#         print("あなたの勝ちです")
#     else:
#         print("あなたの負けです")

# judge()
# print(f"相手は{array[cpu]}でした")


# 上記コードをAIでリファクタリングしたあと、arrayを関数外にだし共通化したもの
import random


array = ["グー", "チョキ", "パー"]      # 表示用に準備した配列。他関数で使用


def get_player_choice():
    while True:         # 条件がTrueで固定されているため無限ループとなる。
        try:
            choice = int(input("あなたは何を出しますか？数字で入力してください\n0:グー\n1:チョキ\n2:パー\n"))
            if choice in [0, 1, 2]:
                return choice       # 入力が正しい場合、returnで関数を抜け、無限ループが終わる。
            else:
                print("0から2の数字を入力してください。")
        except ValueError:
            print("数値で入力してください。")

def judge(cpu, player):
    result = (cpu - player + 3) % 3
    if result == 0:
        return "あいこです"
    elif result == 1:
        return "あなたの勝ちです"
    else:
        return "あなたの負けです"

def main():
    cpu = random.randint(0, 2)
    player = get_player_choice()
    print(f"あなたは{array[player]}を選びました")
    print(f"相手は{array[cpu]}でした")
    print(judge(cpu, player))

if __name__ == "__main__":     # このファイルが直接実行された場合のみmain()を実行する
    main()


def add_number(a, b):
    return a + b


