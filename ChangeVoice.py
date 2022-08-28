import cv2
import mediapipe as mp
import math

#win10弹出通知库 https://blog.csdn.net/yueyue200830/article/details/104270913
from win10toast import ToastNotifier
toaster = ToastNotifier()

#打开网页 https://www.jianshu.com/p/d4eea5b503ed
import webbrowser

#时间模块
import time

#https://blog.csdn.net/weixin_45930948/article/details/115444916

#此处至line17为windows音量控制
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#手势识别是否开始
started = True

def vector_2d_angle(v1,v2):
    '''
        求解二维向量的角度
    '''
    v1_x=v1[0]
    v1_y=v1[1]
    v2_x=v2[0]
    v2_y=v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ =65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_
def hand_angle(hand_):
    '''
        获取对应手相关向量的二维角度,根据角度确定手势
    '''
    angle_list = []
    #---------------------------- thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    #---------------------------- index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    #---------------------------- middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    #---------------------------- ring 无名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    #---------------------------- pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

def h_gesture(angle_list):
    '''
        # 二维约束的方法定义手势
        # fist five gun love one six three thumbup yeah
    '''
    global started
    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = None
    if 65535. not in angle_list:
        # 手势识别是否开始
        if (angle_list[0]<thr_angle_thumb) and (angle_list[1]>thr_angle) and (angle_list[2]<thr_angle) and (angle_list[3]<thr_angle) and (angle_list[4]<thr_angle):
            gesture_str = "Start"
            started = True
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle_s) and (angle_list[2] > thr_angle) and (angle_list[3] > thr_angle) and (angle_list[4] < thr_angle):
            gesture_str = "Stop"
            started = False

        if(started):
            #识别手势
            if (angle_list[0]>thr_angle_thumb) and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "Set Voice:0"
                volume.SetMasterVolumeLevel(-63.5, None)
            elif (angle_list[0]>thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "Set Voice:20"
                volume.SetMasterVolumeLevel(-23.558979034423828, None)
            elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "Set Voice:40"
                volume.SetMasterVolumeLevel(-13.582191467285156, None)
            elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]>thr_angle):
                gesture_str = "Set Voice:60"
                volume.SetMasterVolumeLevel(-7.610085964202881, None)
            elif (angle_list[0]>thr_angle_s) and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]<thr_angle_s):
                gesture_str = "Set Voice:80"
                volume.SetMasterVolumeLevel(-3.333683490753174, None)
            elif (angle_list[0]<thr_angle_s) and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]<thr_angle_s):
                gesture_str = "Set Voice:100"
                volume.SetMasterVolumeLevel(0, None)
            elif (angle_list[0]>thr_angle_s)  and (angle_list[1]>thr_angle_s) and (angle_list[2]<thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "NM$L"
                toaster.show_toast("此电脑","？",icon_path="./mediapipe/this pc.ico",duration=2,threaded=True)
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
                gesture_str = "66"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle) and (angle_list[2]<thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
                gesture_str = "Good Choice"
                webbrowser.open("https://tieba.baidu.com/f?kw=%E5%AD%99%E7%AC%91%E5%B7%9D&fr=index&fp=0&ie=utf-8", new=2, autoraise=True)
                time.sleep(3)
    return gesture_str

def detect():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75)
    cap = cv2.VideoCapture(0)

    while True:
        ret,frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame= cv2.flip(frame,1)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                hand_local = []
                for i in range(21):
                    x = hand_landmarks.landmark[i].x*frame.shape[1]
                    y = hand_landmarks.landmark[i].y*frame.shape[0]
                    hand_local.append((x,y))
                if hand_local:
                    angle_list = hand_angle(hand_local)
                    gesture_str = h_gesture(angle_list)
                    cv2.putText(frame,gesture_str,(0,100),0,1.3,(0,0,255),3)
        cv2.imshow('MediaPipe Hands', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()

if __name__ == '__main__':
    print("张开五指，弯曲食指以开始识别")
    print("--------------------------------")
    print("使用手势数字1-5控制音量")
    print("--------------------------------")
    print("使用手势数字6暂停识别")
    print("--------------------------------")
    print("为确保识别精确请尽量手心朝向摄像头")
    detect()