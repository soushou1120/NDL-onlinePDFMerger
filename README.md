# NDL-onlinePDFMerger
NDL onlineからダウンロードしたPDFの結合と整理をします
# 1. フォルダの準備
PDFをダウンロードするフォルダと、結合したPDFを保存するフォルダを用意してください
# 2. パスの指定
```
source_path = 'PDFをダウンロードするフォルダのパス'
library_path = '結合したPDFを保存するフォルダのパス'
```
# 3. PDFのダウンロード
ダウンロード先は当然`source_path`に指定したフォルダ

metadataがちゃんと保存されるように(そして負荷をかけないために)、「PDFファイルを開く」を右クリックして「名前をつけてリンク先を保存」からダウンロード
## 個人送信対応の資料の場合
「印刷」からPDFをダウンロードする

`1-50`,`51-100`,`101-150`のように、50コマずつ指定してダウンロードする必要がある

## ログインなしで閲覧可能な資料の場合
「印刷」か、下部にある「ダウンロード」からPDFを選択し、すべてのコマをダウンロードする
# 4. PDFファイルの結合と振り分け
欲しい資料をダウンロードし終えたら、`NDL-onlinePDFMerger.py`を実行する
## 結合の仕様
資料についている永続的識別子`ndl_id`に基づいて各資料を結合します
### 結合の順番
「名前をつけてリンク先を保存」を選択時に自動で付与された括弧つきの連番を利用してソートし、結合します
### metadata
最初に保存されたPDFファイル（括弧つきの連番がついてないPDFファイル）につけられているmetadataを、結合後のPDFファイルに付与します
### ファイル名
ダウンロード時のファイル名とあまり変わらないように、
```
merged_file_name = 'digidepo_' + ndl_id + '_merged.pdf'
```
で保存します
## 振り分けの仕様
メタデータのうち、`/Keywords`を利用してPDFファイルを振り分けます
### フォルダを作成
`library_path`の下に、二つのフォルダを作成します

`/Keywords`に含まれる、著者とタイトル`Keywords_title_author`、出版社`Keywords_publisher`、出版年`Keywords_year`のデータを利用して、
```
folder_name = Keywords_publisher + '_' + Keywords_year + '_' + ndl_id + '_' + Keywords_title_author
library_path/Keywords_publisher/folder_name
```
と、出版社の階層の下に、出版社_出版年_`ndl_id`_著者とタイトルの階層を作ります

すなわち、`D://hogehoge/中央公論社/中央公論社_昭和10_1234567_矢田插雲 著『太閤記』第9巻`のような形式です
