# Standard Library
import argparse
import datetime
import os
import subprocess
import random

# Libraries
import cv2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', nargs='?', default='../video.mp4', help='Source video path with .mp4 extension. Defaults to ../video.mp4')
    parser.add_argument('-f', '--frames', nargs='?', default=100, help='Number of frames to save before stopping. Defaults to 100')
    parser.add_argument('-t', '--threshold', nargs='?', type=int, default=3, help='Threshold for amount of fish to consider a frame worth saving. Defaults to 3')
    parser.add_argument('-w', '--weights', nargs='?', default='./best.pt', help='Path to YOLO weights file. Defaults to ./best.pt')
    parser.add_argument('-y', '--yolo', nargs='?', default='./yolov5', help='Path to YOLO directory. Defaults to ./yolov5. This should be the directory containing the YOLOv5 repository (and more specifically the detect.py script)')
    return parser.parse_args()


def extract_random_frame(video, video_length, visited_frames):
    frame = None

    # Loop until a frame is extracted
    while frame is None:
        frame_number = random.randint(0, video_length - 1)

        # Check if the frame has already been visited
        if frame_number in visited_frames:
            continue

        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if not ret:
            continue

    return frame, frame_number


def parse_fishies_from_yolo_output(output):
    fishy_count = 0
    # print('printing output')
    # print(output)
    # print('done printing output')

    # find ALL the lines that start with 'image 1/1'
    lines = [line for line in output.split('\n') if line.startswith('image 1/1')]

    print(f'number of lines that start with image 1/1:', len(lines))

    for line in output.split('\n'):
        if line.startswith('image 1/1'):

            # split line by spaces
            line = line.split(' ')

            try:
                _ = line[0]  # 'image'
                _ = line[1]  # '1/1'
                image_path = line[2]  # 'path/to/image.jpg'
                image_resolution = line[3]  # '480x640'
                fishy_count = int(line[4])  # 'number of fishies'
                fishy_species = line[5]  # 'species'
                fishy_sex = line[6]
                detection_time = line[7]
            except:
                if 'no detections' in line:
                    # This is a valid case, where no fishies were detected
                    continue
                # Print the line that caused the error
                print('Error parsing line:', line)

    return fishy_count


def run_yolo_detect(frame, weights, yolo, output_directory):
    # Temporarily save the frame to disk
    cv2.imwrite('temp_frame.jpg', frame)

    # Create a working directory for YOLO-annotated images
    working_directory = os.path.join(output_directory, 'yolo_output')
    os.makedirs(working_directory, exist_ok=True)

    # Run YOLO detect script on the frame as a subprocess to capture the output
    command = [
        'python3',
        f'{yolo}/detect.py',
        '--weights', weights,
        '--source', 'temp_frame.jpg',
        '--project',
        f'{output_directory}',
        '--exist-ok'
    ]
    # Run the command and capture the output
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # The stdout and stderr can now be accessed separately
    output = process.stdout
    errors = process.stderr
    combined_output = output + errors

    # Parse the output to get the number of fishies detected
    fishy_count = parse_fishies_from_yolo_output(combined_output)
    print('fishy count:', fishy_count)
    return fishy_count


def main(args):
    video_path = args.video
    frame_target = int(args.frames)
    fish_threshold = args.threshold

    visited_frames = set() # Set to keep track of visited frames
    saved_frames = 0 # Counter for saved frames

    # Create base directory for output
    base, extension = os.path.splitext(video_path)
    video_name = os.path.basename(base)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = f'{video_name}_{timestamp}'
    os.makedirs(directory, exist_ok=True)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    video_length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Loop until the target number of frames is reached
    while saved_frames < frame_target:

        # Extract a single random frame from the video
        frame, frame_number = extract_random_frame(video, video_length, visited_frames)

        # Add the frame to the visited frames set
        visited_frames.add(frame_number)

        # Run YOLO detect script on the frame determine number of fishies
        fishy_count = run_yolo_detect(frame, args.weights, args.yolo, directory)

        # If the number of fishies is greater than the threshold, save the frame
        if fishy_count >= fish_threshold:
            count_directory = os.path.join(directory, str(fishy_count))
            os.makedirs(count_directory, exist_ok=True)
            cv2.imwrite(count_directory + "/frame%d.jpg" % saved_frames, frame)
            saved_frames += 1

    # Release the video capture object
    video.release()
    cv2.destroyAllWindows()
    print(f'Extraction completed. The output frames are saved in: {directory}')


if __name__ == "__main__":
    args = parse_args()
    main(args=args)