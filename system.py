import sys
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

with open('report_car_0001.log','r') as car_data: #report_car_0001.log を car_data として開く

    bytes_list = []
    msec_list = []
    for car in car_data:
        car = car.strip('\n') #オブジェクトから改行を削除する
        car_list = car.split(' ') #オブジェクトをスペース区切りで要素として car_list リストに格納
        bytes_list.append((int(car_list[4])))
        msec_list.append((int(car_list[5])))
    #print(bytes_list) #第6列(バイト)の抽出を確認

car_data.close()

mbit_list = [n*8/1000000 for n in bytes_list] #byteをMbitに変換
#print(mbit_list)　#Mbitの確認
sec_list = [n/1000 for n in msec_list] #ミリ秒を秒に変換
#print(sec_list) #secの確認

mbps_list = [x/y for (x,y) in zip(mbit_list, sec_list)] # mbit_list / sec_list で mbps_list を作成
#print(mbps_list) #mbps_list(帯域幅トレース)の確認

"""ここまでが帯域幅トレースの準備"""

tilesinFoV_list = [] #各時刻でFovに含まれるタイルの枚数のリスト

for t in range(0,len(mbps_list)):
    if t % 36 == 0: #FoVに含まれるタイルの枚数が12枚の時
        for i in range(9):
            tiles = 12
            tilesinFoV_list.append(tiles)
    if (t+100) % 36 == 0: #FoVに含まれるタイルの枚数が16枚の時
        for j in range(27):
            tiles = 16
            tilesinFoV_list.append(tiles)

"""ここまでが各時刻でFoVに含まれるタイルの枚数を記録したリスト作成"""


def makePattern(mbps_item,tiles_item,br_list): #TilesinFoV_listの１つの要素に対してbr_listの要素をかけてその積をMbps_listの対応する要素と比較
    for br_item in br_list: #br_list内の要素をfor文で回す
        totalBR = tiles_item * br_item #ビットレート * タイルの枚数
        if(totalBR < mbps_item): #mbps_list内の対応する要素と値の大きさを比較する
            return totalBR #mbps_itemより小さくなったらその値を返す
    return 0.0 #収まらなかったら0を返す

if __name__=='__main__':

    br_list = np.arange(3.6,1.5,-0.4) #ビットレートパターンリスト(Mbps)
    serverBuf = deque([]) #最終的に決定した各時間の映像品質を格納するリスト
    rend_list = []
    bufSize = input()
    bufSize_int = int(bufSize)

    for index in range(len(mbps_list)): #サーババッファに格納
        serverBuf.append(makePattern(mbps_list[index],tilesinFoV_list[index],br_list)) #関数makePatternで返された値を格納する
        if(len(serverBuf) == bufSize_int): 
            rend_list.append(serverBuf[0]) #serverBufの先頭の要素をrend_listに移動
            serverBuf.popleft() #serveBufの先頭の要素を削除

    if(len(serverBuf)>0): #serverBufに残った要素をrend_listに移動
        for n in range(len(serverBuf)):
            rend_list.append(serverBuf[0])
            serverBuf.popleft()

print(serverBuf) #serverBufの表示
print(rend_list) #rend_listの表示
print(len(rend_list)) #rend_listの要素数
print(sum(rend_list)) #全映像品質の合計