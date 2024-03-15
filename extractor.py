import cv2
import random
import os
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("video", help="Source video name with .mp4 extension")
parser.add_argument("frames", nargs="?", default="3000", help="Number of frames to extract. Defaults to 3000")

args = parser.parse_args()

video_name = args.video
num_of_frames = int(args.frames)  #30000 corresponds to about a 15 minute video

base, extension = os.path.splitext(video_name)

video = cv2.VideoCapture(video_name)
max_length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

i = 0

ret, frame = video.read()
video.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if ret is False:
    print("Error reading video")

else:
    os.makedirs(base, exist_ok=True)
    start = datetime.datetime.now()
    print("Starting extraction of "+str(num_of_frames)+" random frames of "+video_name+": "+str(start))
    while(i < num_of_frames):
        frame_id = random.randint(0, max_length)
        
        ret, frame = video.read()
    
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    
        cv2.imwrite(base+"/frame%d.jpg" % i, frame)
        i+=1
    end = datetime.datetime.now()
    print("Ending extraction :"+str(end))
    print("Elapsed time: "+str((end-start)))

video.release()
cv2.destroyAllWindows()
