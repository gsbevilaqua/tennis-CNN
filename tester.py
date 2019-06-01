import cv2
import tensorflow as tf
from functools import reduce
import os

DATADIR = os.getcwd()
CATEGORIES = ["BETWEEN POINTS", "POINT ONGOING"]
IMG_SIZE = 50

MA = []
last_frames_classification = []
nopoints_count = 0
points_count = 0
point_text_counter = 0
point = False
current_frame = 0

def prepare(filepath):
	img_array = cv2.resize(cv2.imread(filepath, cv2.IMREAD_GRAYSCALE), (IMG_SIZE, IMG_SIZE))
	return img_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

model = tf.keras.models.load_model("pointornopoint-CNN.model")

#use any tennis match video here
cap = cv2.VideoCapture("videos/aus2010.mp4")

while True:
	ret, frame = cap.read()
	current_frame += 1
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	if not ret:
		break

	mask_over_gray = cv2.inRange(gray, 150, 255)
	blurred = cv2.GaussianBlur(mask_over_gray, (5, 5), 0)
	edged = cv2.Canny(blurred, 50, 230, 255)

	cv2.imwrite(DATADIR + "/feed.jpg", mask_over_gray);

	prediction = model.predict([prepare(DATADIR + "/feed.jpg")])
	MA.append(prediction[0][0])
	prediction_str = CATEGORIES[int(prediction[0][0])]

	if(len(MA)>50):
		MA.pop(0)
		mean = reduce(lambda x, y: x + y, MA) / 50
		if(mean > 0.5):
			last_frames_classification.append(1.0)
			points_count += 1
			mean = 1.0
			cv2.putText(frame, CATEGORIES[1], (100,130), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
		else:
			last_frames_classification.append(0.0)
			nopoints_count += 1
			mean = 0.0
			cv2.putText(frame, CATEGORIES[0], (100,130), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
	else:
		last_frames_classification.append(prediction[0][0])
		cv2.putText(frame, prediction_str, (100,130), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
		mean = prediction[0][0]	

	if(len(last_frames_classification) > 150):
		last_frames_classification.pop(0)

	if(mean == 0.0):# and nopoints_count > 30):
		points_count = 0
		mean = reduce(lambda x, y: x + y, last_frames_classification) / 150
		if(mean < 2/3 and mean > 0.0):
			print(mean)
			last_frames_classification = []
			cv2.putText(frame, "POINT!!", (100,160), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,50,250), 2);
			points_output = open("final.txt", "a")
			points_output.write(str(current_frame) + '\n')
			points_output.close()
			point = True

	if(point):
		cv2.putText(frame, "POINT!!", (100,160), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,50,250), 2);
		point_text_counter += 1
		if(point_text_counter > 200):
			point_text_counter = 0
			point = False

	cv2.putText(frame, "Frame : " + str(int(current_frame)), (100,530), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (250,170,50), 2);	

	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask_over_gray)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break	

cap.release()
cv2.destroyAllWindows()
