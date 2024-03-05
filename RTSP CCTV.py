import cv2
import numpy as np
#import face_recognition
cap = cv2.VideoCapture('rtsp://admin:thietgia95@192.168.1.245:554/cam/realmonitor?channel=1&subtype=1')
i = 0
"""while True:
    ret, img = cap.read()
    cv2.imshow('video output', img)
    face_locations = face_recognition.face_locations(img)
    if (len(face_locations)!=0):
        print("I found {} face(s) in this photograph.".format(len(face_locations)))
        cv2.imsave (str(i) + '.png', img)
        i = i+1
    k = cv2.waitKey(10)& 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()"""

import cv2, queue, threading, time

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()

#cap = VideoCapture('rtsp://admin:thietgia95@192.168.1.245:554/cam/realmonitor?channel=1&subtype=1')
#cap = VideoCapture('rtsp://admin:thietgia95@192.168.1.247:554/cam/realmonitor?channel=1&subtype=1')
#cap = VideoCapture('rtsp://admin:thietgia95@192.168.1.248:554/cam/realmonitor?channel=1&subtype=1')
cap_list = [VideoCapture('rtsp://admin:thietgia95@192.168.1.245:554/cam/realmonitor?channel=1&subtype=1'),
            VideoCapture('rtsp://admin:thietgia95@192.168.1.247:554/cam/realmonitor?channel=1&subtype=1'),
            VideoCapture('rtsp://admin:thietgia95@192.168.1.248:554/cam/realmonitor?channel=1&subtype=1'),
            VideoCapture('rtsp://admin:thietgia95@192.168.1.249:554/cam/realmonitor?channel=1&subtype=1'),
            VideoCapture('rtsp://admin:thietgia95@192.168.1.250:554/cam/realmonitor?channel=1&subtype=1')]
window_dim = (800, 1200)
cap_list_dim = [(0,0, 800, 800), (0, 800, 200, 400), (200, 800, 200, 400), (400, 800, 200, 400), (600, 800, 200, 400)]
og_windows = np.zeros ((*(window_dim), 3), dtype = np.uint8)
while True:
    for idx, cap in enumerate(cap_list):
      img = cap.read()
      img = cv2.resize (img, (cap_list_dim[idx][3:1:-1]))
      #img = cv2.resize (img, (cap_list_dim[idx][2:4]))
      og_windows [cap_list_dim[idx][0]:(cap_list_dim[idx][0]+cap_list_dim[idx][2]),
                  cap_list_dim[idx][1]:(cap_list_dim[idx][1]+cap_list_dim[idx][3])] = img
    cv2.imshow('video output', og_windows)
    k = cv2.waitKey(10)& 0xff
    if k == 27:
        break
"""while True:
    img = cap.read()
    cv2.imshow('video output', img)
    #face_locations = face_recognition.face_locations(img)
    #if (len(face_locations)!=5):
    #    print("I found {} face(s) in this photograph.".format(len(face_locations)))
        #cv2.imsave (str(i) + '.png', img)
    #    i = i+1
    k = cv2.waitKey(10)& 0xff
    if k == 27:
        break
"""
cap.release()
cv2.destroyAllWindows()
