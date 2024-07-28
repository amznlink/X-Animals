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
            display: flex;
            justify-content: center;
            align-items: center;
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
'''

for i, video in enumerate(videos):
    html_content += f'''
    <div id="video{i+1}" class="video-container">
        <video src="{video_dir}/{video}" id="video{i+1}-player" muted playsinline></video>
    </div>
    '''

html_content += '''
</div>
<script>
    const videos = document.querySelectorAll('video');
    
    const options = {
        root: null,
        rootMargin: '0px',
        threshold: 1.0
    };

    function handleIntersect(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.requestFullscreen();
                entry.target.play();
            } else {
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                }
                entry.target.pause();
                entry.target.currentTime = 0;
            }
        });
    }

    const observer = new IntersectionObserver(handleIntersect, options);

    videos.forEach(video => {
        observer.observe(video);
    });

    // Scroll to the top to ensure the first video plays initially
    window.scrollTo(0, 0);
</script>
</body>
</html>
'''

with open(output_html, 'w') as file:
    file.write(html_content)

print(f"HTML file '{output_html}' has been generated.")
