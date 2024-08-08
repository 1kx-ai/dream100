import json
import time
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


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
        print(f"An error occurred while fetching transcript for {video_url}: {str(e)}")
        return None


def process_influencer_videos(input_file, output_file):
    # Read the JSON file
    with open(input_file, "r") as file:
        data = json.load(file)

    # Process each record
    for i, record in enumerate(data):
        if "youtube_videos" not in record:
            print(f"Skipping {record['name']}: no YouTube videos found")
            continue

        if "youtube_transcripts" not in record:
            record["youtube_transcripts"] = []

        for video_url in record["youtube_videos"]:
            # Check if transcript for this video already exists
            if any(item["link"] == video_url for item in record["youtube_transcripts"]):
                print(f"Skipping {video_url}: transcript already fetched")
                continue

            print(f"Fetching transcript for {video_url}")
            transcript = get_youtube_transcript(video_url)

            if transcript:
                record["youtube_transcripts"].append(
                    {"link": video_url, "transcript": transcript}
                )
                print(f"Transcript fetched successfully for {video_url}")
            else:
                print(f"Failed to fetch transcript for {video_url}")

            # Write the updated data back to the file after each transcript
            with open(output_file, "w") as file:
                json.dump(data, file, indent=2)

            print(f"Progress saved after processing {video_url}")

            # Add a delay to avoid hitting rate limits
            time.sleep(1)

        print(f"Processed all videos for {record['name']} ({i+1}/{len(data)} records)")

    print(f"Processing complete. Final data written to {output_file}")


# Example usage
if __name__ == "__main__":
    input_file = "dream100_with_youtube_transcripts.json"
    output_file = "dream100_with_youtube_transcripts.json"
    process_influencer_videos(input_file, output_file)
