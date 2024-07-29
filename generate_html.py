import os
import json

# Define the directory containing videos and the output JSON file
video_dir = 'videos'
video_list_json = 'video_list.json'

# Get a list of videos sorted by modification time (newest first)
videos = sorted([f for f in os.listdir(video_dir) if f.endswith('.mp4')],
                key=lambda x: os.path.getmtime(os.path.join(video_dir, x)), reverse=True)

# Create a list of video sources with their full paths
video_sources = [os.path.join(video_dir, video) for video in videos]

# Write the video sources to a JSON file
with open(video_list_json, 'w') as json_file:
    json.dump(video_sources, json_file)

print(f"JSON file '{video_list_json}' has been generated.")
