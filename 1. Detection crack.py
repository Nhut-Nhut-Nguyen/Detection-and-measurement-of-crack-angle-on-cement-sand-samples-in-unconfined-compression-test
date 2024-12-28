import cv2
import numpy as np

# Kích thước khung hình:
width_frame = 1280
height_frame = 960
Known_width = 20      #mm
Known_height = 20     #mm
focal_length = 365       # Với kích thước khung nhìn là 800x700
#unit_mm_pixel = (20/46)


#Known_distance = 400  #mm

#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#cap = cv2.VideoCapture("7B.mp4")

def empty(a):
    pass

def on_trackbar_change(value):
    # Ensure the value is odd
    odd_value = max(value // 2 * 2 + 1, 1)
    #print("Trackbar value (odd):", odd_value)
    return odd_value


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,150)
cv2.createTrackbar("Area","Parameters",8199,60000,empty)        # Pham vi hien thi dien tich tu 1000 - 30000
cv2.createTrackbar("BlockSize", "Parameters", 39, 999, on_trackbar_change)
cv2.createTrackbar("Threshold_C","Parameters",7,120,empty)


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
class HomogeneousBgDetector():
    def __init__(self):
        pass
    def detect_objects(self, image):
        #imgBlur = cv2.GaussianBlur(frame, (7, 7), -1)
        #cv2.imshow('Image GRAY', imgBlur)
        # Convert Image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('Image BGR', frame)
        #cv2.imshow('Image GRAY', gray)
        #Create a Mask with adaptive threshold
        id_BlockSize = cv2.getTrackbarPos("BlockSize", "Parameters")
        BlockSize = on_trackbar_change(id_BlockSize)
        Thresh_C = cv2.getTrackbarPos("Threshold_C", "Parameters")
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, BlockSize, Thresh_C)

        cv2.rectangle(mask, (0, 0), (480, 960), (0, 0, 0), -1)
        cv2.rectangle(mask, (1280, 0), (830, 960), (0, 0, 0), -1)
        cv2.rectangle(mask, (0, 0), (1280, 80), (0, 0, 0), -1)
        cv2.rectangle(mask, (0, 960), (1280, 830), (0, 0, 0), -1)

        #cv2.rectangle(mask, (0, 0), (780, 420), (0, 0, 0), -1)
        #cv2.rectangle(mask, (0, 0), (630, 660), (0, 0, 0), -1)

        cv2.imshow('Image MASK', mask)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.imshow("mask", mask)
        objects_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            areaMin = cv2.getTrackbarPos("Area", "Parameters")
            if area > areaMin:
                #cnt = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
                objects_contours.append(cnt)
        return objects_contours

key = cv2. waitKey(1)
count=0

