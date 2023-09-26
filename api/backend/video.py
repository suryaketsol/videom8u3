import cv2
import subprocess

# Initialize webcam
cap = cv2.VideoCapture(0)

# FFmpeg command to convert the video feed to HLS format
command = [
    'ffmpeg',
    '-y',  # Overwrite output files without asking
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', '{}x{}'.format(640, 480),  # Size of one frame
    '-r', '25',  # Frames per second
    '-i', '-',  # Input comes from pipe
    '-an',  # No audio
    '-vf', 'scale=640:480',
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-f', 'hls',
    '-hls_time', '4',
    '-hls_list_size', '0',
    './static/stream.m3u8'
]

# Run FFmpeg command
ffmpeg = subprocess.Popen(command, stdin=subprocess.PIPE)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Write the RGB image into the pipe
    ffmpeg.stdin.write(frame.tobytes())
