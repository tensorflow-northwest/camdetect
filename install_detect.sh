#!/bin/bash
#
# Install camdetect 
#
# Tested on Ubuntu 16.04 LTS
#
# Author: @alkari

set -e

apt-get -y update

apt-get -y install python3.5-dev python3-pip wget unzip \
    build-essential cmake git pkg-config libatlas-base-dev gfortran \
    libjasper-dev libgtk2.0-dev libavcodec-dev libavformat-dev \
    libswscale-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev \
    libv4l-dev ffmpeg

pip3 install --upgrade pip
pip3 install --upgrade scikit-image

pip3 install numpy

cd ~

wget https://github.com/Itseez/opencv/archive/3.3.0.zip -O opencv3.zip

unzip -q opencv3.zip && mv opencv-3.3.0 opencv && rm opencv3.zip

wget https://github.com/Itseez/opencv_contrib/archive/3.3.0.zip -O opencv_contrib3.zip

unzip -q opencv_contrib3.zip && mv opencv_contrib-3.3.0 opencv_contrib && rm opencv_contrib3.zip

mkdir opencv/build && cd opencv/build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D BUILD_PYTHON_SUPPORT=ON \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
      -D BUILD_EXAMPLES=OFF \
      -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 \
      -D BUILD_opencv_python3=ON \
      -D BUILD_opencv_python2=OFF \
      -D WITH_IPP=OFF \
      -D WITH_FFMPEG=ON \
      -D WITH_V4L=ON .. 

make -j$(nproc)

make install

ldconfig

cd ~

rm -rf opencv opencv_contrib

echo "OpenCV installed successfully"


apt-get -y update

apt-get install protobuf-compiler python-pil python-lxml python3-pip git -y
pip3 install --upgrade pillow lxml jupyter matplotlib tensorflow
cd /usr/local/lib/python3.5/dist-packages/tensorflow
git clone https://github.com/tensorflow/models.git
cd models/research/
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
git clone https://github.com/tensorflow-northwest/camdetect.git

# Cleanup
apt-get -y remove build-essential cmake git pkg-config libatlas-base-dev \
    gfortran libjasper-dev libgtk2.0-dev libavcodec-dev libavformat-dev \
    libswscale-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libv4l-dev
apt-get clean
rm -rf /var/lib/apt/lists/*

echo "Install complete. run: python3 camdetect.py"
