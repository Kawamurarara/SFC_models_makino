import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt
import japanize_matplotlib #日本語を有効化するモジュールをインポート
plt.rcParams['xtick.direction'] = 'in' #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in' #y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['xtick.major.width'] = 1 #x軸主目盛り線の線幅
plt.rcParams['ytick.major.width'] = 1 #y軸主目盛り線の線幅
plt.rcParams['font.size'] = 10.5 #フォントの大きさ
plt.rcParams['axes.linewidth'] = 1 # 軸の線幅edge linewidth。囲みの太さ

##変数
#生産
X = [[200, 250, 400, 500, 400]]
x = [[[16, 23, 9, 2, 10],
     [17, 24, 0, 40, 14],
     [18, 26, 78, 54, 54],
     [19, 28, 93, 140, 15],
     [20, 29, 90, 124, 55]]]
#付加価値
y_p = [[110, 120, 130, 140, 252]]
Y = [752]
#可処分所得
YD = [652]
YD_e = [652]
#税金
T = [115]
#消費
C = [652]
c_p = [[135, 145, 155, 185, 32]]

##外生変数
#政府支出
G = 100
g_p = [5, 10, 15, 20, 50]
#利子率
r = 0.025

##先決内生変数
#正味資産残高
V = [800]
V_e = [800]
#債権
B_d = [600]
B_h = [600]
B_s = [800]
B_cb = [200]
ΔB_h = [0]
ΔB_s = [0]
ΔB_cb = [0]
#準備預金
H_d = [200]
H_s = [200]
H_h = [200]
ΔH_s = [0]
#家計・貨幣保有割合
H_h_V = [0.250]

##パラメター
#投入係数
a = [[16/200, 23/250, 9/400, 2/500, 10/400],
     [17/200, 24/250, 0, 40/500, 14/400],
     [18/200, 26/250, 78/400, 54/500, 54/400],
     [19/200, 28/250, 93/400, 140/500, 15/400],
     [20/200, 29/250, 90/400, 124/500, 55/400]]
#付加価値率
v = [110/200, 120/250, 130/400, 140/500, 252/400]
#消費シェア
c = [135/652, 145/652, 155/652, 185/652, 32/652]
#税率
θ = 115/767
#消費・可処分所得(期首の期待)に関するパラメター
α_1 = 3/4
#消費・[期首]正味資産残高に関するパラメター
α_2 = 163/800
#貨幣需要・定数項
λ_0 = 0.752
#貨幣需要・資産需要に関するパラメター
λ_1 = 0.900
#資産需要・取引需要に関するパラメター
λ_2 = 0.030

##各産業における生産額を求めるための行列
#生産額を求めるための行列A
A = [[1 - a[0][0], -a[0][1], -a[0][2], -a[0][3], -a[0][4]],
     [-a[1][0], 1 - a[1][1], -a[1][2], -a[1][3], -a[1][4]],
     [-a[2][0], -a[2][1], 1 - a[2][2], -a[2][3], -a[2][4]],
     [-a[3][0], -a[3][1], -a[3][2], 1 - a[3][3], -a[3][4]],
     [-a[4][0], -a[4][1], -a[4][2], -a[4][3], 1 - a[4][4]]]
#消費と政府支出を足し合わせた列ベクトル
B = [[140, 155, 170, 205, 82]]

