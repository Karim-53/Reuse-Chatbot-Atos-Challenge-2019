import urllib
import json
import os
import subprocess

file = "/home/karim/darknet/data/dog.jpg"
print("testing on file:")
print(file)

proc_yolov3 =      subprocess.Popen(['/home/karim/darknet/darknet', 'detect', '/home/karim/darknet/cfg/yolov3.cfg', '/home/karim/darknet/yolov3.weights', file], stdout=subprocess.PIPE, cwd="/home/karim/darknet/")
proc_yolov3.wait()
out_yolov3 = proc_yolov3.stdout.read()
proc_yolov3_tiny = subprocess.Popen(['/home/karim/darknet/darknet', 'detect', '/home/karim/darknet/cfg/yolov3-tiny.cfg', '/home/karim/darknet/yolov3-tiny.weights', file], stdout=subprocess.PIPE, cwd="/home/karim/darknet/")

proc_yolov3_tiny.wait()
out_yolov3_tiny = proc_yolov3_tiny.stdout.read()

print("*******************----------***********************\n")
print("using the big dataset: yolov3.weights 248.0 Mb")
print( out_yolov3 ) # around 20 sec
print("*******************----------***********************\n")
print("using the big dataset: yolov3-tiny.weights 35,4 Mb")
print( out_yolov3_tiny ) # around 1 sec , but less precise
