#
#　どんといれるだけマスク　ver2.04
#　つくったひと：なべのひと
#

from PIL import Image , ImageOps
import os
import sys

img_keisiki = (".png", ".jpg" , "jpeg" , "bmp" , "gif")


def process_image_file(file_path):

    # コピー先のパスを生成
    base_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_size_str = str(file_size)

    # ログ出力
    process_log_output('変換開始：' + file_name + '(' + file_size_str + 'byte)')

    if file_size > 5000000:
        process_log_output("エラー：" + file_name + "は5MBを超えています。処理をスキップします。")
        return

    #アニメーションGIFはここではねる
    #process_log_output("gifファイルチェック中...")
  
    if file_path.lower().endswith('.gif'):
        with Image.open(file_path) as im:
            if im.n_frames > 1:
                process_log_output("エラー：" + "アニメーションgifは変換できません。処理をスキップします。")
                return
        
    #process_log_output("gifファイルチェック中...OK")
        
            
    # 画像の処理をここに書く
    # 2つのPNGファイルを読み込みます
    img_mask = Image.open(G_mask_path).convert("RGBA")
    img_convert = Image.open(file_path).convert("RGBA")

    img_mask = img_samesize_checker(img_mask, img_convert)

    # マスク明度を反転させる
    if G_worb ==1:
        mask_alpha = ImageOps.invert(img_mask.convert('L'))
        # process_log_output(file_name + 'を変換しました（マスク反転モード）')

    else:
        mask_alpha = img_mask.convert('L')
        # process_log_output(file_name + 'を変換しました')

    # 新しい画像にアルファチャンネルを追加する
    img_convert.putalpha(mask_alpha)

    # 新しいパスを設定して、画像を保存
    convert_path = base_dir + os.path.sep + "copy_"+ file_name

    if convert_path.lower().endswith('.png'):
        img_convert.save(convert_path)
    else:
        convert_path = convert_path + ".png"
        img_convert.save(convert_path,"png")

    # 変換完了メッセージ
    if G_worb ==1:
        process_log_output("変換終了：" + file_name + "（マスク反転モード）")

    else:
        process_log_output("変換終了：" + file_name)


#マスク画像のサイズチェック＆リサイズ
def img_samesize_checker(img_mask, img_convert):
    mask_tupple = img_mask.size
    con_tupple = img_convert.size

    if mask_tupple[0] == con_tupple[0] and mask_tupple[1] == con_tupple[1]:
        process_log_output("画像サイズ確認：マスクと画像のサイズは同一です。処理を続行します。")
        return img_mask
        
    else:
        img_mask_re = img_mask.copy().resize(con_tupple)
        resize_text = str(mask_tupple[0]) + "," + str(mask_tupple[1]) + "→" +str(con_tupple[0]) + "," + str(con_tupple[1])
        process_log_output("画像サイズ確認：マスクと画像のサイズが異なります。マスク画像をリサイズしました："+ resize_text)
        return img_mask_re


#デバッグ用　時間を止める
def timestop(checkpoint):
    print(checkpoint)
    print(type(checkpoint))
    import time
    time.sleep(3)  # 3秒間停止する


#ログをアウトプットします
def process_log_output(log_txt):

    print(log_txt)
    dt_str = Get_datetime_str()

    with open('0_log_file.txt', mode ="a" , encoding="utf-8") as f:
        f.write(log_txt +'　--'+dt_str+ '\n')


# 作業開始時刻の取得
def Get_datetime_str():
    import datetime

    dt_now = datetime.datetime.now()
    dt_str = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    return dt_str


if __name__ == '__main__':

    # 変数の設定        
    i = 0
    r = 0 
    global G_mask_path
    global G_worb
    G_worb = 0

    # ログファイルがなかったら作成
    if os.path.exists("0_log_file.txt"):
        with open("0_log_file.txt", mode="w", encoding="utf-8") as f:
            f.truncate(0)
        
    else:
        dt_str = Get_datetime_str()
        with open("0_log_file.txt",mode ="w" , encoding="utf-8") as f:
            pass

    process_log_output("!!! 起動しました !!!")

    # ドロップされたファイルのパスを取得
    file_paths = sys.argv[1:]


    # マスク画像を検索
    for file_path in file_paths:
        # ファイルのパスを取得
        file_path = os.path.abspath(file_path)

        print(" マスク画像を探しています...：" + file_path)

        #ファイルの数数える用
        r += 1

        # pngでなければ無視
        if not os.path.isfile(file_path) or not file_path.lower().endswith('.png'):
            #print("ファイル形式が違います："+ file_path )
            continue

        #ファイル名にMASKが含まれていたら、処理実行
        if  "mask.png" in file_path:
            process_log_output("マスクファイルを発見しました："+ file_path )
 
            G_mask_path = os.path.abspath(file_path)
            i += 1

        #ファイル名にwが含まれていたら、反転処理する
        #        if  "_W" in file_name.upper():
        if  "_W.PNG" in file_path.upper():
            process_log_output("マスクファイルを発見しました（反転モード）："+ file_path )

            G_mask_path = os.path.abspath(file_path)
            G_worb = 1
            i += 1
        

    #エラーログ出力
    if i == 0:
        process_log_output("エラー：マスク画像ファイルが存在しません。処理を中断しました。")
        sys.exit()

    if i > 1:
        process_log_output("エラー：マスク画像ファイルが複数存在します。処理を中断しました。")
        sys.exit()

    if r == 1:
        process_log_output("ファイルがひとつしかありません。処理を中断しました。")
        sys.exit()        

    process_log_output("マスク画像と" + str(r-1) + "件のファイルを検出しました")
 
    print("ファイルを読み込んでいます...：")

    i=0 #iを初期化

    for file_path in file_paths:
        # ファイルのパスを取得
        file_path = os.path.abspath(file_path)

        # 画像ファイルでなければ無視
        if not os.path.isfile(file_path) or not file_path.lower().endswith(img_keisiki):
            process_log_output("エラー：" + file_path +"は画像ファイルではありません。処理をスキップします")
            continue

        # マスク画像なら無視
        if  "mask.png" in file_path:
          continue

        if  "_W.PNG" in file_path.upper():
          continue

        i += 1
        print(" 画像処理中(" + str(i) + "/" +  str(r-1) + ")：" + file_path)

        # 画像ファイルの処理を実行
        process_image_file(file_path)
