#画面の幅と高さを設定
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

#画像表示用
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2



class Display(BoxLayout):
    pass
 
class Camera_Position(Screen):
    pass

class CameraPreview(Image):
    count = 0
    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)
        # 0番目のカメラに接続
        self.capture = cv2.VideoCapture(1)
        # 描画のインターバルを設定
        Clock.schedule_interval(self.update, 1.0 / 30)

    # インターバルで実行する描画メソッド
    def update(self, dt):
        # フレームを読み込み
        ret, self.frame = self.capture.read()
        # Kivy Textureに変換
        buf = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr') 
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # インスタンスのtextureを変更
        self.texture = texture
        self.count = self.count + 1
        print(self.count)
 
class Config_Device(Screen):
    pass

class CameraViewImage(Image):
    def __init__(self, **kwargs):
        super(CameraViewImage, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(1)
    
    def shot(self):
        ret, self.frame = self.capture.read()
        buf = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr') 
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture
 
class PrototypeApp(App):
    def build(self):
        return Display()
 
if __name__ == '__main__':
    PrototypeApp().run()