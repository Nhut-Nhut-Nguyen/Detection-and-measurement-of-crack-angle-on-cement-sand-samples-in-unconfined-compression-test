# importing the module
import cv2
import numpy as np
import math
# function to display the coordinates of
# of the points clicked on the image
prevX,prevY=-1,-1
def click_event(event, x, y, flags, params):
	global prevX, prevY, drawing
	# checking for left mouse clicks
	if event == cv2.EVENT_LBUTTONDOWN:
		#print("Point x ; y")
		drawing = (x, y)
		cv2.circle(img, (x, y), 5, (200, 0, 0), -1)
		strXY = '(' + str(x) + ' ; ' + str(y) + ')'
		font = cv2.FONT_HERSHEY_PLAIN
		#cv2.putText(img, strXY, (x + 10, y - 10), font, 1, (255, 0, 0), 2)

		if prevX == -1 and prevY == -1:
			prevX, prevY = x, y
		else:
			cv2.line(img, (prevX, prevY), (x, y), (0, 255, 255), 4)
			x1 = prevX
			y1 = prevY
			print("point_1_(x1_y1)")
			print(prevX, prevY)
			prevX, prevY = -1, -1
			x2 = x
			y2 = y
			print("point_2_(x2_y2)")
			print(x, y)
			length_x_2 = math.pow((x2-x1),2)
			length_y_2 = math.pow((y2-y1),2)
			print("length line")
			#length_line = math.sqrt(length_x_2+length_y_2)*(49/(178*2))
			length_line = math.sqrt(length_x_2 + length_y_2)
			print(length_line)
			cv2.rectangle(img, (int(x-58),int(y-7)), (int(x + 250), int(y-70)), (255, 255, 255), -1)
			#cv2.putText(img,format(round(length_line, 1))+"mm", (int(x-55), int(y-15)), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 150), 2)
			cv2.putText(img, format(round(length_line*50/390,1))+".mm", (int(x - 55), int(y - 15)), cv2.FONT_HERSHEY_COMPLEX,2, (0, 0, 150), 2)
		# displaying the coordinates
		# on the Shell
		#print(x, ';', y)
		cv2.imshow("image", img)

# driver function
if __name__=="__main__":
	# reading the image
	img = cv2.imread('images0.jpg', 1)
	img = cv2.resize(img, (1280, 960))

	#l1 = cv2.line(img, (470, 0), (470, 960), (255, 255, 0), 1)
	#L = cv2.line(img, (590, 0), (590, 960), (0, 255, 255), 1)
	#x1 = cv2.line(img, (825, 0), (825, 960), (255, 255, 0), 1)
	#r2 = cv2.line(img, (0, 855), (1280, 855), (0, 200, 0), 1)
	#H = cv2.line(img, (0, 690), (1280, 690), (0, 255, 200), 1)
	#x2 = cv2.line(img, (0, 150), (1280, 150), (0, 200, 0), 1)
	#t1 = cv2.line(img, (0, 285), (1280, 285), (255, 0, 255), 1)
	#b2 = cv2.line(img, (500, 750), (750, 750), (0, 120, 0), 1)
	#a = cv2.line(img, (500, 750), (750, 180), (0, 120, 0), 1)
	# displaying the image
	cv2.imshow("image", img)

	# setting mouse handler for the image
	# and calling the click_event() function
	# cv2.setMouseCallback("image", printCoordinate)
	cv2.setMouseCallback('image', click_event)
	# wait for a key to be pressed to exit
	try:


		# cv2.imshow("Capturing", frame)
		key = cv2.waitKey(0)
		if key == ord('s'):
			cv2.imwrite(filename='saved_img.jpg', img=img)
			# webcam.release()
			img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
			img_new = cv2.imshow("Captured Image", img_new)
			cv2.waitKey(500)
			cv2.destroyAllWindows()
			img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
			gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
			# img_ = cv2.resize(gray,(28,28))
			img_resized = cv2.imwrite("img" + ".jpg", img=img_)
	except(KeyboardInterrupt):
		cv2.destroyAllWindows()
	cv2.waitKey(0)
	# close the window
	cv2.destroyAllWindows()
