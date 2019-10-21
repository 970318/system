import sys
import numpy as np

with open('report_car_0001.log','r') as foot_data: #report_foot_0001.log を foot_data として開く

    bytes_list = []
    msec_list = []
    for foot in foot_data:
        foot = foot.strip('\n') #オブジェクトから改行を削除する
        foot_list = foot.split(' ') #オブジェクトをスペース区切りで要素として foot_list リストに格納
        bytes_list.append((int(foot_list[4])))
        msec_list.append((int(foot_list[5])))
    #print(bytes_list) #第6列(バイト)の抽出を確認

foot_data.close()

Mbit_list = [n*8/1000000 for n in bytes_list] #byteをMbitに変換
#print(Mbit_list)　#Mbitの確認
sec_list = [n/1000 for n in msec_list] #ミリ秒を秒に変換
#print(sec_list) #secの確認

Mbps_list = [x/y for (x,y) in zip(Mbit_list, sec_list)] # Mbit_list / sec_list で Mbps_list を作成
#print(Mbps_list) #Mbps_list(帯域幅トレース)の確認

#ここまでが帯域幅トレースの準備

tiles_list = [] #各時刻でFovに含まれるタイルの枚数のリスト

for t in range(0,len(Mbps_list)):
    if t % 36 == 0: #FoVに含まれるタイルの枚数が12枚の時
        for i in range(9):
            tiles = 12
            tiles_list.append(tiles)
    if (t+100) % 36 == 0: #FoVに含まれるタイルの枚数が16枚の時
        for j in range(27):
            tiles = 16
            tiles_list.append(tiles)
#print(tiles_list)　#tiles_listの確認
#print(len(tiles＿list))　#tiles_listの要素数の確認

#ここまでが各時刻でFoVに含まれるタイルの枚数を記録したリスト作成

def resultCalc(MbpsItem,tilesItem,brItem): #tiles_listの１つの要素に対してbr_listの要素をかけてその積をMbps_listの対応する要素と比較する
    for brItem in br_list: #br_list内のパターン毎の係数をfor文で回す
        multipleResult = tilesItem * brItem #FoV内の映像品質を計算する
        if(multipleResult < MbpsItem): #帯域幅と比較する
            return multipleResult #帯域幅よりも小さいビットレートが決まったらその値を返す
    return 0.0 #帯域幅に治らなかったら0を返す

if __name__=='__main__':

    br_list = np.arange(3.6,1.5,-0.4) #各パターンのビットレートリスト(Mbps)
    quality_list = [] #最終的に決定した各時間の映像品質を格納するリスト

    for index in range(len(Mbps_list)):
        quality_list.append(resultCalc(Mbps_list[index],tiles_list[index],br_list)) #quality_listにFoV内の最終的に決定した映像品質を格納する

print(quality_list) #quality_listの表示
print(len(quality_list)) #quality_listの要素数
print(sum(quality_list)) #全映像品質の合計
