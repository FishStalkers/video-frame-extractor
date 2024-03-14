# video-frame-extractor
This repository randomly selects a set of frames from a video to be used in YOLO analysis.
You must include the video as an argument. Number of frames is an optional argument. It will default to 3000. It will take approximately 83 seconds per 1k of frames to run.

A well formed command line execution could be "extractor.py 0004_vid.mp4 3000" or "extractor.py 0004_vid.mp4". The folder the frames are extracted to can be used directly as the input source in YOLOV5.
