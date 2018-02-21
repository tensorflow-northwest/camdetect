# camdetect

### Object Detection using a webcam with OpenCV and TensorFlow

### Tested on Ubuntu 16.04 LTS

### Author: @alkari

## Install steps:
############################################################


```
apt-get update
apt-get install git -y

# Install OpenCV 3.3
git clone https://github.com/alkari/install_cv2.git
cd install_cv2
chmod +x ubuntu_install_cv2.sh
bash ubuntu_install_cv2.sh

# Install tensorflow & other packages
apt-get update
apt-get install git -y
apt-get install protobuf-compiler python-pil python-lxml python3-pip -y
pip3 install --upgrade pillow lxml jupyter matplotlib tensorflow
cd /usr/local/lib/python3.5/dist-packages/tensorflow
git clone https://github.com/tensorflow/models.git
cd models/research/
protoc object_detection/protos/*.proto --python_out=.
### From tensorflow/models/research/
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
git clone https://github.com/tensorflow-northwest/camdetect.git
apt-get clean
rm -rf /var/lib/apt/lists/*
cd camdetect/
python3 camdetect.py
```

