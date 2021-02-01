# USAGE
# python yolo_object_detection.py --input example_videos/janie.mp4 --output ../output_videos/yolo_janie.avi --yolo yolo-coco --display 0
# python yolo_object_detection.py --input example_videos/janie.mp4 --output ../output_videos/yolo_janie.avi --yolo yolo-coco --display 0 --use-gpu 1

#python yolo_object_detection.mod.py --input ..\videos\brumotti2wide.mp4 --confidence 0.4  --yolo yolo-coco --display 1 --use-gpu 1

'''Use CSRT when you need higher object tracking accuracy and can tolerate slower FPS throughput
Use KCF when you need faster FPS throughput but can handle slightly lower object tracking accuracy
Use MOSSE when you need pure speed'''

# import the necessary packages
import numpy as np

import cv2
import os
import sys
from PIL import Image





class YoloDetector:

	identity_method = ''
	video = None
	frame = None
	matte = None
	#frame_size: (0,0)
	confidence = 0
	threshold = 0
	COLORS = []
	mattes = []
	confidences = []
	classIDs = []
	ids = []
	frame_n = 0
	use_gpu = True
	model_path = ''
	box_identifier = None
	identity_bboxes = {}
	analyzed_bboxes = []
	img_to_detect = None
	img_to_show = None
	cv_image = None

	def __init__(self, img_to_detect=None, min_confidence=0.5, threshold=0.5, use_gpu=False, identity_method='area'):
		SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
		
		self.path=SITE_ROOT
		self.identity_method = identity_method
		self.confidence=min_confidence
		self.threshold = threshold
		self.frame_n = 0
		self.use_gpu = use_gpu

		print(os.path)
		#mettere una verifica server

		self.img_to_detect = Image.open(self.path+"\people.jpg").convert('RGB')
		self.cv_image = np.array(self.img_to_detect)  

		# load the COCO class labels our YOLO model was trained on
		self.labelsPath = self.path+"\coco.names.wider"
		self.LABELS = open(self.labelsPath).read().strip().split("\n")

		# initialize a list of colors to represent each possible class label
		np.random.seed(42)
		self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
			dtype="uint8")

		'''LOADING RESOURCES'''
		# derive the paths to the YOLO weights and model configuration
		weightsPath = self.path+"\yolov3-wider_16000.weights"
		#weightsPath = self.model_path+"yolov3-wider_16000.weights"
		#weightsPath = self.model_path+"yolov3-tiny.weights"
		configPath = self.path+"\yolov3-wider.cfg"
		#configPath = self.model_path+"yolov3-wider.cfg"
		#configPath = self.model_path+"yolov3-tiny.cfg"
		print("using weights and cfg: ",weightsPath,configPath)

		# load our YOLO object detector trained on COCO dataset (80 classes)
		print("[INFO] loading YOLO from disk...")
		self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

		# check if we are going to use GPU
		if self.use_gpu:
			# set CUDA as the preferable backend and target
			print("[INFO] setting preferable backend and target to CUDA...")
			self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
			self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

		# determine only the *output* layer names that we need from YOLO
		self.ln = self.net.getLayerNames()
		self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

		
	def getResult(self):
		return {'result':True}


	# --------------------------------------------------------------------------------------------------------
	# ------------------------------------GET BBOXES SINGLE FRAME---------------------------------------------
	# --------------------------------------------------------------------------------------------------------

	def run_singleframe_detector(self, cv_image = None,  min_confidence = 0.5, threshold = 0.5, blur=True, show_yolobox = True):
		# initialize the width and height of the frames in the video file
		
		#\	self.cv_image=cv_image
		self.W = None
		self.H = None
		self.threshold = threshold
		self.confidence = min_confidence
		bboxes = []
		outputIndex = 0
		self.confidences = []
		self.classIDs = []

		# if the frame dimensions are empty, grab them
		if self.W is None or self.H is None:
			(self.H, self.W) = self.cv_image.shape[:2]


		blob = cv2.dnn.blobFromImage(self.cv_image, 1 / 255.0, (416, 416),
									 swapRB=True, crop=False)
		self.net.setInput(blob)
		layerOutputs = self.net.forward(self.ln)

		# loop over each of the layer outputs
		bboxes = []
		for output in layerOutputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability)
				# of the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]

				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > self.confidence:
					# scale the bounding box coordinates back relative to
					# the size of the image, keeping in mind that YOLO
					# actually returns the center (x, y)-coordinates of
					# the bounding box followed by the boxes' width and
					# height
					box = detection[0:4] * np.array([self.W, self.H, self.W, self.H])
					(centerX, centerY, width, height) = box.astype("int")

					# use the center (x, y)-coordinates to derive the top
					# and and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))

					# update our list of bounding box coordinates,
					# confidences, and class IDs
					bboxes.append([x, y, int(width), int(height)])
					self.confidences.append(float(confidence))
					self.classIDs.append(classID)

		# apply non-maxima suppression to suppress weak, overlapping
		# bounding boxes

		idxs = cv2.dnn.NMSBoxes(bboxes, self.confidences, self.confidence, self.threshold)
		detected_bboxes = []
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (bboxes[i][0], bboxes[i][1])
				(w, h) = (bboxes[i][2], bboxes[i][3])
				detected_bboxes.append((x, y, w, h))
				# ******* Trova il valore medio della luminosità per ogni box ma dobbiamo trovare il valore colore di tutto il soggetto ( box più grande )
				# -------- Test sui confini del box
				tlx = int(x + int(w/4))
				tly = int(y + int(y/4))
				brx = tlx + int(w/2)
				bry = tly + int(h/2)
				#\	cropped_frame = self.frame[(y-h):(y-h) + (h*2), (x-w):(x-w) + (w*2)]
				cropped_img = self.cv_image[tly:bry, tlx:brx]
				color = (0, 255, 0)
				if show_yolobox: cv2.rectangle(self.cv_image, (x,y), (x+w,y+h), color, 1)
				# text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
				if show_yolobox: cv2.putText(self.cv_image, str(i), (x, y - 5),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
				#\	if blur: self.frame, self.matte = blur_area(self.frame, self.matte, bboxes[i])
				# check to see if the output frame should be displayed to our
				# screen
		#return {'result':True}
		return {'bboxes' : detected_bboxes}
		return {'bboxes' : detected_bboxes, 'result_img' : self.img_to_detect}

	

	def __del__(self):
		self.bboxes = None
		self.ln = None
		self.net = None
		self = None
		print ("detector deleted")

