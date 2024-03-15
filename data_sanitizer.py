import os
import datetime
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("path",help="Path to YOLO label output directory")
parser.add_argument("fish", nargs="?", default="3", help="Optional number of minimum fish for detection. Defaults to 3")

args = parser.parse_args()

dir_path = args.path
num_of_fish = int(args.fish)

count = 0

os.makedirs(dir_path+"_OUT/labels", exist_ok=True)
os.makedirs(dir_path+"_OUT/frames", exist_ok=True)

start = datetime.datetime.now()

print("Starting anotation examination :"+str(start))

for file in os.scandir(dir_path):
    if file.is_file():
            lines = 0
            with open(file, 'r') as f:
                newlines = f.readlines()
                newlines = len(newlines)
                lines += newlines
            if lines >= num_of_fish:
                shutil.copy(file, dir_path+"_OUT/labels")
                count = count + 1
                head,filename = os.path.split(file)
                base, extension = os.path.splitext(filename)
                base_frame_dir = os.path.dirname(os.path.dirname(file))
                shutil.copy(base_frame_dir+"/"+base+".jpg",dir_path+"_OUT/frames")
                f = open(dir_path+"_OUT/output summary.txt", "a")
                f.write(filename+"\n")
                f.close()
                
end = datetime.datetime.now()                
print("Ending examination :"+str(end))
print("Elapsed time: "+str((end-start)))                
print(str(count)+" annotations greater than or equal to "+str(num_of_fish)+" fish")
