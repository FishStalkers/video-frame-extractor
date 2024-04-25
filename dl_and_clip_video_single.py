import subprocess
from moviepy.editor import VideoFileClip
import os

# Usage: Manually change the hardcoded paths and run
# TODO:
# Change to args
# Iterative version

def download_and_trim(video_remote_path, download_dir):
    rclone_path = 'C:/Users/JP/Desktop/RECENT/GT/FishStalkers/rclone-v1.66.0-windows-amd64/rclone.exe' # hardcoded rclone.exe path
    
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory {download_dir}")

    command = f'"{rclone_path}" copy "{video_remote_path}" "{download_dir}"'
    print("Executing command:", command)
    
    subprocess.run(command, shell=True, capture_output=True, text=True)

    video_filename = video_remote_path.split('/')[-1]
    local_path = os.path.join(download_dir, video_filename)

    try:
        with VideoFileClip(local_path) as clip:
            video_length = clip.duration
            portion_length = video_length * 0.2
            trimmed_clip = clip.subclip(0, portion_length)
            output_filename = os.path.join(download_dir, 'trimmed_' + video_filename)
            trimmed_clip.write_videofile(output_filename, codec='libx264')
            print("Video trimmed and saved to:", output_filename)
    except Exception as e:
        print(f"Error processing video: {e}")
    finally:
        if 'clip' in locals() and clip:
            clip.close()
        try:
            os.remove(local_path)
            print("Original video file removed.")
        except PermissionError as e:
            print(f"Failed to delete original video file due to: {e}")

# Change the paths to what you need
video_path = 'dropbox:BioSci-McGrath/Apps/CichlidPiData/__ProjectData/MC_multi/MC_s2_tr4_BowerBuilding/Videos/0005_vid.mp4' # path in DropBox
download_dir = 'E:/fishstalkers/videos/MC_s2_tr4_BowerBuilding' # output path
download_and_trim(video_path, download_dir)
