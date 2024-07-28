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
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
            scroll-behavior: smooth;
        }}
        .video-container {{
            width: 100%;
            height: 100vh;
            position: relative;
            scroll-snap-align: start;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        #video-list {{
            display: flex;
            flex-direction: column;
            scroll-snap-type: y mandatory;
            overflow-y: scroll;
            height: 100vh;
        }}
        video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
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
    let currentVideoIndex = 0;

    function playVideo(index) {{
        videos.forEach((video, idx) => {{
            if (idx === index) {{
                video.play();
            }} else {{
                video.pause();
                video.currentTime = 0;
            }}
        }});
    }}

    function handleScroll() {{
        const index = Math.round(window.scrollY / window.innerHeight);
        if (index !== currentVideoIndex) {{
            currentVideoIndex = index;
            playVideo(currentVideoIndex);
        }}
    }}

    window.addEventListener('scroll', handleScroll);

    // Initial play
    playVideo(currentVideoIndex);
</script>
</body>
</html>
'''

with open(output_html, 'w') as file:
    file.write(html_content)

print(f"HTML file '{output_html}' has been generated.")