#コピー
X1, X2, X3, X4, X5, X6 = X.copy(), X.copy(), X.copy(), X.copy(), X.copy(), X.copy()
x1, x2, x3, x4, x5, x6 = x.copy(), x.copy(), x.copy(), x.copy(), x.copy(), x.copy()
y_p1, y_p2, y_p3, y_p4, y_p5, y_p6 = y_p.copy(), y_p.copy(), y_p.copy(), y_p.copy(), y_p.copy(), y_p.copy()
Y1, Y2, Y3, Y4, Y5, Y6 = Y.copy(), Y.copy(), Y.copy(), Y.copy(), Y.copy(), Y.copy()
YD1, YD2, YD3, YD4, YD5, YD6 = YD.copy(), YD.copy(), YD.copy(), YD.copy(), YD.copy(), YD.copy()
YD_e1, YD_e2, YD_e3, YD_e4, YD_e5, YD_e6 = YD_e.copy(), YD_e.copy(), YD_e.copy(), YD_e.copy(), YD_e.copy(), YD_e.copy()
T1, T2, T3, T4, T5, T6 = T.copy(), T.copy(), T.copy(), T.copy(), T.copy(), T.copy()
C1, C2, C3, C4, C5, C6 = C.copy(), C.copy(), C.copy(), C.copy(), C.copy(), C.copy()
c_p1, c_p2, c_p3, c_p4, c_p5, c_p6 = c_p.copy(), c_p.copy(), c_p.copy(), c_p.copy(), c_p.copy(), c_p.copy()
V1, V2, V3, V4, V5, V6 = V.copy(), V.copy(), V.copy(), V.copy(), V.copy(), V.copy()
V_e1, V_e2, V_e3, V_e4, V_e5, V_e6 = V_e.copy(), V_e.copy(), V_e.copy(), V_e.copy(), V_e.copy(), V_e.copy()
B_d1, B_d2, B_d3, B_d4, B_d5, B_d6 = B_d.copy(), B_d.copy(), B_d.copy(), B_d.copy(), B_d.copy(), B_d.copy()
B_h1, B_h2, B_h3, B_h4, B_h5, B_h6 = B_h.copy(), B_h.copy(), B_h.copy(), B_h.copy(), B_h.copy(), B_h.copy()
B_s1, B_s2, B_s3, B_s4, B_s5, B_s6 = B_s.copy(), B_s.copy(), B_s.copy(), B_s.copy(), B_s.copy(), B_s.copy()
B_cb1, B_cb2, B_cb3, B_cb4, B_cb5, B_cb6 = B_cb.copy(), B_cb.copy(), B_cb.copy(), B_cb.copy(), B_cb.copy(), B_cb.copy()
ΔB_h1, ΔB_h2, ΔB_h3, ΔB_h4, ΔB_h5, ΔB_h6 = ΔB_h.copy(), ΔB_h.copy(), ΔB_h.copy(), ΔB_h.copy(), ΔB_h.copy(), ΔB_h.copy()
ΔB_s1, ΔB_s2, ΔB_s3, ΔB_s4, ΔB_s5, ΔB_s6 = ΔB_s.copy(), ΔB_s.copy(), ΔB_s.copy(), ΔB_s.copy(), ΔB_s.copy(), ΔB_s.copy()
ΔB_cb1, ΔB_cb2, ΔB_cb3, ΔB_cb4, ΔB_cb5, ΔB_cb6 = ΔB_cb.copy(), ΔB_cb.copy(), ΔB_cb.copy(), ΔB_cb.copy(), ΔB_cb.copy(), ΔB_cb.copy()
H_d1, H_d2, H_d3, H_d4, H_d5, H_d6 = H_d.copy(), H_d.copy(), H_d.copy(), H_d.copy(), H_d.copy(), H_d.copy()
H_s1, H_s2, H_s3, H_s4, H_s5, H_s6 = H_s.copy(), H_s.copy(), H_s.copy(), H_s.copy(), H_s.copy(), H_s.copy()
H_h1, H_h2, H_h3, H_h4, H_h5, H_h6 = H_h.copy(), H_h.copy(), H_h.copy(), H_h.copy(), H_h.copy(), H_h.copy()
ΔH_s1, ΔH_s2, ΔH_s3, ΔH_s4, ΔH_s5, ΔH_s6 = ΔH_s.copy(), ΔH_s.copy(), ΔH_s.copy(), ΔH_s.copy(), ΔH_s.copy(), ΔH_s.copy()
B1, B2, B3, B4, B5, B6 = B.copy(), B.copy(), B.copy(), B.copy(), B.copy(), B.copy()
H_h_V1, H_h_V2, H_h_V3, H_h_V4, H_h_V5, H_h_V6 = H_h_V.copy(), H_h_V.copy(), H_h_V.copy(), H_h_V.copy(), H_h_V.copy(), H_h_V.copy()

