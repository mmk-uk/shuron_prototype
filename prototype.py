#画面の幅と高さを設定
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'resizable', False) 

#アプリ用ライブラリ
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty

#画像表示用
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock

#MediaPipe
import mediapipe as mp
#import prototype_module
from prototype_module import joint_angle
from prototype_module import select_kaden_judge1
from prototype_module import select_kaden_judge2
from prototype_module import draw_landmarks
from prototype_module import eyes_keypoint
from prototype_module import dominant_arm_shoulder
from prototype_module import dominant_arm_elbow
from prototype_module import dominant_arm_tip
from prototype_module import dominant_arm_waist

#その他ライブラリ
import cv2
import numpy as np
import copy
import uuid



class Display(BoxLayout):
    pass
 
#画面１：カメラ位置設定
class Camera_Position(Screen):
    #count = 0
    def __init__(self, **kwargs):
        super(Camera_Position, self).__init__(**kwargs)
        self.play()
    
    def play(self):
        global stepStatus
        if stepStatus == 1:
            self.capture = cv2.VideoCapture(1)
            Clock.schedule_interval(self.update, 1.0 / 30)
        else:
            Clock.unschedule(self.update)
            self.capture.release()


        # インターバルで実行する描画メソッド
    def update(self, dt):
        # フレームを読み込み
        ret, self.frame = self.capture.read()
        #print(self.frame.shape[1],self.frame.shape[0]) #->1280 720
        # Kivy Textureに変換
        buf = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr') 
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # インスタンスのtextureを変更
        camera = self.ids['camera_preview']
        camera.texture = texture
        #self.count = self.count + 1
        #print(self.count)
    

    def nextStep(self):
        global stepStatus
        stepStatus += 1
        #self.capture.release()
    
