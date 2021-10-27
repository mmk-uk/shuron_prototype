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

#その他ライブラリ
import cv2
import numpy as np
import copy
import uuid



class Display(BoxLayout):
    pass
 
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
        if clickFlag == 2:
            show_img = cv2.rectangle(show_img, (start_x, start_y), (end_x, end_y), colors[len(kaden_list)], 3)
            
        buf = cv2.flip(show_img, 0).tostring()
        texture = Texture.create(size=(show_img.shape[1], show_img.shape[0]), colorfmt='bgr') 
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        camera = self.ids['image1']
        camera.texture = texture
    
    def add(self):
        #print(self.ids.kaden_name.text)
        global start_x,start_y,end_x,end_y,clickFlag,kaden_list,colors
        if end_x < start_x :
            tmp_x = start_x
            start_x = end_x
            end_x = tmp_x
        
        if end_y < start_y :
            tmp_y = start_y
            start_y = end_y
            end_y = tmp_y

        if clickFlag == 2 and len(self.ids.kaden_name.text) != 0:
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
        global stepStatus
        stepStatus += 1

    def backStep(self):
        global stepStatus,start_x,start_y,end_x,end_y,clickFlag,kaden_list
        start_x,start_y,end_x,end_y = 0,0,0,0
        clickFlag = 0
        kaden_list.clear()
        self.rv.data = []
        self.ids.kaden_name.text = ""
        stepStatus -= 1
    

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


class Control_Device(Screen):
    def __init__(self, **kwargs):
        super(Control_Device, self).__init__(**kwargs)

    def play(self):
        global stepStatus
        if stepStatus == 3:
            self.capture = cv2.VideoCapture(1)
            ret, self.frame = self.capture.read()
            self.capture_img = self.frame
            Clock.schedule_interval(self.update, 1.0 / 30)

        else:
            Clock.unschedule(self.update)
            self.capture.release()
    
    def update(self, dt):
        ret, self.frame = self.capture.read()

        buf = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr') 
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        camera = self.ids['image2']
        camera.texture = texture
    
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
colors = [(0,0,255),(0,255,0),(255,0,0),(255,255,0),(255,0,255),(0,255,255)]

if __name__ == '__main__':
    PrototypeApp().run()