def model(X, x, y_p, Y, YD, YD_e, T, C, c_p, G, g_p, r, V, V_e, B_d, B_h, B_s, B_cb, ΔB_h, ΔB_s, ΔB_cb, H_d, H_s, H_h, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B, H_h_V, t):
    B.append([])
    x.append([])
    y_p.append([])
    c_p.append([])

    #期待可処分所得を求める
    YD_e.append(YD[-1])
    #消費総額を求める
    C.append(α_1 * YD_e[-1] + α_2 * V[-1])
    #各産業における消費額を求める
    for i in range(5):
        c_p[t].append(C[-1] * c[i])
    #消費と政府支出の和を求める
    for i in range(5):
        B[t].append(g_p[i] + c_p[t][i])
    #各産業における生産額を求める
    X.append(solve(A, B[t]).tolist())
    #各産業における中間投入を求める
    for i in range(5):
        x[t].append([])
        for j in range(5):
            x[t][i].append(a[i][j] * X[t][j])
    #各産業における付加価値を求める
    for i in range(5):
        y_p[t].append(v[i] * X[t][i])
    #付加価値の総額を求める
    Y.append(sum(y_p[t]))
    #税金を求める
    T.append(θ * (Y[-1] + r * B_h[-1]))
    #可処分所得を求める
    YD.append(Y[-1] - T[-1] + r * B_h[-1])
    #期首時点の期末正味資産残高の期待値を求める
    V_e.append(V[-1] + YD_e[-1] - C[-1])
    #期末正味資産残高を求める
    V.append(V[-1] + YD[-1] - C[-1])
    #家計の、期末正味資産残高の期待値を求める
    B_d.append(V_e[-1] *(λ_0 + λ_1 * r) - λ_2 * YD_e[-1])
    #家計の、債券保有割合の計画値
    H_d.append(V_e[-1] - B_d[-1])
    #家計は期末に計画通り、債券を保有する
    B_h.append(B_d[-1])
    #家計は、期末における正味資産残高の期待値と実際値のずれを、貨幣保有残高により調整する
    H_h.append(V[-1] - B_h[-1])
    #家計・債券保有純増を求める
    ΔB_h.append(B_h[-1] - B_h[-2])
    #政府の新たな債券発行額を求める
    ΔB_s.append(G + r * B_s[-1] - (T[-1] + r * B_cb[-1]))
    #政府の、期末の債券発行残高を求める
    B_s.append(B_s[-1] + ΔB_s[-1])
    #中央銀行による買いオペ
    B_cb.append(B_s[-1] - B_h[-1])
    #中央銀行・債券保有純増を求める
    ΔB_cb.append(B_cb[-1] - B_cb[-2])
    #期末の貨幣発行残高を求める
    H_s.append(H_s[-1] + ΔB_cb[-1])
    #中央銀行・貨幣発行純増を求める
    ΔH_s.append(H_s[-1] - H_s[-2])
    #家計・貨幣保有割合を求める
    H_h_V.append(H_h[-1] / V[-1])

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)
Time = [i for i in range(0, 51)]

#定常状態
for t in range(1,51):
        model(X, x, y_p, Y, YD, YD_e, T, C, c_p, G, g_p, r, V, V_e, B_d, B_h, B_s, B_cb, ΔB_h, ΔB_s, ΔB_cb, H_d, H_s, H_h, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B, H_h_V, t)
line = ax.plot(Time, H_h_V, label = "定常状態")

