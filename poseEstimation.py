import cv2 as cv
import numpy as np

net = cv.dnn.readNetFromTensorflow("static/graph_opt.pb")

inWidth = 300
inHeight = 400
thr = 0.1

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

# Create list of pairs of body parts

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"], ["Neck", "Nose"]]

def pose_estimation(frame, thickness = 25):
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    
    canvas = np.zeros((frameHeight, frameWidth, 1), dtype = "uint8") # Print pose over a black background 
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > thr else None)

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(canvas, points[idFrom], points[idTo], (255, 255, 255), thickness)
            
    return canvas

def crop_image(imgToCrop):
  xmin, xmax, ymin, ymax = 100000, 0, 100000, 0
  for i in range(len(imgToCrop)):
    for j in range(len(imgToCrop[i])):
      if(imgToCrop[i][j] > 0):
        if i < ymin:
          ymin = i
        if i > ymax:
          ymax = i
        if j < xmin:
          xmin = j
        if j > xmax:
          xmax = j
  return imgToCrop[ymin:ymax,xmin:xmax]

def resize_image(imgToResize, width, height):
  resized_image = cv.resize(imgToResize,
                            (width, height), 
                         interpolation = cv.INTER_NEAREST)
  return resized_image
