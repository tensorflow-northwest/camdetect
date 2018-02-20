# coding: utf-8

"""camDetect: Use a Webcam with OpenCV and TensorFlow to detect objects"""

__author__      = "@alkari"


# # camDetect

# Env Setup & Imports

import os
import sys

# Set your PYTHONPATH.
PACKAGES_PATH = '/usr/local/lib/python3.5/dist-packages' # Adjust if using other version
sys.path.append("..")
sys.path.append(PACKAGES_PATH + '/tensorflow') 
sys.path.append(PACKAGES_PATH + '/tensorflow/models') 
sys.path.append(PACKAGES_PATH + '/tensorflow/models/research')
sys.path.append(PACKAGES_PATH + '/tensorflow/models/research/slim')
sys.path.append(PACKAGES_PATH + '/tensorflow/models/research/object_detection')



# Import required libraries
import numpy as np
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
import zipfile
import cv2

from collections import defaultdict
from io import StringIO
from PIL import Image

# Import Object Detection support functions
from utils import label_map_util
from utils import visualization_utils as vis_util


# # Model preparation 

# ## Variables
# 
# Any model exported using the `export_inference_graph.py` tool can be loaded simply
# by changing `PATH_TO_CKPT` to point to a new .pb file.  
# 
# Other models that can be run out-of-the-box with varying speeds and accuracies are available via [detection model zoo] at:
# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
# Some examples commented below.
#
# Comment out only one of the models below..

MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17' # FASTEST
# MODEL_NAME = 'ssd_inception_v2_coco_2017_11_17'
# MODEL_NAME = 'rfcn_resnet101_coco_11_06_2017'
# MODEL_NAME = 'faster_rcnn_resnet101_coco_11_06_2017'
# MODEL_NAME = 'faster_rcnn_inception_resnet_v2_atrous_coco_11_06_2017'


MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = PACKAGES_PATH + '/tensorflow/models/research/object_detection/data/mscoco_label_map.pbtxt'

# Number of classes to include in object detection
NUM_CLASSES = 200


# ## Download and expand model if not on disk

if not os.path.isfile(MODEL_FILE):
    opener = urllib.request.URLopener()
    opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
if not os.path.isdir(MODEL_NAME):
    tar_file = tarfile.open(MODEL_FILE)
    for file in tar_file.getmembers():
        file_name = os.path.basename(file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, os.getcwd())

## Video Capture & Record

# Ensure directory exists for video recording output
if not os.path.exists('output'):
  os.makedirs('output')

# Increment output video file name
filename = 1
while os.path.isfile("output/video_"+str(filename)+".avi"):
    filename += 1

# Select detection device (camera)
device = int(sys.argv[1]) if len(sys.argv) > 1 else 0

# Create and resize display window
cv2.namedWindow("Object Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Object Detection", 640, 480)
cv2.moveWindow("Object Detection", 420, 0)

# Initiate frame capture
cap = cv2.VideoCapture(device)
cap.set(3,640)
cap.set(4,480)

# Add frame to video recording
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output/video_"+str(filename)+'.avi', fourcc, 20.0, (640, 480))


# ## Load a (frozen) Tensorflow model into memory.

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Load label map
# Label map translantes prediction output like `5` to corresponding label `airplane`. Using internal utility functions to return a dictionary mapping integers to appropriate string labels.

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


### Main Detection loop

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        while True:
            # Capture a frame from webcam using OpenCV
            ret, image_np = cap.read()
            
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            
            # Each box represents a part of the image where a particular object was detected.
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            
            # Each score represent the level of confidence for each of the objects.
            # Score is shown on the resulting image box, together with the class label.
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            
            # Actual detection session run
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            
            # Visualization of the results of detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8)
            
            # Display frame in detection window
            cv2.imshow('Object Detection', image_np)
            out.write(image_np)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                break



