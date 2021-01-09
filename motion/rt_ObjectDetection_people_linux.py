# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse, imutils, time, cv2, sys, pymysql

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
    help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
    help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
    help="minimum probability to filter weak detections")
ap.add_argument("-v", "--video", default='stream', help="path/url to video file/streams")
ap.add_argument("-f", "--frameskip", default=10, help="frames to skip(default: 10)")
ap.add_argument("-s", "--stdout", default='no', help="use stdout to use vlc stream(yes or no, default: no)")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
#CLASSES = ["background","person"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] Loading model ...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] Starting video stream ...")
if args["video"] == 'stream':
    vs = VideoStream(src=0).start()
    print("[INFO] Using webcam as video stream ...")
else:
    vs = FileVideoStream(args["video"]).start()
    print("[INFO] Using video file/url as video stream ...")

# Database setup..
## Create connection to MySQL server
print("Connecting ...")
try:
    connection = pymysql.connect(host='localhost',
                                 user='pi',
                                 password='raspberry',
                                 db='pi',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
except pymysql.err.Error as msg:
    print("Connection error: ", msg)
    exit()
## Create cursor
cc = connection.cursor()
#----------------------------------------------------------------------------------------->


time.sleep(1.0)
fps = FPS().start()

# loop over the frames from the video stream
if int(args["frameskip"]) == 0:
    args["frameskip"] = 10
print("[INFO] Frameskip set to", args["frameskip"],"...")
i,f = 0, int(args["frameskip"])

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
if '://' in args["video"] or args["video"] == 'stream':
        frame = vs.read()
else:
    ret, frame = vs.read()
(h, w) = frame.shape[:2]
 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), (f/2), (w,h))

while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    if '://' in args["video"] or args["video"] == 'stream':
        frame = vs.read()
    else:
        ret, frame = vs.read()
    #frame = imutils.resize(frame, width=400)
    #read every 30th frame
    if i % f == 0:
        (h, w) = frame.shape[:2]
        pframe = imutils.resize(frame, width=200)
        # grab the pframe dimensions and convert it to a blob
        (ph, pw) = pframe.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(pframe, (300, 300)),
            0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                #only show person which index is 15
                if idx == 15:
                    motion = 1
                    '''# compute the (x, y)-coordinates of the bounding box
                    # for the object
                    box = detections[0, 0, i, 3:7] * np.array([pw, ph, pw, ph])
                    (pstartX, pstartY, pendX, pendY) = box.astype("int")

                    # draw the bounding box around the detected object on
                    # the frame
                    plabel = "{}: {:.2f}%".format(CLASSES[idx],
                        confidence * 100)
                    cv2.rectangle(pframe, (pstartX, pstartY), (pendX, pendY),
                        COLORS[idx], 1)
                    py = pstartY - 15 if pstartY - 15 > 15 else pstartY + 15
                    cv2.putText(pframe, plabel, (pstartX, py),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, COLORS[idx], 1)
                    '''
                    # compute the (x, y)-coordinates of the bounding box
                    # for the object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # draw the bounding box around the detected object on
                    # the frame
                    label = "{}: {:.2f}%".format(CLASSES[idx],
                        confidence * 100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                        COLORS[idx], 1)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, COLORS[idx], 1)
                else:
                    motion = 0
                try:
                    result = "UPDATE `motion` SET `deteksi`='%s' WHERE `motion`.`sensor` = 'motion';" % (motion)
                    cc.execute(result)
                    connection.commit()
                except pymysql.err.InternalError as msg:
                    print("Command skipped: ", msg)

        # show the output pframe
        #cv2.imshow("pframe", pframe)
        #cv2.imshow("frame", frame)
        #out.write(frame)
        print("Motion:", motion)
        cv2.imwrite("video.jpg", frame)
        cv2.imwrite("/var/www/tambak/video.jpg", frame)
        
        if args["stdout"] == 'yes':
            sys.stdout.buffer.write(frame.tobytes())
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # if there is no more pframe, break from the loop
    if '://' not in args["video"] and '.' in args["video"]:
        if ret == False:
            break
    i = i + 1
    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
out.release()
connection.close()