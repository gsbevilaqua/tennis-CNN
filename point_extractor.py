import cv2
import os
import numpy as np

DATADIR = os.getcwd()
CATEGORIES = ["Top", "Botton"]
VIDEO_LENGTH = 267603

cap = cv2.VideoCapture("videos/points.mp4")
current_frame = 0
mode = 0

while True:
	ret, frame = cap.read()
	current_frame += 1

	if not ret:
		break

	# Display current frame
	cv2.putText(frame, "Current frame: " + str(int(current_frame)), (100,530), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);	

	cv2.imshow('frame', frame)

	if mode == 0:
		if cv2.waitKey(1) & 0xFF == ord('p'):
			mode = 1

	if mode == 1:
		while True:
			keypressed = cv2.waitKey(0)

			if keypressed == ord('f'):
				current_frame = int(input("Go to frame: "))
				print("You're now on frame", current_frame)
				frame_no = (current_frame/(VIDEO_LENGTH*40000))
				cap.set(2, frame_no);
				break			

			if keypressed == ord('t'):
				print("Frame: ", current_frame)
				print(' Top')
				mode = 0
				break
				
			if keypressed == ord('b'):
				print("Frame: ", current_frame)
				print(' Botton')
				mode = 0
				break

			if keypressed == ord('q'):
				break

			else:
				mode = 0
				break

		if keypressed == ord('q'):
			break

							

cap.release()
cv2.destroyAllWindows()