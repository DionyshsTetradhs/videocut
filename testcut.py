# Import the necessary packages
import os
import cv2
import pyscenedetect 

# Set the path to the input video file
video_path = '/path/to/video.mp4'

# Create a SceneManager object to perform scene detection
sm = pyscenedetect.manager.SceneManager()

# Set the video codec, FPS, and frame size for the video reader
video_reader = cv2.VideoCapture(video_path)
video_fps, video_frame_size = video_reader.get(cv2.CAP_PROP_FPS), (
    video_reader.get(cv2.CAP_PROP_FRAME_WIDTH),
    video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT)
)

# Create a VideoManager object and add the video to it
vm = pyscenedetect.manager.VideoManager([video_path])
sm.add_video_manager(vm)

# Set the detection method to use (in this case, content-aware scene detection)
detector_type = pyscenedetect.detectors.ContentDetector()
sm.add_detector(detector_type)

# Detect the scenes in the video
sm.detect_scenes()

# Get the list of scenes detected in the video
scene_list = sm.get_scene_list(video_path)

# Loop through each scene in the video
for i, scene in enumerate(scene_list):
    # Get the start and end frames for the scene
    start_frame, end_frame = scene[0], scene[1]

    # Set the start and end times for the scene in seconds
    start_time = start_frame / video_fps
    end_time = end_frame / video_fps

    # Set the output file path for the scene
    output_file_path = os.path.join(
        '/path/to/output/directory',
        'scene_{}.mp4'.format(i)
    )

    # Create a VideoWriter object for the output file
    output_video = cv2.VideoWriter(
        output_file_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        video_fps,
        video_frame_size
    )

    # Loop through each frame in the scene and save it to the output file
    for frame_num in range(start_frame, end_frame):
        _, frame = video_reader.read()
        output_video.write(frame)

    # Release the VideoWriter object
    output_video.release()

# Release the video reader
video_reader.release()
