import pandas as pd
import os
from scipy import arange, hamming, sin, pi
from scipy.fftpack import fft, ifft
from matplotlib import pylab as plt
import numpy as np

#ディレクトリの指定
os.chdir("C:/Users/kento/Desktop/データM1")
class frequency():

    MONTH = ""
    DAY = ""
    SENSOR = ""
    main_df = pd.DataFrame(columns=['X', 'Y', 'Z'])

    def __init__(self):
        pass

    def input_number(self):
        self.MONTH = input("何月?")
        if len(self.MONTH) == 1:
            self.MONTH = '0' + str(self.MONTH)
        else:
            self.MONTH = str(self.MONTH)

            self.DAY = input("何日?")
        if len(self.DAY) == 1:
            self.DAY = '0' + str(self.DAY)
        else:
            self.DAY = str(self.DAY)

            self.SENSOR = input("センサーは?")

    def dataframe(self):
        for i in range(4,17):
            if len(str(i)) == 1:
                HOUR = '0' + str(i)
            else:
                HOUR = str(i)
            file_name = '2017' + self.MONTH + self.DAY + HOUR + ' ' + self.SENSOR + 'sec.csv'

            try:
                df = pd.read_csv(file_name, names = list("ABXYZ"))
            except:
                continue

            drop_col = ['A', 'B']
            df = df.drop(drop_col, axis=1)
            self.main_df = pd.concat([self.main_df, df],ignore_index=True)

    def Sum_Squares(self):
        a = []
        for i in range(0,46800):
            square = self.main_df.ix[i,1]**2 + self.main_df.ix[i,1]**2 + self.main_df.ix[i,2]**2
            a.append(square)
            print(i)

        series = pd.Series(a)
        df = pd.DataFrame(series, columns=['Square'])

        self.main_df = pd.concat([self.main_df, df], axis=1)
        print(self.main_df)
        file_name = '2017' + self.MONTH + self.DAY + ' ' + self.SENSOR + 'sec Square.csv'
        self.main_df.to_csv(file_name)

    def Calc(self):
        f = self.main_df['Square'] - 1

        # データのパラメータ
        N = 46800  # サンプル数
        dt = 1/60 # サンプリング間隔 1分間の周波数を求める

        t = np.arange(0, N * dt, dt)  # 時間軸
        freq = np.linspace(0, 1.0 / dt, N)  # 周波数軸
        window = hamming(N) #窓関数
        #データを加工
        f = f * window
        # 高速フーリエ変換
        F = np.fft.fft(f)

        # 振幅スペクトルを計算
        Amp = np.abs(F)

        # グラフ表示
        plt.figure()
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 17
        plt.subplot(121)
        plt.plot(t, f, label='f(n)')
        plt.xlabel("Time", fontsize=20)
        plt.ylabel("Signal", fontsize=20)
        plt.grid()
        leg = plt.legend(loc=1, fontsize=25)
        leg.get_frame().set_alpha(1)
        plt.subplot(122)
        plt.plot(freq, Amp, label='|F(k)|')
        plt.xlabel('Frequency', fontsize=20)
        plt.ylabel('Amplitude', fontsize=20)
        plt.grid()
        leg = plt.legend(loc=1, fontsize=25)
        leg.get_frame().set_alpha(1)
        plt.show()

f = frequency()
f.input_number()
f.dataframe()
f.Sum_Squares()
f.Calc()




