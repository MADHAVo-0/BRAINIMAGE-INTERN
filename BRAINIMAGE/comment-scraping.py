import re
import os
from googleapiclient.discovery import build

api_key = 'AIzaSyDAZ3Ya1XKxi_76C6CGKY6EYexYhDWXggY'  # Replace with your API key
youtube = build('youtube', 'v3', developerKey=api_key)

def extract_video_id(url):
    video_id = None
    youtube_regex = r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(youtube_regex, url)
    if match:
        video_id = match.group(1)
    return video_id

def get_video_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100
    )
    response = request.execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    while 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

    return comments

def save_comments_to_file(comments, base_file_name="comments"):
    index = 1
    while True:
        file_name = f"{base_file_name}_download_{index}.txt"
        if not os.path.exists(file_name):
            break
        index += 1

    with open(file_name, 'w', encoding='utf-8') as file:
        for idx, comment in enumerate(comments, 1):
            file.write(f"{idx}. {comment}\n")
    
    print(f"Comments saved to {file_name}")
    return file_name

youtube_url = input("Enter the YouTube video URL: ")
video_id = extract_video_id(youtube_url)
if video_id:
    comments = get_video_comments(video_id)
    if comments:
        save_comments_to_file(comments)
    else:
        print("No comments found.")
else:
    print("Invalid YouTube URL. Please check the URL and try again.")
