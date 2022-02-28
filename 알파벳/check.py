import pose as pm
import tensorflow as tf
import cv2
import mediapipe as mp
import time
import wx

app = wx.App(False)
width, height = wx.GetDisplaySize()
detector = pm.PoseDetector()
new_model = tf.keras.models.load_model('model21.h5')
alphabetlist = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
cam = cv2.VideoCapture(0)
S_W = int(width/2)
S_H = int(height)
time_list = [0]
what_explain_input = 1
explain_input = ''
image_upload_stop = 0
agg_img = 0
agg_real_img = 0

def pose_alphabet_check_main_def():
    global image_upload_stop, agg_img, agg_real_img
    cv2.namedWindow('Virtual Image')
    cv2.namedWindow('Real Image')
    if image_upload_stop == 0:
        check, img = cam.read()
        real_img = img.copy()
        img, p_landmarks, p_connections = detector.findPose(img.shape[0], img, False)
        mp.solutions.drawing_utils.draw_landmarks(real_img, p_landmarks, p_connections)
        lmList = detector.getPosition(img, False)
        if len(lmList) <= 0:
            img = cv2.resize(img, dsize=(S_W, S_H), interpolation=cv2.INTER_CUBIC)
            real_img = cv2.resize(real_img, dsize=(S_W, S_H), interpolation=cv2.INTER_CUBIC)
        else:
            img = detector.draw_pose(img, img.shape[1] if img.shape[1] > img.shape[0] else img.shape[0], lmList)
            gray = cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_AREA)
            gray = gray.copy()
            check = cv2.resize(gray, dsize=(28, 28), interpolation=cv2.INTER_AREA)
            check = check.reshape(1,28,28,3)
            data_result = new_model.predict(check[0:1])
            img = cv2.resize(img, dsize=(S_W,S_H), interpolation=cv2.INTER_CUBIC)
            real_img = cv2.resize(real_img, dsize=(S_W,S_H), interpolation=cv2.INTER_CUBIC)
            if what_explain_input == 0 and explain_input != '':
                AI_data = int(float(str(data_result[0][alphabetlist.index(explain_input)])[0:3])*10)
                cv2.putText(img, str(AI_data), (20, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                cv2.putText(real_img, str(AI_data), (20, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                cv2.putText(img, str(explain_input), (20, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                cv2.putText(real_img, str(explain_input), (20, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cTime = time.time()
        fps = 1 / (cTime - time_list[0]) if (cTime - time_list[0]) != 0 else 1
        time_list[0] = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.putText(real_img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        if what_explain_input == 1:
            print("Please Input Alphabet")
            cv2.putText(img, "Please Input Alphabet", (int(S_H/8), int(S_W/2)), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0),3)
            cv2.putText(real_img, "Please Input Alphabet", (int(S_H / 8), int(S_W / 2)), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            print(S_W, S_H)
        agg_img = img
        agg_real_img = real_img

    cv2.imshow("Virtual Image", agg_img)
    cv2.imshow("Real Image", agg_real_img)