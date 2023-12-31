import cv2
import time 
import imutils

cam = cv2.VideoCapture(0) #for main cam
# cam = cv2.VideoCapture(1) #for usb cam

time.sleep(1)

firstFrame = None
area = 500

while True:
    _,img = cam.read()
    text =  "Normal"
    img = imutils.resize(img, width=500)
    grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gaussianImg = cv2.GaussianBlur(grayImg, (21,21), 0)
    if firstFrame is None:
        firstFrame = gaussianImg
        continue
    imgDiff =  cv2.absdiff(firstFrame,gaussianImg)
    thresholdImg = cv2.threshold(imgDiff, 25, 255, cv2.THRESH_BINARY)[1]
    dilateImg = cv2.dilate(thresholdImg, None, iterations=2)
    cntrs= cv2.findContours(thresholdImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntrs = imutils.grab_contours(cntrs)
    for c in cntrs:
        if cv2.contourArea(c) < area:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
        text = "Moving Object detected"
    print(text)
    cv2.putText(img, text, (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Camera Feed", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