#画面２：家電位置の設定
class Config_Device(Screen):
    rv = ObjectProperty()
    capture_img = np.zeros((1280,720), np.uint8)

    def __init__(self, **kwargs):
        super(Config_Device, self).__init__(**kwargs)

    def play(self):
        global stepStatus
        if stepStatus == 2:
            self.capture = cv2.VideoCapture(1)
            ret, self.frame = self.capture.read()
            self.capture_img = self.frame
            Clock.schedule_interval(self.update, 1.0 / 30)

        else:
            Clock.unschedule(self.update)
            self.capture.release()

    def update(self, dt):
        show_img = self.capture_img.copy()
        global start_x,start_y,end_x,end_y,clickFlag,colors
        #print(start_x,start_y,end_x,end_y,clickFlag)
        if clickFlag == 2 and len(kaden_list) < kaden_limit_n:
            show_img = cv2.rectangle(show_img, (start_x, start_y), (end_x, end_y), colors[len(kaden_list)], 3)
            
        buf = cv2.flip(show_img, 0).tostring()
        texture = Texture.create(size=(show_img.shape[1], show_img.shape[0]), colorfmt='bgr') 
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        camera = self.ids['image1']
        camera.texture = texture
    
    #家電の追加
    def add(self):
        #print(self.ids.kaden_name.text)
        global start_x,start_y,end_x,end_y,clickFlag,kaden_list,colors,kaden_limit_n
        if end_x < start_x :
            tmp_x = start_x
            start_x = end_x
            end_x = tmp_x
        
        if end_y < start_y :
            tmp_y = start_y
            start_y = end_y
            end_y = tmp_y

        if clickFlag == 2 and len(self.ids.kaden_name.text) != 0 and len(kaden_list) < kaden_limit_n:
            kaden_area = {"start_x":start_x,"start_y":start_y,"end_x":end_x,"end_y":end_y}
            show_image = self.capture_img.copy()
            kaden_image = show_image[start_y:end_y,start_x:end_x,]
            kaden_info = {"id":str(uuid.uuid4()),"name":self.ids.kaden_name.text,"area":kaden_area,"image":kaden_image}
            kaden_list.append(kaden_info)

            #kaden_image = cv2.rectangle(kaden_image,(0,0),(kaden_image.shape[1],kaden_image.shape[0]),colors[len(kaden_list)-1],4)
            kaden_image = cv2.copyMakeBorder(kaden_image,5,5,5,5,cv2.BORDER_CONSTANT,value=colors[len(kaden_list)-1])

            buf = cv2.flip(kaden_image, 0).tostring()
            texture = Texture.create(size=(kaden_image.shape[1], kaden_image.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.rv.data.append({'id':kaden_info["id"],'name':self.ids.kaden_name.text,'image':texture})

            clickFlag = 0
            self.ids.kaden_name.text = ""


    def nextStep(self):
        global stepStatus,kaden_list
        if len(kaden_list) > 0:
            stepStatus += 1
            return True
        else:
            return False

    def backStep(self):
        global stepStatus,start_x,start_y,end_x,end_y,clickFlag,kaden_list
        start_x,start_y,end_x,end_y = 0,0,0,0
        clickFlag = 0
        kaden_list.clear()
        self.rv.data = []
        self.ids.kaden_name.text = ""
        stepStatus -= 1
    
    def dominant_hand_check(self,hand):
        global dominant_hand_flag

        if self.ids.left_hand.state == 'normal' and self.ids.right_hand.state == 'normal':
            if hand == '左利き':
                self.ids.right_hand.state = 'down'
            else:
                self.ids.left_hand.state = 'down'

        if self.ids.left_hand.state == 'down':
            #左利き
            dominant_hand_flag = 1

        if self.ids.right_hand.state == 'down':
            #右利き
            dominant_hand_flag = 0

class Camera_View(Image):
    def on_image1_down(self, touch):
        if self.collide_point(*touch.pos): #自身にタッチしたか
            print(touch.pos[0],touch.pos[1]-270)
            global start_x,start_y,clickFlag
            start_x = int(touch.pos[0])
            start_y = int(720-(touch.pos[1]-270))
            clickFlag = 1

    def on_image1_up(self, touch):
        if self.collide_point(*touch.pos): #自身にタッチしたか
            #print(touch.pos[0],touch.pos[1]-270)
            global end_x,end_y,clickFlag
            end_x = int(touch.pos[0])
            end_y = int(720-(touch.pos[1]-270))
            clickFlag = 2

class Selected_Kaden(BoxLayout):
    id = StringProperty()
    name = StringProperty()
    image = ObjectProperty(None)  

    def deleteKaden(self):
        global kaden_list,colors
        rv = self.parent.parent.parent.parent.parent.parent.rv
        kaden_list = [kaden for kaden in kaden_list if kaden["id"] != self.id]
        rv.data = [kaden for kaden in rv.data if kaden["id"] != self.id]

        for i,kaden in enumerate(kaden_list):
            kaden_image = cv2.copyMakeBorder(kaden["image"],5,5,5,5,cv2.BORDER_CONSTANT,value=colors[i])
            buf = cv2.flip(kaden_image, 0).tostring()   
            texture = Texture.create(size=(kaden_image.shape[1], kaden_image.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            rv.data[i]['image'] = texture


#画面３：家電の操作
class Control_Device(Screen):
    selected_kaden_name = StringProperty()
    kaden_judge_s = StringProperty()

    def __init__(self, **kwargs):
        super(Control_Device, self).__init__(**kwargs)
        
        #モデルロード
        mp_pose = mp.solutions.pose #モデルの選択
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
    def play(self):
        global stepStatus
        if stepStatus == 3:            
            self.capture = cv2.VideoCapture(1)
            ret, self.frame = self.capture.read()
            self.capture_img = self.frame
            Clock.schedule_interval(self.update, 1.0 / 30)

            self.selected_kaden_name = ""
            self.kaden_judge_s = "選択されていません。"
            tmp_img = np.full((300, 300, 3), (204,204,204), dtype=np.uint8)
            buf = cv2.flip(tmp_img, 0).tostring()
            texture = Texture.create(size=(tmp_img.shape[1], tmp_img.shape[0]), colorfmt='bgr') 
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            camera = self.ids['select_kaden_image']
            camera.texture = texture

        else:
            Clock.unschedule(self.update)
            self.capture.release()
    
    def update(self, dt):
        global kaden_list,dominant_hand_flag
        ret, show_img = self.capture.read()

        #家電位置の描画
        for i,kaden in enumerate(kaden_list):
            show_img = cv2.rectangle(show_img, (kaden["area"]["start_x"],kaden["area"]["start_y"]), (kaden["area"]["end_x"], kaden["area"]["end_y"]), colors[i], 3)
        
        #姿勢推定処理
        show_img.flags.writeable = False
        show_img = cv2.cvtColor(show_img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(show_img)

        #キーポイントリスト作成
        landmark_point = []
        if results.pose_landmarks is not None:
            for index, landmark in enumerate(results.pose_landmarks.landmark):
                landmark_x = min(int(landmark.x * show_img.shape[1]), show_img.shape[1] - 1)
                landmark_y = min(int(landmark.y * show_img.shape[0]), show_img.shape[0] - 1)
                landmark_point.append([landmark.visibility, (landmark_x, landmark_y)])
        
        #姿勢の描画
        if results.pose_landmarks is not None:
            #print(type(self.frame))
            show_img = draw_landmarks(show_img, landmark_point)

        #家電選択の計算
        visibility_th = 0.5
        self.selected_kaden_name = ""
        self.kaden_judge_s = "選択されていません。"
        tmp_img = np.full((300, 300, 3), (204,204,204), dtype=np.uint8)
        select_kaden = {"not_select":True,"name":"","image":tmp_img,"diff":180}
        if len(landmark_point) > 0:
            #if landmark_point[12][0] > visibility_th and landmark_point[14][0] > visibility_th and landmark_point[16][0] > visibility_th:
                #右腕の曲がり角度
                arm_angle = joint_angle(dominant_arm_shoulder(landmark_point,dominant_hand_flag),dominant_arm_elbow(landmark_point,dominant_hand_flag),dominant_arm_tip(landmark_point,dominant_hand_flag))
                if arm_angle > 120:
                    #cv2.line(show_img, eyes_keypoint(landmark_point[2][1],landmark_point[5][1]), landmark_point[16][1],(255, 0, 0), 6)
                    cv2.line(show_img, eyes_keypoint(dominant_arm_shoulder(landmark_point,dominant_hand_flag),dominant_arm_waist(landmark_point,dominant_hand_flag)), dominant_arm_tip(landmark_point,dominant_hand_flag),(255, 0, 0), 6)
                    for kaden in kaden_list:
                        #家電選択の判定
                        judge = select_kaden_judge1(dominant_arm_shoulder(landmark_point,dominant_hand_flag),dominant_arm_waist(landmark_point,dominant_hand_flag),dominant_arm_tip(landmark_point,dominant_hand_flag),(kaden["area"]["start_x"],kaden["area"]["start_y"]),(kaden["area"]["end_x"], kaden["area"]["end_y"]))
                        if judge:
                            diff = select_kaden_judge2(dominant_arm_shoulder(landmark_point,dominant_hand_flag),dominant_arm_waist(landmark_point,dominant_hand_flag),dominant_arm_tip(landmark_point,dominant_hand_flag),(kaden["area"]["start_x"],kaden["area"]["start_y"]),(kaden["area"]["end_x"], kaden["area"]["end_y"]))
                            if diff < select_kaden["diff"]:
                                select_kaden["not_select"] = False
                                self.selected_kaden_name = kaden["name"]
                                self.kaden_judge_s = "が選択されています。"
                                select_kaden["image"] = cv2.resize(kaden["image"],dsize=(round(kaden["image"].shape[1]*(300/kaden["image"].shape[0])),300))
                            

                    #if select_kaden["not_select"]:
                    #   self.selected_kaden_name = ""
                    #   self.kaden_judge_s = "選択されていません。"


        buf1 = cv2.flip(select_kaden["image"], 0).tostring()
        texture1 = Texture.create(size=(select_kaden["image"].shape[1], select_kaden["image"].shape[0]), colorfmt='bgr') 
        texture1.blit_buffer(buf1, colorfmt='bgr', bufferfmt='ubyte')
        camera1 = self.ids['select_kaden_image']
        camera1.texture = texture1

        buf2 = cv2.flip(show_img, 0).tostring()
        texture2 = Texture.create(size=(show_img.shape[1], show_img.shape[0]), colorfmt='rgb') 
        texture2.blit_buffer(buf2, colorfmt='rgb', bufferfmt='ubyte')
        camera2 = self.ids['image2']
        camera2.texture = texture2

    def backStep(self):
        global stepStatus,start_x,start_y,end_x,end_y,clickFlag
        start_x,start_y,end_x,end_y = 0,0,0,0
        clickFlag = 0
        stepStatus -= 1

class PrototypeApp(App):
    def build(self):
        return Display()

stepStatus = 1
start_x,start_y = 0,0
end_x,end_y = 0,0
clickFlag = 0
kaden_list = []
kaden_limit_n = 6
dominant_hand_flag = 0 #0:右,1:左
colors = [(0,215,255),(255,144,30),(0,102,225),(34,139,34),(204,102,255),(51,102,153)]

if __name__ == '__main__':
    PrototypeApp().run()