import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import pickle

DATADIR = os.getcwd() + "/Training Samples"
CATEGORIES = ["N", "P"]
IMG_SIZE = 50

training_data = []

def create_training_data():
	for category in CATEGORIES:
		path = os.path.join(DATADIR, category).replace("\\","/")
		class_num = CATEGORIES.index(category)
		for img in os.listdir(path):
			try:
				img_array = cv2.resize(cv2.imread(os.path.join(path, img).replace("\\","/"), cv2.IMREAD_GRAYSCALE), (IMG_SIZE, IMG_SIZE))
				training_data.append([img_array, class_num])
				print("added image " + img + " to training set")
			except Exception as e:
				pass
			#plt.imshow(img_array, cmap="gray")
			#plt.show()

create_training_data()
rd.shuffle(training_data)

X = []
y = []

for features, label in training_data:
	X.append(features)
	y.append(label)

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close

pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close