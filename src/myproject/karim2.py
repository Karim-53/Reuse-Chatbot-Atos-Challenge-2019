import subprocess
proc = subprocess.Popen(['/home/karim/darknet/darknet', 'detect', '/home/karim/darknet/cfg/yolov3.cfg', '/home/karim/darknet/yolov3.weights', '/home/karim/darknet/data/dog.jpg'], stdout=subprocess.PIPE, cwd="/home/karim/darknet/")
output = proc.stdout.read()
print( output )









#import subprocess
#result = subprocess.run(['./darknet', 'detect', 'cfg/yolov3.cfg', 'yolov3.weights', 'data/dog.jpg'], stdout=subprocess.PIPE)
#print( result.stdout )
