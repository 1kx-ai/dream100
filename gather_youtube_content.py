import os
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import json
import time

API_KEY = "AIzaSyDfJMbk8UalElj9dM0uXScN6HZGbcaoIwA"

youtube = build("youtube", "v3", developerKey=API_KEY)


def get_youtube_transcript(video_url):
    try:
        # Extract video ID from the URL
        parsed_url = urlparse(video_url)
        video_id = parse_qs(parsed_url.query).get("v")

        if not video_id:
            raise ValueError("Invalid YouTube URL. Unable to extract video ID.")

        video_id = video_id[0]

        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine all text parts into a single string
        full_transcript = " ".join([entry["text"] for entry in transcript])

        return full_transcript

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def get_channel_id_from_url(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "www.youtube.com" or parsed_url.hostname == "youtube.com":
        print(parsed_url.path)
        if "/channel/" in parsed_url.path:
            return parsed_url.path.split("/")[-1]
        elif parsed_url.path == "/user/":
            username = parsed_url.path.split("/")[-1]
            response = (
                youtube.channels().list(part="id", forUsername=username).execute()
            )
            if "items" in response:
                return response["items"][0]["id"]
        elif parsed_url.path == "/c/":
            custom_name = parsed_url.path.split("/")[-1]
            response = (
                youtube.search()
                .list(part="id", q=custom_name, type="channel")
                .execute()
            )
            if "items" in response:
                return response["items"][0]["id"]["channelId"]
    return None


def get_channel_videos(channel_url):
    channel_id = get_channel_id_from_url(channel_url)
    if not channel_id:
        print("Invalid channel URL or unable to find channel ID.")
        return []

    video_links = []

    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,  # Adjust as needed, max is 50
        type="video",
    )

    while request:
        response = request.execute()

        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video_links.append(video_link)

        request = youtube.search().list_next(request, response)

    return video_links


def process_dream_100_links(input_file, output_file):
    # Read the JSON file
    with open(input_file, "r") as file:
        data = json.load(file)

    # Process each record
    for i, record in enumerate(data):
        if "youtube_videos" in record.keys():
            print(f"Skipping {record['name']}: already processed")
            continue

        if "youtube" in record and record["youtube"]:
            print(f"Processing YouTube channel for {record['name']}...")
            youtube_videos = get_channel_videos(record["youtube"])
            if youtube_videos is not None:
                record["youtube_videos"] = youtube_videos
                print(f"Found {len(youtube_videos)} videos for {record['name']}")
            else:
                print(f"Skipped adding videos for {record['name']} due to an error")
        else:
            print(f"No YouTube link found for {record['name']}")

        # Write the updated data back to the file after each record
        with open(output_file, "w") as file:
            json.dump(data, file, indent=2)

        # Add a delay to avoid hitting rate limits
        time.sleep(1)

        print(f"Processed {i+1}/{len(data)} records. Progress saved.")

    print(f"Processing complete. Final data written to {output_file}")


if __name__ == "__main__":
    file_path = "./dream100_with_youtube_links.json"
    output_path = "./dream100_with_youtube_links.json"
    process_dream_100_links(file_path, output_path)
