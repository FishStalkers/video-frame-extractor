import cv2
import os
import argparse

# Usage: python extractor_sequential.py --video_path "E:/path/to/video.mp4" --interval 5000 --frames 30

def main():
    parser = argparse.ArgumentParser(description="Extract frames from a video at specified intervals.")
    parser.add_argument("--video_path", help="Full path to the source video file with extension, e.g., E:/videos/video.mp4")
    parser.add_argument("--interval", type=int, default=5000, help="Interval between frames in milliseconds. Defaults to 5000ms (5 seconds)")
    parser.add_argument("--frames", type=int, default=30, help="Maximum number of frames to save. Defaults to 30")

    args = parser.parse_args()

    video_path = args.video_path
    interval_ms = args.interval
    max_frames = args.frames

    if not video_path:
        print("Error: No video path provided.")
        return

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Error: Could not open video.")
        return

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * (interval_ms / 1000))
    base_name = os.path.basename(video_path)
    base_name_without_ext = os.path.splitext(base_name)[0]
    output_dir = os.path.join(os.path.dirname(video_path), f"{base_name_without_ext}_frames")  # Directory named after the video
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    print(f"Processing video: {video_path}")

    frame_id = 0
    saved_frame_count = 0

    while saved_frame_count < max_frames:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = video.read()
        if not ret:
            break

        cv2.imshow("Frame", frame)
        key = 0
        while key not in [ord('y'), ord('n'), ord('x')]:
            key = cv2.waitKey(0) & 0xFF

        if key == ord('y'):
            frame_filename = os.path.join(output_dir, f"frame{frame_id}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1
            print(f"Saved: {frame_filename}")
        elif key == ord('x'):
            cv2.destroyAllWindows()
            break

        cv2.destroyAllWindows()

        frame_id += frame_interval

    video.release()
    cv2.destroyAllWindows()
    print(f"Saved {saved_frame_count} frames.")

if __name__ == "__main__":
    main()
