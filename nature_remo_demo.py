from remo import NatureRemoAPI

#アクセストークンを発行しておく
access_token = 'w1cS-wzj1gltKA8Rs5lRS7wx5M-jabqPlUFAN_R0YHY.47HQh0RDT72Sh75UWiyIXShKHKdqKj3Z9pCREBnGtGQ'

#初期化
api = NatureRemoAPI(access_token)

#デバイス情報
#devices = api.get_devices()

#接続された家電の情報
appliances = api.get_appliances()

#for app in appliances:
#print(app)

light_on = 'ce40d4e6-35e8-4613-87b7-a46add6783ee'
light_off = '9bae11d5-ae94-4115-8037-b3312d292e01'

api.send_signal(light_off)