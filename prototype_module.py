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
    cos = 1 if cos > 1 else -1 if cos < -1 else cos

    #アークコサインで角度を求める
    deg = math.degrees(math.acos(cos))
    #少数を整数に
    return int((deg * 2 + 1) // 2)

#腕の角度と家電の位置から選択家電を決定する関数
def select_kaden_judge1(A,AA,B,X,Y):

    #目辺りの基準
    eyes = eyes_keypoint(A,AA)

    #目辺りを基準にベクトル
    v = (B[0]-eyes[0],B[1]-eyes[1])
    x = (X[0]-eyes[0],Y[1]-eyes[1])
    y = (Y[0]-eyes[0],X[1]-eyes[1])
    w = (X[0]-eyes[0],X[1]-eyes[1])
    z = (Y[0]-eyes[0],Y[1]-eyes[1])

    #角度を求める
    v_t = -(math.degrees(np.arctan2(v[1],v[0])))
    x_t = -(math.degrees(np.arctan2(x[1],x[0])))
    y_t = -(math.degrees(np.arctan2(y[1],y[0])))
    w_t = -(math.degrees(np.arctan2(w[1],w[0])))
    z_t = -(math.degrees(np.arctan2(z[1],z[0])))

    #小さい順、大きい順に並べ替え
    min_angles = sorted([x_t,y_t,w_t,z_t])
    max_angles = sorted([x_t,y_t,w_t,z_t],reverse=True)

    #print(v_t,min_angles[0],max_angles[0])

    if (max_angles[0] - min_angles[0]) < 180:
        if min_angles[0] < v_t and v_t < max_angles[0]:
            return True
        else:
            return False
    else:
        if (-180 < v_t and v_t < min_angles[1]) or (max_angles[1] < v_t and v_t < 180):
            return True
        else:
            return False

#腕の角度と家電の位置の中心への方向との差を調べる関数
def select_kaden_judge2(A,AA,B,X,Y):
    #目辺りの基準
    eyes = eyes_keypoint(A,AA)
    #家電の中心
    center = ((X[0]+Y[0])/2,(X[1]+Y[1])/2)
    #目辺りを基準にベクトル
    v = (B[0]-eyes[0],B[1]-eyes[1])
    c = (center[0]-eyes[0],center[1]-eyes[1])
    #角度を求める
    v_t = math.degrees(np.arctan2(v[0],v[1]))
    c_t = math.degrees(np.arctan2(c[0],c[1]))
    #角度の差を求める
    diff = abs(v_t-c_t)
    return diff



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

def eyes_keypoint(A,B):
    #eyes = ((B[0]+A[0])//2,(B[1]+A[1])//2)
    up_dis = abs(A[1]-B[1])//3
    eyes = (A[0],A[1]-up_dis)
    return eyes

def dominant_arm_shoulder(landmark_point,dominant_hand_flag):
    if dominant_hand_flag == 1:
        return landmark_point[11][1]
    else:
        return landmark_point[12][1]

def dominant_arm_elbow(landmark_point,dominant_hand_flag):
    if dominant_hand_flag == 1:
        return landmark_point[13][1]
    else:
        return landmark_point[14][1]

def dominant_arm_tip(landmark_point,dominant_hand_flag):
    if dominant_hand_flag == 1:
        return landmark_point[19][1]
    else:
        return landmark_point[20][1]

def dominant_arm_waist(landmark_point,dominant_hand_flag):
    if dominant_hand_flag == 1:
        return landmark_point[23][1]
    else:
        return landmark_point[24][1]