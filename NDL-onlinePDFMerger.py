import pypdf
import os
import re


# マージするPDFファイルが入っているフォルダを指定
source_path = 'D://s_dl/ndl/src'
# マージしたPDFファイルを出力するフォルダを指定
library_path = 'D://s_dl/ndl/lib'
## フォルダにPDFファイルが入っていない場合は終了
## 入っている場合は"マージ作業を開始します"と表示
if not os.listdir(source_path):
    print('フォルダにPDFファイルが入っていません')
    exit()
else:
    print('マージ作業を開始します')

# ndlの永続的識別子の正規表現
ndl_id_re = r'digidepo_(\d+)_'

# PDFファイルの名前とパスを取得
def get_pdf_files(source_path):
    pdf_files = []
    for filename in os.listdir(source_path):
        if filename.endswith('.pdf'):
            pdf_files.append(os.path.join(source_path, filename))
    ## PDFファイルの数を表示
    print('PDFファイルの数: ' + str(len(pdf_files)))
    return pdf_files

# ndl_idごとにファイルをグループ化
def group_pdf_files(pdf_files):
    pdf_files_grouped = {}
    for pdf_file in pdf_files:
        ndl_id_match = re.search(ndl_id_re, pdf_file)
        if ndl_id_match:
            extracted_ndl_id = ndl_id_match.group(1)
            if extracted_ndl_id in pdf_files_grouped:
                pdf_files_grouped[extracted_ndl_id].append(pdf_file)
            else:
                pdf_files_grouped[extracted_ndl_id] = [pdf_file]
    ## PDFグループの数を表示
    print('PDFグループの数: ' + str(len(pdf_files_grouped)))
    return pdf_files_grouped

# ndl_idごとにPDFファイルをソートしてマージ
def merge_pdf_files(pdf_files_grouped):
    for ndl_id, pdf_files in pdf_files_grouped.items():
        ## 何個目のグループを処理しているか、ndl_idと共に表示
        print(' ')
        print('PDFグループ' + str(list(pdf_files_grouped.keys()).index(ndl_id) + 1) + ':' + ndl_id + 'を処理中')
        
        ## PDFファイルのリストをソート
        ## 括弧がない場合は、括弧がある場合よりも前に来るようにする
        ## 括弧がある場合は、括弧の中身でソート
        def sort_key(pdf_file):
            match = re.search(r'\((\d+)\)', pdf_file)
            if match:
                return int(match.group(1))
            else:
                return -1
        pdf_files.sort(key=sort_key)
        
        ## メタデータを設定
        ## 実際にメタデータを設定するのは、PDFをマージした後
        pdf_metadata = pypdf.PdfReader(pdf_files[0]).metadata
        pdf_metadata = {k: pdf_metadata[k] for k in pdf_metadata.keys()}

        ## メタデータの内、Keywordsを使って、フォルダ名を設定
        ### Keywordsはテキストで、カンマで区切られている
        ### しかし、著者が複数の場合にもカンマが含まれていることがあるため、前後にスペースがないカンマで区切ることで解決する必要がある　（スペースが前または後にあるカンマは区分内の区分に用いられている）
        ### Keywordsの0番目が著者とタイトル、1番目が出版社、2番目が出版年 （不要な情報も含まれている）
        print(pdf_metadata['/Keywords'])

        ### Keywordsをカンマで区切る関数
        def Keywords_splitter(Keywords):
            Keywords_slicer = [m.start() for m in re.finditer(r'\S,\S', Keywords)]
            parts = []
            start = 0
            for slicer in Keywords_slicer:
                part = Keywords[start:slicer + 1]
                parts.append(part)
                start = slicer + 2
            parts.append(Keywords[start:])
            return parts
        Split_keywords = Keywords_splitter(pdf_metadata['/Keywords'])
        
        ### 分かりやすくするために、Keywordsの要素を変数に代入
        Keywords_title_author = Split_keywords[0]
        Keywords_publisher = Split_keywords[1]
        Keywords_year = Split_keywords[2]
        dot_index = Keywords_year.index('.')
        Keywords_year = Keywords_year[:dot_index]

        ### フォルダ名は出版社 + 出版年 + ndl_id + 著者とタイトル
        folder_name = Keywords_publisher + '_' + Keywords_year + '_' + ndl_id + '_' + Keywords_title_author
        ### folder_nameからフォルダー名に使えない文字を削除
        folder_name = re.sub(r'[\\/:*?"<>|]', '', folder_name)
        print(folder_name)

        ## マージしたPDFファイルの名前を設定
        merged_file_name = Keywords_title_author + '_' + ndl_id + '.pdf'
        ## マージする
        merger = pypdf.PdfMerger()
        for pdf_file in pdf_files:
            merger.append(pdf_file)
        ## ここでメタデータを設定
        merger.add_metadata(pdf_metadata)

        ## マージしたPDFファイルを出力
        ### フォルダを作成して、その中に出力
        library_output_path = os.path.join(library_path, Keywords_publisher, folder_name)
        ### 必要なディレクトリを作成
        os.makedirs(library_output_path, exist_ok=True)
        merger.write(library_output_path + '/' + merged_file_name)
        merger.close()
        print('PDFグループ' + str(list(pdf_files_grouped.keys()).index(ndl_id) + 1) + 'を処理しました')
    print(' ')
    print('マージ作業が完了しました')

if __name__ == '__main__':
    pdf_files = get_pdf_files(source_path)
    pdf_files_grouped = group_pdf_files(pdf_files)
    merge_pdf_files(pdf_files_grouped)
