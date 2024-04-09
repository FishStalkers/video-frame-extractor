import cv2
import os
import argparse

# Usage: python extractor_sequential.py video.mp4 5000 30

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", help="Source video name with .mp4 extension")
    parser.add_argument("interval", type=int, default=5000, help="Interval between frames in milliseconds. Defaults to 5000ms (5 seconds)")
    parser.add_argument("frames", type=int, default=30, help="Maximum number of frames to save. Defaults to 30")

    args = parser.parse_args()

    video_name = args.video
    interval_ms = args.interval
    max_frames = args.frames

    base, _ = os.path.splitext(video_name)

    video = cv2.VideoCapture(video_name)
    if not video.isOpened():
        print("Error: Could not open video.")
        return

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * (interval_ms / 1000))

    os.makedirs(base, exist_ok=True)

    print(f"Processing video: {video_name}")

    frame_id = 0
    saved_frame_count = 0

    while saved_frame_count < max_frames:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = video.read()
        if not ret:
            break

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

        frame_id += frame_interval

    video.release()
    cv2.destroyAllWindows()
    print(f"Saved {saved_frame_count} frames.")

if __name__ == "__main__":
    main()