while True:
    #ret, f = cap.read()  # Đọc máy ảnh với biến khung hình frame
    f = cv2.imread("crack_cemented_sand.jpg")
    frame = cv2.resize(f, (width_frame, height_frame))
    image = frame.copy()
    pic = frame.copy()
    #cv2.line(image, (0, 400), (604, 400), (200, 200, 200), 5)
    #cv2.line(image, (0, 800), (604, 800), (200, 200, 200), 5)
    cv2.getTrackbarPos("Area", "Parameters")
    #Load Object Detector
    detector = HomogeneousBgDetector()
    contours = detector.detect_objects(image)
    # Draw objects boundaries
    for cnt in contours:
        #pl1 = cv2.polylines(frame, [cnt], True, (0,0,255), 1)
        epsilon = 0.0001* cv2.arcLength(cnt, True,)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        #cv2.putText(frame, "Crack mumber : {}".format(a1), (50, 300), cv2.FONT_HERSHEY_COMPLEX, 1, (90, 0, 255), 2)
        cc = cv2.drawContours(image, [approx], 0, (250,0,0), 2)
        #cv2.imshow('cont', cc)
        # Put text
        #cv2.putText(image, "Number of cracks: {}".format(len(contours)), (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (90, 0, 100), 2)
        # Get rect
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect
        #cv2.circle(frame, (int(x), int(y)), 4, (0, 0, 255), -1)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        # Ham vẽ chiều dài và chiều rông vùng nứt
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        # Menggambar titik tengah pada objek
        cv2.circle(image, (int(tltrX), int(tltrY)), 0, (0, 0, 0), 1)
        cv2.circle(image, (int(blbrX), int(blbrY)), 0, (0, 0, 0), 1)
        cv2.circle(image, (int(tlblX), int(tlblY)), 0, (0, 0, 0), 1)
        cv2.circle(image, (int(trbrX), int(trbrY)), 0, (0, 0, 0), 1)
        if w > h:
            #cv2.rectangle(image,(int(x + 55), int(y +58)), (int(x + 280), int(y + 90)), (255,255,255),-1 )
            #cv2.putText(image, "[" + str(round(h, 1)) + "; " + str(round(w, 1)) + "; " + str(round(angle, 1))+"]", (int(x + 60), int(y + 80)), cv2.FONT_HERSHEY_COMPLEX, 0.7, (200, 0, 150), 2)
            cv2.putText(image, "[" + str(round(angle, 1)) + "]" + "degrees", (int(x + 60), int(y + 0)), cv2.FONT_HERSHEY_COMPLEX, 0.8, (160, 0, 210), 2)
            # Menggambar garis pada titik tengah
            longline1 =cv2.line(image, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (0, 0, 255), 3)
            #shortline1 = cv2.line(image, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (0, 90, 0), 2)
        else:
            #cv2.rectangle(image, (int(x + 55), int(y+58)), (int(x + 280), int(y + 90)), (255, 255, 255), -1)
            #cv2.putText(image,"[" + str(round(w, 1)) + "; " + str(round(h, 1)) + "; " + str(round(90-angle, 1)) + "]", (int(x + 60), int(y + 80)), cv2.FONT_HERSHEY_COMPLEX, 0.7, (200, 0, 150), 2)
            cv2.putText(image,"[" + str(round(90 - angle, 1)) + "]" + "degrees",(int(x + 60), int(y + 0)), cv2.FONT_HERSHEY_COMPLEX, 0.8, (160, 0, 210), 2)
            # Menggambar garis pada titik tengah
            longline2 = cv2.line(image, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (0, 0, 255), 3)
            #shortline2 = cv2.line(image, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (0, 90, 0), 2)
        #cv2.polylines(image, [box], True, (255,0,0), 1)


    try:
        #l1 = cv2.line(image, (488, 0), (488, 960), (200, 0, 200), 1)
        #r2 = cv2.line(image, (840, 0), (840, 960), (200, 0, 200), 1)
        #t1 = cv2.line(image, (0, 135), (1280, 135), (250, 0, 200), 1)
        #b2 = cv2.line(image, (0, 842), (1280, 842), (250, 0, 200), 1)

        #x1 = cv2.line(image, (485, 150), (485, 300), (0, 0, 200), 1)
        #x2 = cv2.line(image, (847, 150), (847, 300), (0, 0, 200), 1)


        #cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename='saved_img.jpg', img=image)
            #webcam.release()
            img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
            img_new = cv2.imshow("Captured Image", img_new)
            cv2.waitKey(500)
            cv2.destroyAllWindows()
            img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            #img_ = cv2.resize(gray,(28,28))
            img_resized = cv2.imwrite("images"+str(count)+".jpg", img=img_)
            count = count + 1
            #break
        elif key == ord('q'):
            frame.release()
            cv2.destroyAllWindows()
            break
    except(KeyboardInterrupt):
        frame.release()
        cv2.destroyAllWindows()
        break
    #datet = str(datetime.datetime.now())
    #cv2.putText(image, datet, (950, 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (100, 0, 0), 2)

    cv2.imshow('Crack detection', image)      # Hiển thị khung hình đọc được
    key_pressed = cv2.waitKey(1)
    if key_pressed == 113:       # mã 13 = phím "q"
        break
#cap.release()                       # Giải phóng bộ nhớ của camera
cv2.destroyAllWindows()             # Phá hủy, bỏ hết mọi thứ ngoài windows để giải phóng bộ nhớ
