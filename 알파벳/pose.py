import cv2
import mediapipe as mp
import time
import numpy as np


class PoseDetector:
    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode = self.mode,
                                     model_complexity=self.upBody,
                                     smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)

    def findPose(self, s, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        img = np.zeros((s, s, 3), dtype=np.uint8) + 255
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS

    def getPosition(self, img, draw=True):
        lmList= []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    if (((id >= 1 and id <= 10) == False) and (id != 17 and id != 18 and id != 21 and id != 22 and id != 31 and id != 32)):
                        cv2.circle(img, (cx, cy), 5, (0, 0, 0), cv2.FILLED)
        return lmList

    def draw_pose(self, img, s, lmList):
        for i in range(int(len(lmList))-6):
            if i != 22 and i != 21:
                img = cv2.line(img, (lmList[i][1], lmList[i][2]), (lmList[i+2][1], lmList[i+2][2]), (0, 0, 0), int((s/800)*50))
        img = cv2.line(img, (lmList[11][1], lmList[11][2]), (lmList[23][1], lmList[23][2]), (0, 0, 0), int((s/800)*50))
        img = cv2.line(img, (lmList[12][1], lmList[12][2]), (lmList[24][1], lmList[24][2]), (0, 0, 0), int((s/800)*50))

        img = cv2.line(img, (lmList[11][1], lmList[11][2]), (lmList[12][1], lmList[12][2]), (0, 0, 0), int((s/800)*50))
        img = cv2.line(img, (lmList[23][1], lmList[23][2]), (lmList[24][1], lmList[24][2]), (0, 0, 0), int((s/800)*50))
        return img