#第５期のみ第４財への財政支出を20から30に変更
for t in range(1,51):
    if t < 5:
        model(X1, x1, y_p1, Y1, YD1, YD_e1, T1, C1, c_p1, G, g_p, r, V1, V_e1, B_d1, B_h1, B_s1, B_cb1, ΔB_h1, ΔB_s1, ΔB_cb1, H_d1, H_s1, H_h1, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B1, H_h_V1, t)
    elif t == 5:
        G = 110
        g_p = [5, 10, 15, 30, 50]
        model(X1, x1, y_p1, Y1, YD1, YD_e1, T1, C1, c_p1, G, g_p, r, V1, V_e1, B_d1, B_h1, B_s1, B_cb1, ΔB_h1, ΔB_s1, ΔB_cb1, H_d1, H_s1, H_h1, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B1, H_h_V1, t)
    else:
        G = 100
        g_p = [5, 10, 15, 20, 50]
        model(X1, x1, y_p1, Y1, YD1, YD_e1, T1, C1, c_p1, G, g_p, r, V1, V_e1, B_d1, B_h1, B_s1, B_cb1, ΔB_h1, ΔB_s1, ΔB_cb1, H_d1, H_s1, H_h1, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B1, H_h_V1, t)
line1 = ax.plot(Time, H_h_V1, label = "財政支出拡大(第５期のみ)")

#第５期以降も第４財への財政支出を20から30に変更
for t in range(1,51):
    if t < 5:
        model(X2, x2, y_p2, Y2, YD2, YD_e2, T2, C2, c_p2, G, g_p, r, V2, V_e2, B_d2, B_h2, B_s2, B_cb2, ΔB_h2, ΔB_s2, ΔB_cb2, H_d2, H_s2, H_h2, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B2, H_h_V2, t)
    elif t == 5:
        G = 110
        g_p = [5, 10, 15, 30, 50]
        model(X2, x2, y_p2, Y2, YD2, YD_e2, T2, C2, c_p2, G, g_p, r, V2, V_e2, B_d2, B_h2, B_s2, B_cb2, ΔB_h2, ΔB_s2, ΔB_cb2, H_d2, H_s2, H_h2, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B2, H_h_V2, t)
    else:
        model(X2, x2, y_p2, Y2, YD2, YD_e2, T2, C2, c_p2, G, g_p, r, V2, V_e2, B_d2, B_h2, B_s2, B_cb2, ΔB_h2, ΔB_s2, ΔB_cb2, H_d2, H_s2, H_h2, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B2, H_h_V2, t)
line2 = ax.plot(Time, H_h_V2, label = "財政支出拡大(第５期以降)")

#パラメターを元の数値に戻す
G = 100
g_p = [5, 10, 15, 20, 50]

#第５期のみ税率を0.15から0.14に変更
for t in range(1,51):
    if t < 5:
        model(X3, x3, y_p3, Y3, YD3, YD_e3, T3, C3, c_p3, G, g_p, r, V3, V_e3, B_d3, B_h3, B_s3, B_cb3, ΔB_h3, ΔB_s3, ΔB_cb3, H_d3, H_s3, H_h3, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B3, H_h_V3, t)
    elif t == 5:
        θ = 0.14
        model(X3, x3, y_p3, Y3, YD3, YD_e3, T3, C3, c_p3, G, g_p, r, V3, V_e3, B_d3, B_h3, B_s3, B_cb3, ΔB_h3, ΔB_s3, ΔB_cb3, H_d3, H_s3, H_h3, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B3, H_h_V3, t)
    else:
        θ = 0.15
        model(X3, x3, y_p3, Y3, YD3, YD_e3, T3, C3, c_p3, G, g_p, r, V3, V_e3, B_d3, B_h3, B_s3, B_cb3, ΔB_h3, ΔB_s3, ΔB_cb3, H_d3, H_s3, H_h3, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B3, H_h_V3, t)
line3 = ax.plot(Time, H_h_V3, label = "減税(第５期のみ)")

