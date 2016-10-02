#!/bin/bash

if [ -a /home/pi/security_camera.pid ]; kill -INT $(cat /home/pi/security_camera.pid); fi
