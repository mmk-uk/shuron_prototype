import cv2
import numpy as np
import math

#３点からなる角度を求める関数
def joint_angle(A,B,C):
    #中点を基準に２点を決定
    a = (A[0]-B[0],A[1]-B[1])
    b = (C[0]-B[0],C[1]-B[1])
    #2点からコサインを求める
    cos = (a[0]*b[0]+a[1]*b[1])/(math.sqrt(a[0]*a[0]+a[1]*a[1])*math.sqrt(b[0]*b[0]+b[1]*b[1]))
    #アークコサインで角度を求める
    deg = math.degrees(math.acos(cos))
    #少数を整数に
    return int((deg * 2 + 1) // 2)

#腕の角度と家電の位置から選択家電を決定する関数
def select_kaden_judge(A,B,X,Y):
    #A(右肩)を基準にベクトル
    v = (B[0]-A[0],B[1]-A[1])
    x = (X[0]-A[0],Y[1]-A[1])
    y = (Y[0]-A[0],X[1]-A[1])

    #角度を求める
    v_t = v[1]/v[0]
    x_t = x[1]/x[0]
    y_t = y[1]/y[0]

    #角度を比較
    if x_t > y_t:
        if y_t < v_t and v_t < x_t:
            return True
        else:
            return False
    else:
        if x_t < v_t and v_t < y_t:
            return True
        else:
            return False

#骨格を描画する関数
def draw_landmarks(image, landmark_point, visibility_th=0.5):

    if len(landmark_point) > 0:
        # 右目
        if landmark_point[1][0] > visibility_th and landmark_point[2][0] > visibility_th:
            cv2.line(image, landmark_point[1][1], landmark_point[2][1],(0, 255, 255), 3)
        if landmark_point[2][0] > visibility_th and landmark_point[3][0] > visibility_th:
            cv2.line(image, landmark_point[2][1], landmark_point[3][1],(0, 255, 255), 3)

        # 左目
        if landmark_point[4][0] > visibility_th and landmark_point[5][0] > visibility_th:
            cv2.line(image, landmark_point[4][1], landmark_point[5][1],(0, 255, 255), 3)
        if landmark_point[5][0] > visibility_th and landmark_point[6][0] > visibility_th:
            cv2.line(image, landmark_point[5][1], landmark_point[6][1],(0, 255, 255), 3)

        # 口
        if landmark_point[9][0] > visibility_th and landmark_point[10][0] > visibility_th:
            cv2.line(image, landmark_point[9][1], landmark_point[10][1],(0, 255, 255), 3)

        # 肩
        if landmark_point[11][0] > visibility_th and landmark_point[12][0] > visibility_th:
            cv2.line(image, landmark_point[11][1], landmark_point[12][1],(0, 255, 255), 3)

        # 右腕
        if landmark_point[11][0] > visibility_th and landmark_point[13][0] > visibility_th:
            cv2.line(image, landmark_point[11][1], landmark_point[13][1],(0, 255, 255), 3)
        if landmark_point[13][0] > visibility_th and landmark_point[15][0] > visibility_th:
            cv2.line(image, landmark_point[13][1], landmark_point[15][1],(0, 255, 255), 3)

        # 左腕
        if landmark_point[12][0] > visibility_th and landmark_point[14][0] > visibility_th:
            cv2.line(image, landmark_point[12][1], landmark_point[14][1],(0, 255, 255), 3)
        if landmark_point[14][0] > visibility_th and landmark_point[16][0] > visibility_th:
            cv2.line(image, landmark_point[14][1], landmark_point[16][1],(0, 255, 255), 3)

        # 右手
        if landmark_point[15][0] > visibility_th and landmark_point[17][0] > visibility_th:
            cv2.line(image, landmark_point[15][1], landmark_point[17][1],(0, 255, 255), 3)
        if landmark_point[17][0] > visibility_th and landmark_point[19][0] > visibility_th:
            cv2.line(image, landmark_point[17][1], landmark_point[19][1],(0, 255, 255), 3)
        if landmark_point[19][0] > visibility_th and landmark_point[21][0] > visibility_th:
            cv2.line(image, landmark_point[19][1], landmark_point[21][1],(0, 255, 255), 3)
        if landmark_point[21][0] > visibility_th and landmark_point[15][0] > visibility_th:
            cv2.line(image, landmark_point[21][1], landmark_point[15][1],(0, 255, 255), 3)

        # 左手
        if landmark_point[16][0] > visibility_th and landmark_point[18][0] > visibility_th:
            cv2.line(image, landmark_point[16][1], landmark_point[18][1],(0, 255, 255), 3)
        if landmark_point[18][0] > visibility_th and landmark_point[20][0] > visibility_th:
            cv2.line(image, landmark_point[18][1], landmark_point[20][1],(0, 255, 255), 3)
        if landmark_point[20][0] > visibility_th and landmark_point[22][0] > visibility_th:
            cv2.line(image, landmark_point[20][1], landmark_point[22][1],(0, 255, 255), 3)
        if landmark_point[22][0] > visibility_th and landmark_point[16][0] > visibility_th:
            cv2.line(image, landmark_point[22][1], landmark_point[16][1],(0, 255, 255), 3)

        # 胴体
        if landmark_point[11][0] > visibility_th and landmark_point[23][0] > visibility_th:
            cv2.line(image, landmark_point[11][1], landmark_point[23][1],(0, 255, 255), 3)
        if landmark_point[12][0] > visibility_th and landmark_point[24][0] > visibility_th:
            cv2.line(image, landmark_point[12][1], landmark_point[24][1],(0, 255, 255), 3)
        if landmark_point[23][0] > visibility_th and landmark_point[24][0] > visibility_th:
            cv2.line(image, landmark_point[23][1], landmark_point[24][1],(0, 255, 255), 3)

        if len(landmark_point) > 25:
            # 右足
            if landmark_point[23][0] > visibility_th and landmark_point[25][0] > visibility_th:
                cv2.line(image, landmark_point[23][1], landmark_point[25][1],(0, 255, 255), 3)
            if landmark_point[25][0] > visibility_th and landmark_point[27][0] > visibility_th:
                cv2.line(image, landmark_point[25][1], landmark_point[27][1],(0, 255, 255), 3)
            if landmark_point[27][0] > visibility_th and landmark_point[29][0] > visibility_th:
                cv2.line(image, landmark_point[27][1], landmark_point[29][1],(0, 255, 255), 3)
            if landmark_point[29][0] > visibility_th and landmark_point[31][0] > visibility_th:
                cv2.line(image, landmark_point[29][1], landmark_point[31][1],(0, 255, 255), 3)

            # 左足
            if landmark_point[24][0] > visibility_th and landmark_point[26][0] > visibility_th:
                cv2.line(image, landmark_point[24][1], landmark_point[26][1],(0, 255, 255), 3)
            if landmark_point[26][0] > visibility_th and landmark_point[28][0] > visibility_th:
                cv2.line(image, landmark_point[26][1], landmark_point[28][1],(0, 255, 255), 3)
            if landmark_point[28][0] > visibility_th and landmark_point[30][0] > visibility_th:
                cv2.line(image, landmark_point[28][1], landmark_point[30][1],(0, 255, 255), 3)
            if landmark_point[30][0] > visibility_th and landmark_point[32][0] > visibility_th:
                cv2.line(image, landmark_point[30][1], landmark_point[32][1],(0, 255, 255), 3)
    return image