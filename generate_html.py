import requests
import os

# Fetch the list of tweet URLs from the local file
def get_tweet_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls if url.strip()]

# Download videos from the tweet URLs and save them to a directory
def download_videos(tweet_urls, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    video_paths = []
    for url in tweet_urls:
        response = requests.get(url, stream=True)
        video_filename = os.path.join(download_path, url.split("/")[-1] + ".mp4")
        with open(video_filename, 'wb') as video_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    video_file.write(chunk)
        video_paths.append(video_filename)
    
    return video_paths

# Generate the HTML file to display videos with fullscreen and autoplay
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

# Main function
def main():
    file_path = 'tweet_urls.txt'
    download_path = 'videos'
    
    # Get the list of URLs from the file
    tweet_urls = get_tweet_urls(file_path)

    # Download videos
    video_paths = download_videos(tweet_urls, download_path)

    # Generate HTML
    html_content = generate_html(video_paths)
    
    # Write HTML to file
    with open('index.html', 'w') as file:
        file.write(html_content)

if __name__ == "__main__":
    main()
