import cv2
import os
import numpy as np

DATADIR = os.getcwd() + "\\Training Samples"
print(DATADIR)
CATEGORIES = ["N", "P"]

#use any tennis match video here
cap = cv2.VideoCapture("videos/moments.mp4")
frame_number = 0

while True:
	ret, frame = cap.read()
	frame_number += 1
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Start timer
	timer = cv2.getTickCount()

	# Calculate Frames per second (FPS)
	fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);	

	if not ret:
		break

	mask_over_gray = cv2.inRange(gray, 150, 255)
	blurred = cv2.GaussianBlur(mask_over_gray, (5, 5), 0)
	blurredx2 = cv2.GaussianBlur(blurred, (5, 5), 0)
	edged = cv2.Canny(blurred, 50, 230, 255)
	#other_mask = cv2.inRange(hsv, other_lower, other_upper)

	# Display FPS on frame
	cv2.putText(frame, "FPS : " + str(int(fps)), (100,500), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
	# Display FPS on frame
	cv2.putText(frame, "FPS : " + str(int(frame_number)), (100,530), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);	

	cv2.imshow('frame', frame)
	cv2.imshow('edged', edged)

	while True:
		keypressed = cv2.waitKey(0)

		if keypressed == ord('n'):
			print("Frame: ", frame_number)
			print(' No Point')
			cv2.imwrite(DATADIR + "/" + CATEGORIES[0] + "/m" + str(frame_number) + ".jpg", mask_over_gray);
			break
			
		if keypressed == ord('p'):
			print("Frame: ", frame_number)
			print(' Point')
			cv2.imwrite(DATADIR + "/" + CATEGORIES[1] + "/m" + str(frame_number) + ".jpg", mask_over_gray);
			break

		if keypressed == ord('q'):
			break

	if keypressed == ord('q'):
		break	
							

cap.release()
cv2.destroyAllWindows()		
