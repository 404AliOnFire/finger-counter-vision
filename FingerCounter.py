import time
import cv2 as cv
import os
import threading
import queue
from HandDetector import HandDetector

class FingerCounter:
    URL = 'http://192.168.1.2:4747/video'
    PATH = os.getcwd()

    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.capture_queue = queue.Queue(maxsize=1)
        self.display_queue = queue.Queue(maxsize=1)
        self.exit_flag = False
        self.hand_detector = HandDetector(min_detection=self.min_detection_confidence,
                                          min_tracking=self.min_tracking_confidence)
        self.photos_list = self.get_photos()

    def get_photos(self):
        absolute_path = os.path.join(self.PATH, "Pictures")
        list_photos = os.listdir(absolute_path)
        list_photos = [os.path.join(absolute_path, x) for x in list_photos]
        return list_photos

# ------------------ Thread Classes ------------------

class CaptureThread(threading.Thread):
    def __init__(self, finger_counter):
        super().__init__()
        self.fg = finger_counter

    def run(self):
        cap = cv.VideoCapture(self.fg.URL)
        cap.set(cv.CAP_PROP_BUFFERSIZE, 1)
        while not self.fg.exit_flag:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                continue
            if self.fg.capture_queue.full():
                _ = self.fg.capture_queue.get()
            self.fg.capture_queue.put(frame)
            time.sleep(0.005)
        cap.release()

class ProcessThread(threading.Thread):
    def __init__(self, finger_counter):
        super().__init__()
        self.fg = finger_counter
        self.points_list = [4, 8, 12, 16, 20]

    def run(self):
        while not self.fg.exit_flag:
            if self.fg.capture_queue.empty():
                time.sleep(0.01)
                continue
            frame = self.fg.capture_queue.get()
            frame = self.fg.hand_detector.find_hands(frame)
            lms = self.fg.hand_detector.find_position(frame)

            counter_list = [0, 0, 0, 0, 0]

            if len(lms) != 0:
                if lms[self.points_list[0]][0] > lms[self.points_list[1]][0]:
                    counter_list[0] = 1
                for i in range(1, 5):
                    if lms[self.points_list[i]][1] < lms[self.points_list[i]-2][1]:
                        counter_list[i] = 1

            number = counter_list.count(1)
            if 0 <= number <= len(self.fg.photos_list):
                photo = cv.imread(self.fg.photos_list[number-1])
                if photo is not None:
                    photo = cv.resize(photo, (300, 400))
                    photo = cv.flip(photo, 0)
                    frame[0:400, 0:300] = photo

            frame = cv.flip(frame, 1)
            frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)

            if self.fg.display_queue.full():
                _ = self.fg.display_queue.get()
            self.fg.display_queue.put(frame)
            time.sleep(0.005)

class DisplayThread(threading.Thread):
    def __init__(self, finger_counter):
        super().__init__()
        self.fg = finger_counter

    def run(self):
        while not self.fg.exit_flag:
            if self.fg.display_queue.empty():
                time.sleep(0.01)
                continue
            frame = self.fg.display_queue.get()
            cv.imshow('Finger Counter', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                self.fg.exit_flag = True
                break
        cv.destroyAllWindows()

# ------------------ Main ------------------

def main():
    fg = FingerCounter()

    t_capture = CaptureThread(fg)
    t_process = ProcessThread(fg)
    t_display = DisplayThread(fg)

    t_capture.start()
    t_process.start()
    t_display.start()

    try:
        while not fg.exit_flag:
            time.sleep(0.1)
    except KeyboardInterrupt:
        fg.exit_flag = True

    t_capture.join()
    t_process.join()
    t_display.join()

if __name__ == '__main__':
    main()
