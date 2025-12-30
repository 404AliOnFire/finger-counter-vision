import cv2 as cv
import mediapipe as mp


class HandDetector:
    def __init__(self,hands=1,min_detection = 0.5, min_tracking = 0.5):
        self.mpHands = mp.solutions.hands
        self.hands_num = hands
        self.detection = min_detection
        self.tracking = min_tracking
        self.hands = self.mpHands.Hands(max_num_hands=self.hands_num,
                                       min_detection_confidence=self.detection,
                                       min_tracking_confidence=self.tracking)

        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        hands_result = self.hands.process(img_rgb)

        self.landmarks = hands_result.multi_hand_landmarks
        if self.landmarks and draw:
            for lm in self.landmarks:
                self.mpDraw.draw_landmarks(img,lm,self.mpHands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, hand_no = 0, draw=True):
        lm_dic = {}
        if not self.landmarks:
            return lm_dic

        if hand_no < 0 or hand_no > len(self.landmarks):
            print("Hand No is out of range (0,20)")
            return lm_list

        if self.landmarks:
            position = self.landmarks[hand_no]

            for id,lm in enumerate(position.landmark):
                cx = int(lm.x * img.shape[1])
                cy = int(lm.y * img.shape[0])

                if draw:
                    cv.circle(img,(cx,cy),5,(255,0,255),cv.FILLED)

                lm_dic[id] = (cx,cy)

        return lm_dic

