# camdetect

### Object Detection using a webcam with OpenCV and TensorFlow

Tested on Ubuntu 16.04 LTS

Author: @alkari

## TL;DR - Run camdetect:

The fastest way to run is using Docker. Once installed, camdetect.sh script is provided to quickly run a container and launch the application.

```
git clone https://github.com/tensorflow-northwest/camdetect.git
cd camdetect
chmod +x camdetect.sh
./camdetect.sh
```



## Options to run pre-compiled in a Docker container:
############################################################

### First, ensure x permissions allow connections on host system
```
xhost +
```

### To run cam object detection:
```
docker run -it --rm  --privileged --env DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro alkari/camdetect python3 camdetect/camdetect.py
```

### To login to the container and examine the files or run manually:
```
docker run -it --rm  --privileged --env DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro -p 8888:8888 alkari/camdetect /bin/bash
```

### To view files in Jupyter notebook
```
docker run -it --rm -p 127.0.0.1:8888:8888 alkari/camdetect sh -c "jupyter notebook --ip=* --allow-root --no-browser"
```

## To Compile and Install from scratch on Ubuntu 16.04:
############################################################

Note: Could take up to an hour to complete.

```
git clone https://github.com/tensorflow-northwest/camdetect.git
cd camdetect
chmod +x install_detect.sh
sudo bash install_detect.sh
```

