import cv2
import os
import random
import argparse

# Usage: python extractor_random.py video.mp4 30

def main():
    parser = argparse.ArgumentParser(description='Random Frame Selector')
    parser.add_argument("video", help="Source video name with .mp4 extension")
    parser.add_argument("frames", type=int, default=30, help="Maximum number of frames to save before exiting. Defaults to 30")

    args = parser.parse_args()

    video_name = args.video
    max_saves = args.frames

    base, _ = os.path.splitext(video_name)

    video = cv2.VideoCapture(video_name)
    if not video.isOpened():
        print("Error: Could not open video.")
        return

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    saved_frame_count = 0

    os.makedirs(base, exist_ok=True)

    print(f"Processing video: {video_name}")

    while saved_frame_count < max_saves:
        frame_id = random.randint(0, total_frames - 1)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = video.read()
        if not ret:
            continue

        cv2.imshow("Frame", frame)
        print("Do you want to save this frame? [y/n/x] (x to exit)")
        key = cv2.waitKey(0) & 0xFF

        if key == ord('y'):
            frame_filename = os.path.join(base, f"frame{frame_id}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1
            print(f"Saved: {frame_filename}")
        elif key == ord('x'):
            break

    video.release()
    cv2.destroyAllWindows()
    print(f"Finished. Saved {saved_frame_count} frames.")

if __name__ == "__main__":
    main()
