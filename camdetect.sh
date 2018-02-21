#!/bin/bash

xhost +

docker run -it --rm  --privileged \
  --env DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  alkari/camdetect python3 camdetect/camdetect.py

xhost -
