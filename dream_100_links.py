import requests
import json
from urllib.parse import urlparse
import time


def google_search(query, api_key, cx, **kwargs):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": api_key, "cx": cx, **kwargs}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Search query failed: {response.status_code}")


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def find_website(query, api_key, cx):
    search_results = google_search(query + " website", api_key, cx)
    items = search_results.get("items", [])
    return items[0]["link"] if items else None


def find_social_media_page(query, platform, api_key, cx):
    search_results = google_search(query + " " + platform, api_key, cx)

    def is_platform_link(item):
        parsed = urlparse(item["link"])
        return f"{platform}.com" in parsed.netloc

    items = search_results.get("items", [])
    platform_links = list(filter(is_platform_link, items))
    return platform_links[0]["link"] if platform_links else None


def find_links(object, api_key, cx):
    query = object["name"]
    results = {
        "website": find_website(query, api_key, cx),
        "facebook": find_social_media_page(query, "facebook", api_key, cx),
        "twitter": find_social_media_page(query, "twitter", api_key, cx),
        "youtube": find_social_media_page(query, "youtube", api_key, cx),
        "linkedin": find_social_media_page(query, "linkedin", api_key, cx),
    }
    return merge_two_dicts(object, results)


def save_progress(output, filename):
    f = open(filename, "w")
    json.dump(output, f, indent=2)


def main():
    api_key = "AIzaSyCa7hmDieYjjhC40ZREbuO_ocmZWusaxro"
    cx = "05ca554a39da44f32"

    if not api_key or not cx:
        raise ValueError("Please set valid GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID")

    input_file = "dream100.json"
    output_file = "dream100_output.json"

    # Load input data
    with open(input_file, "r") as f:
        input_data = json.load(f)

    # Load existing output data or create empty list
    try:
        with open(output_file, "r") as f:
            output_data = json.load(f)
    except FileNotFoundError:
        output_data = []

    # Find the index of the last processed item
    last_processed = len(output_data)

    # Process remaining items
    for i, item in enumerate(input_data[last_processed:], start=last_processed):
        try:
            result = find_links(item, api_key, cx)
            output_data.append(result)
            save_progress(output_data, output_file)
            print(f"Processed item {i+1}/{len(input_data)}")
        except Exception as e:
            print(f"Error processing item {i+1}: {str(e)}")
            # Save progress before exiting
            save_progress(output_data, output_file)
            break

        # Add a delay to avoid hitting API rate limits
        time.sleep(1)

    print("Processing complete.")


if __name__ == "__main__":
    main()
