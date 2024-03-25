# video-frame-extractor
This repository performs data massaging tasks before data is fed into YOLO for analysis.

#extractor.py
This script randomly selects frames of an mp4 video to be used as input for YOLO analysis.

You must include the video as an argument. Number of frames is an optional argument. It will default to 3000. It will take approximately 83 seconds per 1k of frames to run. The equivalent of a 15 minute video is 30000 frames.

A well formed command line execution could be "python3 extractor.py 0004_vid.mp4 3000" or "python3 extractor.py 0004_vid.mp4". The folder the frames are extracted to can be used directly as the input source in YOLOV5.

#data_sanitizer.py
This script will analyze the anotation output following analysis. Given a label directory produced via the --save-txt argument in YOLO, it will copy the frame data containing frames we are interested in into an _OUTPUT directory. It will copy the frame.jpgs, the .txt files, and produce a summary.txt containing the frame numbers that were selected.

You must include the directory of the labels as an input argument. Optional input is number of minimum fish per frame. It will default to 3 fish. The input must be more than 0 fish.

The script expects the .jpgs to live one folder higher than the label directory. 

A well formed command line execution could be "python3 data_sanitizer.py yolov5\runs\detect\exp12\labels" or "python3 data_sanitizer.py yolov5\runs\detect\exp12\labels 4". 