#第５期以降も税率を0.15から0.14に変更
for t in range(1,51):
    if t < 5:
        model(X4, x4, y_p4, Y4, YD4, YD_e4, T4, C4, c_p4, G, g_p, r, V4, V_e4, B_d4, B_h4, B_s4, B_cb4, ΔB_h4, ΔB_s4, ΔB_cb4, H_d4, H_s4, H_h4, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B4, H_h_V4, t)
    elif t == 5:
        θ = 0.14
        model(X4, x4, y_p4, Y4, YD4, YD_e4, T4, C4, c_p4, G, g_p, r, V4, V_e4, B_d4, B_h4, B_s4, B_cb4, ΔB_h4, ΔB_s4, ΔB_cb4, H_d4, H_s4, H_h4, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B4, H_h_V4, t)
    else:
        model(X4, x4, y_p4, Y4, YD4, YD_e4, T4, C4, c_p4, G, g_p, r, V4, V_e4, B_d4, B_h4, B_s4, B_cb4, ΔB_h4, ΔB_s4, ΔB_cb4, H_d4, H_s4, H_h4, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B4, H_h_V4, t)
line4 = ax.plot(Time, H_h_V4, label = "減税(第５期以降)")

#パラメターを元の数値に戻す
θ = 0.15

#第５期のみ消費性向を0.75から0.80に変更
for t in range(1,51):
    if t < 5:
        model(X5, x5, y_p5, Y5, YD5, YD_e5, T5, C5, c_p5, G, g_p, r, V5, V_e5, B_d5, B_h5, B_s5, B_cb5, ΔB_h5, ΔB_s5, ΔB_cb5, H_d5, H_s5, H_h5, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B5, H_h_V5, t)
    elif t == 5:
        α_1 = 4/5
        model(X5, x5, y_p5, Y5, YD5, YD_e5, T5, C5, c_p5, G, g_p, r, V5, V_e5, B_d5, B_h5, B_s5, B_cb5, ΔB_h5, ΔB_s5, ΔB_cb5, H_d5, H_s5, H_h5, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B5, H_h_V5, t)
    else:
        α_1 = 3/4
        model(X5, x5, y_p5, Y5, YD5, YD_e5, T5, C5, c_p5, G, g_p, r, V5, V_e5, B_d5, B_h5, B_s5, B_cb5, ΔB_h5, ΔB_s5, ΔB_cb5, H_d5, H_s5, H_h5, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B5, H_h_V5, t)
line5 = ax.plot(Time, H_h_V5, label = "消費性向上昇(第５期のみ)")

#第５期以降も消費性向を0.75から0.80に変更
for t in range(1,51):
    if t < 5:
        model(X6, x6, y_p6, Y6, YD6, YD_e6, T6, C6, c_p6, G, g_p, r, V6, V_e6, B_d6, B_h6, B_s6, B_cb6, ΔB_h6, ΔB_s6, ΔB_cb6, H_d6, H_s6, H_h6, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B6, H_h_V6, t)
    elif t == 5:
        α_1 = 4/5
        model(X6, x6, y_p6, Y6, YD6, YD_e6, T6, C6, c_p6, G, g_p, r, V6, V_e6, B_d6, B_h6, B_s6, B_cb6, ΔB_h6, ΔB_s6, ΔB_cb6, H_d6, H_s6, H_h6, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B6, H_h_V6, t)
    else:
        model(X6, x6, y_p6, Y6, YD6, YD_e6, T6, C6, c_p6, G, g_p, r, V6, V_e6, B_d6, B_h6, B_s6, B_cb6, ΔB_h6, ΔB_s6, ΔB_cb6, H_d6, H_s6, H_h6, a, v, c, θ, α_1, α_2, λ_0, λ_1, λ_2, A, B6, H_h_V6, t)
line6 = ax.plot(Time, H_h_V6, label = "消費性向上昇(第５期以降)")

#パラメターを元の数値に戻す
α_1 = 3/4

ax.set_title("家計・貨幣保有割合")
ax.set_xlabel("期")
ax.set_ylabel("G\nD\nP", rotation=0, va='center')
ax.set_xlim(0,50)
ax.legend()
plt.grid()
plt.show()
