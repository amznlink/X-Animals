import os

video_dir = 'videos'
output_html = 'index.html'

videos = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]

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
        }
        .video-container {
            width: 100%;
            height: 100vh;
            position: relative;
            scroll-snap-align: start;
        }
        #video-list {
            display: flex;
            flex-direction: column;
            scroll-snap-type: y mandatory;
            overflow-y: scroll;
            height: 100vh;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    </style>
</head>
<body>
<div id="video-list">
    <div class="video-container">
        <video id="video-player" controls></video>
    </div>
</div>
<script>
    const videoList = document.getElementById('video-list');
    const videoPlayer = document.getElementById('video-player');
    const videos = {videos};
    let currentVideoIndex = 0;

    function playVideo(index) {
        videoPlayer.src = videos[index];
        videoPlayer.play();
    }

    function handleScroll() {
        const index = Math.round(videoList.scrollTop / window.innerHeight);
        if (index !== currentVideoIndex) {
            currentVideoIndex = index;
            playVideo(currentVideoIndex);
        }
    }

    videoList.addEventListener('scroll', handleScroll);

    // Initial play
    playVideo(currentVideoIndex);

    // Preload next video for smoother transitions
    videoPlayer.addEventListener('ended', () => {
        if (currentVideoIndex < videos.length - 1) {
            currentVideoIndex++;
            playVideo(currentVideoIndex);
            videoList.scrollTop = currentVideoIndex * window.innerHeight;
        }
    });

    // Ensure the initial video is loaded and played on page load
    window.onload = () => {
        playVideo(currentVideoIndex);
    };
</script>
</body>
</html>
'''.format(videos=[f'{video_dir}/{video}' for video in videos])

with open(output_html, 'w') as file:
    file.write(html_content)

print(f"HTML file '{output_html}' has been generated.")
