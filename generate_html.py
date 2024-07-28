import os
import requests
import re

def get_tweet_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls if url.strip()]

def fetch_video_url(tweet_url):
    oembed_url = f"https://publish.twitter.com/oembed?url={tweet_url}"
    response = requests.get(oembed_url)
    if response.status_code != 200:
        print(f"Failed to fetch oEmbed data for {tweet_url}")
        return None
    oembed_data = response.json()
    html_content = oembed_data['html']
    video_url = re.search(r'https://video.twimg.com/[^"]+', html_content)
    return video_url.group(0) if video_url else None

def download_video(video_url, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    video_filename = os.path.join(download_path, video_url.split("/")[-1])
    response = requests.get(video_url, stream=True)
    with open(video_filename, 'wb') as video_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                video_file.write(chunk)
    return video_filename

def generate_html(video_paths):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Animal Videos</title>
        <style>
            body, html {
                height: 100%;
                margin: 0;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                background: black;
            }
            video {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .video-container {
                width: 100%;
                height: 100%;
                position: relative;
            }
            .video-container video {
                display: none;
            }
            .video-container video.active {
                display: block;
            }
        </style>
    </head>
    <body>
    <div class="video-container">
    """

    for video_path in video_paths:
        html_content += f'<video src="{video_path}" controls></video>\n'

    html_content += """
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', (event) => {
            const videos = document.querySelectorAll('video');
            let currentVideoIndex = 0;

            const showVideo = (index) => {
                videos.forEach((video, idx) => {
                    video.classList.toggle('active', idx === index);
                    if (idx === index) {
                        video.play();
                    } else {
                        video.pause();
                        video.currentTime = 0;
                    }
                });
            };

            const nextVideo = () => {
                currentVideoIndex = (currentVideoIndex + 1) % videos.length;
                showVideo(currentVideoIndex);
            };

            document.addEventListener('wheel', (event) => {
                if (event.deltaY > 0) {
                    nextVideo();
                }
            });

            showVideo(currentVideoIndex);
        });
    </script>
    </body>
    </html>
    """
    return html_content

def main():
    file_path = 'tweet_urls.txt'
    download_path = 'videos'
    
    tweet_urls = get_tweet_urls(file_path)
    video_paths = []

    for tweet_url in tweet_urls:
        video_url = fetch_video_url(tweet_url)
        if video_url:
            video_path = download_video(video_url, download_path)
            video_paths.append(video_path)

    html_content = generate_html(video_paths)
    
    with open('index.html', 'w') as file:
        file.write(html_content)

if __name__ == "__main__":
    main()
