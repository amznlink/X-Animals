import os
import requests
import re
import tweepy
import youtube_dl

# Twitter API credentials from environment variables
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_tweet_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls if url.strip()]

def fetch_video_url(tweet_url):
    tweet_id = tweet_url.split('/')[-1]
    tweet = api.get_status(tweet_id, tweet_mode='extended')

    if 'media' in tweet.entities:
        media = tweet.entities['media']
        for media_item in media:
            if media_item['type'] == 'video':
                return media_item['video_info']['variants'][0]['url']
            elif media_item['type'] == 'animated_gif':
                return media_item['video_info']['variants'][0]['url']
    return None

def download_video(video_url, download_path):
    video_filename = os.path.join(download_path, video_url.split("/")[-1])
    if os.path.exists(video_filename):
        print(f"Video already exists: {video_filename}")
        return video_filename
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    response = requests.get(video_url, stream=True)
    with open(video_filename, 'wb') as video_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                video_file.write(chunk)
    return video_filename

def download_video_from_tweet(tweet_url):
    video_url = fetch_video_url(tweet_url)
    if video_url:
        return download_video(video_url, 'videos')
    return None

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
        video_path = download_video_from_tweet(tweet_url)
        if video_path:
            video_paths.append(video_path)

    html_content = generate_html(video_paths)
    
    with open('index.html', 'w') as file:
        file.write(html_content)

if __name__ == "__main__":
    main()
