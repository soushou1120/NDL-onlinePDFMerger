import pypdf
import os
import re


# マージするPDFファイルが入っているフォルダを指定
source_path = 'D://s_dl/ndl/src'
## フォルダにPDFファイルが入っていない場合は終了
## 入っている場合は"マージ作業を開始します"と表示
if not os.listdir(source_path):
    print('フォルダにPDFファイルが入っていません')
    exit()
else:
    print('マージ作業を開始します')

# マージしたPDFファイルを出力するフォルダを指定
library_path = "D:/s_dl/ndl/lib/"

# PDFファイルの名前とパスを取得
pdf_files = []
for filename in os.listdir(source_path):
    if filename.endswith('.pdf'):
        pdf_files.append(os.path.join(source_path, filename))
## PDFファイルの数を表示
print('PDFファイルの数: ' + str(len(pdf_files)))

# ndlの永続的識別子
ndl_id = r"digidepo_(\d+)_"

# ndl_idごとにファイルをグループ化
pdf_files_grouped = {}
for pdf_file in pdf_files:
    ndl_id_match = re.search(ndl_id, pdf_file)
    if ndl_id_match:
        extracted_ndl_id = ndl_id_match.group(1)
        if extracted_ndl_id in pdf_files_grouped:
            pdf_files_grouped[extracted_ndl_id].append(pdf_file)
        else:
            pdf_files_grouped[extracted_ndl_id] = [pdf_file]
## PDFグループの数を表示
print('PDFグループの数: ' + str(len(pdf_files_grouped)))

# ndl_idごとにPDFファイルをソートしてマージ
for ndl_id, pdf_files in pdf_files_grouped.items():
    ## 何個目のグループを処理しているか表示
    print('PDFグループ' + str(list(pdf_files_grouped.keys()).index(ndl_id) + 1) + 'を処理中')
    
    ## PDFファイルのリストをソート
    ## 括弧がない場合は、括弧がある場合よりも前に来るようにする
    ## 括弧がある場合は、括弧の中身でソート
    def sort_key(pdf_file):
        match = re.search(r"\((\d+)\)", pdf_file)
        if match:
            return int(match.group(1))
        else:
            return -1
    pdf_files.sort(key=sort_key)
    
    ## マージしたPDFファイルの名前を設定
    merged_file_name = 'digidepo_' + ndl_id + '_merged.pdf'
    merger = pypdf.PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)

    ## メタデータを設定
    d = pypdf.PdfReader(pdf_files[0]).metadata
    d = {k: d[k] for k in d.keys()}
    merger.add_metadata(d)

    ## メタデータの内、Keywordsを使って、フォルダ名を設定
    ### Keywordsの0番目が著者とタイトル、1番目が出版社、2番目が出版年（不要な情報も含まれる）
    Keywords_title_author = d['/Keywords'].split(',')[0]
    Keywords_publisher = d['/Keywords'].split(',')[1]
    Keywords_year = d['/Keywords'].split(',')[2]
    dot_index = Keywords_year.index('.')
    Keywords_year = Keywords_year[:dot_index] 
    ### フォルダ名は出版社 + 出版年 + ndl_id + 著者とタイトル
    folder_name = Keywords_publisher + '_' + Keywords_year + '_' + ndl_id + '_' + Keywords_title_author
    ## folder_nameからフォルダー名に使えない文字を削除
    folder_name = re.sub(r'[\\/:*?"<>|]', '', folder_name)

    ## マージしたPDFファイルを出力
    ## フォルダを作成して、その中に出力
    library_output_path = os.path.join(library_path, Keywords_publisher, folder_name)
    ## 必要なディレクトリを再帰的に作成
    os.makedirs(source_path, exist_ok=True)
    merger.write(library_output_path + Keywords_publisher + "/" + folder_name + "/" + merged_file_name)
    merger.close()
    print('PDFグループ' + str(list(pdf_files_grouped.keys()).index(ndl_id) + 1) + 'を処理しました')

print('マージ作業が完了しました')