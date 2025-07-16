import cv2
import os

# Path to your image folder (raw string to avoid backslash issues)
image_folder = r'C:\Users\Advait S\Downloads\dataset_ADAS\data\images'
video_name = 'project_video.mp4'

# List all .jpg files and sort them
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
images.sort()

# Read the first image to get frame size
first_image_path = os.path.join(image_folder, images[0])
frame = cv2.imread(first_image_path)
height, width, _ = frame.shape

# Define the video writer
out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (width, height))

# Write all images to video
for image in images:
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    out.write(frame)

out.release()
print("✅ Video generated successfully as 'project_video.mp4'")

