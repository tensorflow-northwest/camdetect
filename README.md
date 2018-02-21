# camdetect

### Object Detection using a webcam with OpenCV and TensorFlow

Tested on Ubuntu 16.04 LTS

Author: @alkari

## TL;DR:

```
git clone https://github.com/tensorflow-northwest/camdetect.git
cd camdetect
chmod +x camdetect.sh
./camdetect.sh
```


## Compile and Install from scratch on Ubuntu 16.04:
############################################################


```
apt-get update
apt-get install git -y

### Install OpenCV 3.3
git clone https://github.com/alkari/install_cv2.git
cd install_cv2
chmod +x ubuntu_install_cv2.sh
bash ubuntu_install_cv2.sh

### Install tensorflow & other packages
apt-get update
apt-get install git -y
apt-get install protobuf-compiler python-pil python-lxml python3-pip -y
pip3 install --upgrade pillow lxml jupyter matplotlib tensorflow
cd /usr/local/lib/python3.5/dist-packages/tensorflow
git clone https://github.com/tensorflow/models.git
cd models/research/
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
git clone https://github.com/tensorflow-northwest/camdetect.git
apt-get clean
rm -rf /var/lib/apt/lists/*
cd camdetect/
python3 camdetect.py
```
############################################################


## To run pre-compiled in a Docker container:

### First, ensure x permissions allow connections on host system
```
xhost +
```

### To run cam object detection
```
docker run -it --rm  --privileged --env DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro alkari/camdetect python3 camdetect/camdetect.py
```

### To login to the container
```
docker run -it --rm  --privileged --env DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro -p 8888:8888 alkari/camdetect /bin/bash
```

### To view files in Jupyter notebook
```
docker run -it --rm -p 127.0.0.1:8888:8888 alkari/camdetect sh -c "jupyter notebook --ip=* --allow-root --no-browser"
```
