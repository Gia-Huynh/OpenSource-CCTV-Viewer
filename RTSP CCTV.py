import cv2
import numpy as np
i = 0

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

cap_list = [VideoCapture('rtsp://admin:thietgia95@192.168.1.245:554/cam/realmonitor?channel=1&subtype=1'),
            VideoCapture('rtsp://admin:thietgia95@192.168.1.247:554/cam/realmonitor?channel=1&subtype=1'),
            VideoCapture('rtsp://admin:thietgia95@192.168.1.248:554/cam/realmonitor?channel=1&subtype=1'),
            VideoCapture('rtsp://admin:thietgia95@192.168.1.249:554/cam/realmonitor?channel=1&subtype=1'),
            VideoCapture('rtsp://admin:thietgia95@192.168.1.250:554/cam/realmonitor?channel=1&subtype=1')]
window_dim = (900, 1600)
cap_list_dim = [(0,0, 800, 800), (0, 800, 200, 400), (200, 800, 200, 400), (400, 800, 200, 400), (600, 800, 200, 400)]
scale = 100
cap_list_dim = np.array([(0,0, 100, 66.6), (0, 66.7, 25, 33.3), (25, 66.7, 25, 33.3), (50, 66.7, 25, 33.3), (75, 66.7, 25, 33.3)]).astype(np.float64)
cap_list_dim[:,0]*= window_dim[0]/scale
cap_list_dim[:,1]*= window_dim[1]/scale
cap_list_dim[:,2]*= window_dim[0]/scale
cap_list_dim[:,3]*= window_dim[1]/scale
cap_list_dim = cap_list_dim.astype (np.int32)
og_windows = np.zeros ((*(window_dim), 3), dtype = np.uint8)
while True:
    for idx, cap in enumerate(cap_list):
      img = cap.read()
      cap_dim = cap_list_dim[idx]
      img = cv2.resize (img, (cap_dim[3:1:-1]))
      if (cap_dim[0]+cap_dim[2] > og_windows.shape[0]) or (
        cap_dim[1]+cap_dim[3] > og_windows.shape[1]):
          og_windows [cap_dim[0]:min(cap_dim[0]+cap_dim[2], og_windows.shape[0]),
                  cap_dim[1]:min(cap_dim[1]+cap_dim[3], og_windows.shape[1])] = img[0:min(cap_dim[0]+cap_dim[2], og_windows.shape[0])-cap_dim[0],
                                                                                    0:min(cap_dim[1]+cap_dim[3], og_windows.shape[1])-cap_dim[1]]
      else:
          og_windows [cap_dim[0]:(cap_dim[0]+cap_dim[2]),
                  cap_dim[1]:(cap_dim[1]+cap_dim[3])] = img
    cv2.imshow('video output', og_windows)
    k = cv2.waitKey(10)& 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
