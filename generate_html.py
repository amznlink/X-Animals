import os

video_dir = 'videos'
output_html = 'index.html'

# Get a list of videos sorted by modification time (newest first)
videos = sorted([f for f in os.listdir(video_dir) if f.endswith('.mp4')],
                key=lambda x: os.path.getmtime(os.path.join(video_dir, x)), reverse=True)

video_sources = [os.path.join(video_dir, video) for video in videos]

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animals</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
            scroll-behavior: smooth;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .video-container {
            width: 100%;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
            top: 0;
            left: 0;
        }
        video {
            width: 100%;
            height: auto;
        }
        #video-list {
            height: 100vh;
            overflow-y: scroll;
            scroll-snap-type: y mandatory;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
        }
        .spacer {
            height: 100vh;
            scroll-snap-align: start;
        }
    </style>
</head>
<body>
<div id="video-list">
    <div class="spacer"></div>
'''

for i in range(len(video_sources)):
    html_content += '<div class="spacer"></div>'

html_content += '''
</div>
<div class="video-container">
    <video id="main-video" controls muted autoplay playsinline></video>
</div>
<script>
    const videoList = {video_sources};
    let currentIndex = 0;

    const videoElement = document.getElementById('main-video');
    videoElement.src = videoList[currentIndex];

    const spacers = document.querySelectorAll('.spacer');
    spacers.forEach((spacer, index) => {
        spacer.addEventListener('scroll', () => {
            if (index !== currentIndex) {
                videoElement.pause();
                videoElement.currentTime = 0;
                videoElement.src = videoList[index];
                currentIndex = index;
                videoElement.play();
            }
        });
    });
</script>
</body>
</html>
'''.format(video_sources=video_sources)

with open(output_html, 'w') as file:
    file.write(html_content)

print(f"HTML file '{output_html}' has been generated.")
